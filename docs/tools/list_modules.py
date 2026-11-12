#!/usr/bin/env python3
"""Generate the list of COSMA modules as a Markdown page.

To update the page automatically, run docs/tools/update_modulelist.sh, for
example from cron.  To run this script by hand, use a COSMA login node and
commit the result:

    python3 docs/tools/list_modules.py --output docs/source/modulelist.md

With --output, the file is only replaced once the whole run has finished and
the results look sensible, so a failed run leaves the existing page alone.
Without it, the page is printed to standard output.  Avoid redirecting that
straight into the page with ">", because the shell empties the file before the
script starts, so a failed run leaves an empty page.

As well as listing the modules, the script finds which compiler and MPI
modules each library can be used with.  It reads the build directories that
the modulefiles use, then loads each combination to check that it works, so
only combinations that load are shown.  It also checks each module in
old-modules, and whether its programs are missing system libraries.  This
takes about a minute.
"""
import argparse
import collections
import concurrent.futures
import contextlib
import datetime
import glob
import html
import io
import os
import re
import subprocess
import sys
import tempfile

MODULEFILES = "/cosma/local/Modules/modulefiles"
SECTIONS = {
    "compilers": "Compilers",
    "mpi": "MPI",
    "libraries": "Libraries",
    "tools": "Tools",
    "MAD": "Large memory node tools",
}
# The second file sets the COSMA module path, in case this runs outside a login shell.
# Start each command from COSMA's own module setup, whatever the caller's
# environment.  The setup only sets MODULEPATH if it is not already set, so
# clear it first: otherwise a bare environment, such as cron, only sees the
# system modules, and a user's own "module use" directories would be listed.
INIT = ("unset MODULEPATH LOADEDMODULES _LMFILES_ MODULESHOME; "
        "source /etc/profile.d/cosma-local-modules.sh >/dev/null 2>&1; "
        "module purge >/dev/null 2>&1; ")
TOKEN = re.compile(r"^(?P<name>[^\s(<]+)(?:\((?P<tags>[^)]*)\))?")
# Build directory names, as used by module_utils.tcl on COSMA.
COMP_DIR = re.compile(r"^([a-zA-Z]+)_([0-9.a-z-]+)$")
MPI_DIR = re.compile(r"^([a-zA-Z]+)_([0-9.a-z-]+)_([a-zA-Z_0-9]+mpi)_([0-9.a-z-]+)$")
ONEAPI = ["compiler-rt", "tbb", "compiler"]
OLD = "module load old-modules >/dev/null 2>&1; "


# Commands that could not be run at all, for example because a process could
# not be started.  A few are tolerated; many mean the results are unreliable.
ERRORS = []
MAX_ERRORS = 20
# The smallest results that look like a real run.
MIN_MODULES = 100
MIN_DEPENDENCY_TABLES = 5


def run(script, extra="", timeout=300):
    try:
        return subprocess.run(["bash", "-c", INIT + extra + script], capture_output=True,
                              text=True, check=False, timeout=timeout)
    except (OSError, subprocess.SubprocessError) as err:
        ERRORS.append(f"{script[:60]}: {err}")
        return subprocess.CompletedProcess(args=script, returncode=1, stdout="", stderr="")


def module_avail(extra=""):
    """Return {section: {name: (versions, default)}} from `module -t avail`."""
    out = run(f"{extra}module -t avail 2>&1").stdout
    data = collections.defaultdict(dict)
    section = None
    for line in out.splitlines():
        if line.endswith(":") and line.startswith("/"):
            section = line[:-1].rstrip("/").rsplit("/", 1)[-1]
            continue
        match = TOKEN.match(line.strip())
        if not match or section is None:
            continue
        path = match.group("name").split("/")
        name = path[0]
        version = "/".join(path[1:])
        versions, default = data[section].get(name, ([], None))
        if version:
            versions.append(version)
        if "default" in (match.group("tags") or ""):
            default = version
        data[section][name] = (versions, default)
    return data


def compiler_options(comp, version):
    """Possible commands to load a compiler, for a build directory's compiler."""
    module = f"{comp}_comp/{version}"
    if comp == "intel":
        return [[module], [module] + ONEAPI]
    return [[module]]


def mpi_options(kind, version, comp, comp_version):
    """Possible commands to load an MPI, for a build directory's MPI."""
    name = "openmpi" if kind == "ompi" else kind
    options = [[f"{name}/{version}"]]
    if kind == "intel_mpi" and comp == "intel" and version == comp_version:
        options.insert(0, ["mpi"])
    return options


def parse_modulefiles(sections):
    """Find modules that need a compiler or an MPI, and their build directories."""
    needs = {}
    for section in sections:
        for path in sorted(glob.glob(f"{MODULEFILES}/{section}/*/*")):
            name, version = path.split("/")[-2:]
            if version.endswith("~") or version.startswith("."):
                continue
            try:
                text = open(path, errors="replace").read()
            except OSError:
                continue
            if "CheckCompiler" not in text:
                continue
            match = re.search(r"set\s+basedir\s+(\S+)", text)
            if not match:
                continue
            basedir = match.group(1).replace("${name}", name).replace("$name", name)
            builds = [os.path.basename(os.path.dirname(p))
                      for p in glob.glob(os.path.join(basedir, "*", version))]
            needs[(name, version)] = ("CheckMPI" in text, builds)
    return needs


def candidates(name, version, uses_mpi, builds):
    """Yield (compiler, mpi, commands) to try for each build directory."""
    for build in sorted(builds):
        match = (MPI_DIR if uses_mpi else COMP_DIR).match(build)
        if not match:
            continue
        comp, comp_version = match.group(1), match.group(2)
        comp_cmds = compiler_options(comp, comp_version)
        if uses_mpi:
            kind, mpi_version = match.group(3), match.group(4)
            mpi_cmds = mpi_options(kind, mpi_version, comp, comp_version)
        else:
            mpi_cmds = [[]]
        tries = [c + m + [f"{name}/{version}"] for c in comp_cmds for m in mpi_cmds]
        yield build, tries


def works(commands, extra=""):
    """True if every module in the command loads, including the target."""
    script = " ".join(f"module load {c} >/dev/null 2>&1;" for c in commands)
    loaded = " && ".join(f"module is-loaded {c}" for c in commands)
    return run(f"{script} {loaded}", extra).returncode == 0


def check(item):
    (name, version), build, tries, extra = item
    for commands in tries:
        if works(commands, extra):
            return name, version, build, commands
    return name, version, build, None


def find_dependencies(sections, extra=""):
    """Return {name: {version: [command lists]}} for combinations that load."""
    jobs = []
    needs_mpi = collections.defaultdict(bool)
    for (name, version), (uses_mpi, builds) in parse_modulefiles(sections).items():
        needs_mpi[name] |= uses_mpi
        for build, tries in candidates(name, version, uses_mpi, builds):
            jobs.append(((name, version), build, tries, extra))
    found = collections.defaultdict(lambda: collections.defaultdict(list))
    failed = collections.Counter()
    with concurrent.futures.ThreadPoolExecutor(max_workers=16) as pool:
        for name, version, _, commands in pool.map(check, jobs):
            if commands:
                found[name][version].append(commands)
            else:
                failed[name] += 1
    return found, failed, needs_mpi


# The main program of modules whose program is not named after the module.
MAIN_PROGRAM = {"gnu_comp": "gcc", "llvm": "clang", "aocc": "clang", "aocc_comp": "clang",
                "intel_comp": "icc", "nvhpc": "nvc", "nvhpc-nompi": "nvc", "python": "python"}


def old_status(module):
    """Load an old module, then look for missing libraries in the programs it adds."""
    script = (
        'before="$PATH"; module load ' + module + ' >/dev/null 2>&1; '
        'module is-loaded ' + module + ' || { echo NOLOAD; exit 0; }; '
        'echo "$PATH" | tr ":" "\\n" | grep -vxF -f <(echo "$before" | tr ":" "\\n") | '
        'while read -r d; do echo "NEWDIR $d"; [ -d "$d" ] && echo "HASDIR $d"; '
        'find -L "$d" -maxdepth 1 -type f -perm -u+x 2>/dev/null | head -500 | sed "s/^/FILE /"; done | '
        'while read -r kind f; do if [ "$kind" = FILE ]; then echo "PROG $f"; '
        'ldd "$(readlink -f "$f")" 2>/dev/null | grep "=> not found" | sed "s/^/MISSING /"; '
        'else echo "$kind $f"; fi; done')
    out = run(script, OLD).stdout
    if "NOLOAD" in out:
        return "noload", [], 0, 0
    programs, broken, libs, current = 0, set(), set(), None
    for line in out.splitlines():
        if line.startswith("PROG "):
            programs += 1
            current = line[5:]
        elif line.startswith("MISSING ") and current:
            broken.add(current)
            libs.add(line.split()[1])
    name = module.split("/")[0]
    main = MAIN_PROGRAM.get(name, name)
    if broken:
        if len(broken) == programs:
            state = "allmissing"
        elif any(os.path.basename(b) == main for b in broken):
            state = "mainmissing"
        else:
            state = "somemissing"
        return state, sorted(libs), len(broken), programs
    if "NEWDIR " in out and "HASDIR " not in out:
        return "notinstalled", [], 0, 0
    return ("loads" if programs else "noprogs"), [], 0, programs


def old_modules(current):
    """Return the modules only reachable through old-modules, with their status."""
    old = module_avail(OLD).get("centos7", {})
    plain = []
    for name, (versions, _) in old.items():
        for version in versions or [""]:
            plain.append(f"{name}/{version}" if version else name)
    needs = parse_modulefiles(["centos7"])
    direct = [m for m in plain if tuple(m.split("/", 1)) not in needs]
    with concurrent.futures.ThreadPoolExecutor(max_workers=16) as pool:
        status = dict(zip(direct, pool.map(old_status, direct)))
    deps, failed, needs_mpi = find_dependencies(["centos7"], OLD)
    return old, status, deps, failed, needs_mpi


def version_key(text):
    return [int(p) if p.isdigit() else p for p in re.split(r"(\d+)", text)]


def write_table(mods, deps, needs_mpi):
    print("| Module | Default | Other versions | Needs |")
    print("| ------ | ------- | -------------- | ----- |")
    for name in sorted(mods, key=str.lower):
        versions, default = mods[name]
        others = [v for v in versions if v != default]
        shown = ", ".join(others[-6:])
        if len(others) > 6:
            shown = f"{len(others) - 6} older, then {shown}"
        need = ""
        if name in deps:
            label = "Compiler and MPI" if needs_mpi[name] else "Compiler"
            need = f'<a href="#dep-{name}">{label}</a>'
        print(f"| `{name}` | {default or ''} | {shown} | {need} |")
    print()


def describe(commands):
    """Split a working command list into compiler, MPI and the full command."""
    target = commands[-1]
    rest = commands[:-1]
    comp = [c for c in rest if c.endswith("_comp") or "_comp/" in c]
    mpi = [c for c in rest if c not in comp and c not in ONEAPI]
    mpi_text = "Intel MPI (`mpi`)" if mpi == ["mpi"] else ", ".join(mpi)
    return (comp[0] if comp else ""), mpi_text, "module load " + " ".join(commands), target


def write_dependencies(deps, failed, prefix="dep", heading=True, old=False):
    if heading:
        print("## What to load first\n")
        print("Many libraries can only be loaded after a compiler, and some also need an MPI "
              "module.  For each library below, find your version to see the combinations "
              "that work, and the command that loads them.  Each combination was tested when "
              "this page was generated.\n")
    for name in sorted(deps, key=str.lower):
        versions = deps[name]
        total = sum(len(v) for v in versions.values())
        plural = "s" if total != 1 else ""
        print(f'<div class="module-deps" id="{prefix}-{name}">\n')
        print(f'<h3><code>{html.escape(name)}</code></h3>\n')
        print(f"<p>{len(versions)} version{'s' if len(versions) != 1 else ''}, "
              f"{total} combination{plural}.</p>\n")
        print('<table class="docutils"><thead><tr><th>Version</th><th>Compiler</th><th>MPI</th>'
              "<th>Command</th></tr></thead><tbody>")
        for version in sorted(versions, key=version_key, reverse=True):
            rows = sorted(versions[version], key=lambda c: version_key(" ".join(c)), reverse=True)
            for i, commands in enumerate(rows):
                comp, mpi, command, _ = describe(commands)
                if old:
                    command = "module load old-modules " + command[len("module load "):]
                cell = (f'<td rowspan="{len(rows)}"><code>{html.escape(version)}</code></td>'
                        if i == 0 else "")
                print(f"<tr>{cell}<td><code>{html.escape(comp)}</code></td>"
                      f"<td>{html.escape(mpi).replace('`mpi`', '<code>mpi</code>')}</td>"
                      f"<td><code>{html.escape(command)}</code></td></tr>")
        print("</tbody></table>\n")
        if failed.get(name):
            print(f"<p>{failed[name]} other builds could not be loaded, "
                  "so they are not shown.</p>\n")
        print("</div>\n")


def generate():
    """Write the page to standard output, and return a summary for checking."""
    today = datetime.date.today().strftime("%B %Y")
    data = module_avail()
    old = module_avail(OLD)
    deps, failed, needs_mpi = find_dependencies(SECTIONS)
    total = sum(len(v[0]) or 1 for s in data.values() for v in s.values())
    print("# List of modules\n")
    print(f"This list was generated in {today} and shows {total} modules on the "
          "login nodes.  It can go out of date, so run `module avail` for the "
          "current list, or `module avail NAME` to search.  See "
          "[modules](modules.md) for how to use them.\n")
    print("Where no default is shown, `module load NAME` loads the last version "
          "listed.  The Needs column shows modules that must be loaded after a "
          "compiler or MPI module: follow the link to see which ones.\n")
    print("The list is generated by `docs/tools/list_modules.py`.\n")
    for key, title in SECTIONS.items():
        if key in data:
            print(f"## {title}\n")
            write_table(data[key], deps, needs_mpi)
    write_dependencies(deps, failed)
    write_old(data, old)
    return total, data, deps


STATUS_TEXT = {
    "loads": "Loads, and no missing libraries were found",
    "noprogs": "Loads, but adds no programs to check",
    "somemissing": "Some programs are missing system libraries",
    "allmissing": "No programs can run: all are missing system libraries",
    "mainmissing": "The main program is missing system libraries",
    "noload": "Does not load",
    "notinstalled": "Loads, but its files are not installed",
}


def main():
    parser = argparse.ArgumentParser(description="Generate the COSMA module list page.")
    parser.add_argument("-o", "--output", help="write the page to this file, only if the run succeeds")
    args = parser.parse_args()
    page = io.StringIO()
    with contextlib.redirect_stdout(page):
        total, data, deps = generate()
    problems = []
    if total < MIN_MODULES:
        problems.append(f"only {total} modules were found")
    missing = [s for s in ("compilers", "mpi", "libraries", "tools") if s not in data]
    if missing:
        problems.append("no modules were found in " + ", ".join(missing))
    if len(deps) < MIN_DEPENDENCY_TABLES:
        problems.append(f"only {len(deps)} libraries had working compiler combinations")
    if len(ERRORS) > MAX_ERRORS:
        problems.append(f"{len(ERRORS)} commands could not be run, for example: {ERRORS[0]}")
    if problems:
        print("list_modules.py: not writing the page, because " + "; ".join(problems) + ".",
              file=sys.stderr)
        sys.exit(1)
    if not args.output:
        sys.stdout.write(page.getvalue())
        return
    folder = os.path.dirname(os.path.abspath(args.output))
    with tempfile.NamedTemporaryFile("w", dir=folder, prefix=".modulelist-", suffix=".tmp",
                                     delete=False, encoding="utf-8") as tmp:
        tmp.write(page.getvalue())
    os.chmod(tmp.name, 0o644)
    os.replace(tmp.name, args.output)


def write_old(data, old_all):
    current = {n: d for s in data.values() for n, (_, d) in s.items()}
    current_versions = {n: v for s in data.values() for n, (v, _) in s.items()}
    old, status, deps, failed, needs_mpi = old_modules(current)
    counts = collections.Counter(s[0] for s in status.values())
    print("## Older modules\n")
    print("COSMA used CentOS 7 until it was reinstalled with Rocky Linux 9 in July 2024 "
          "(see the [cluster upgrade](clusterupgrade.md)).  Modules built for CentOS 7 are "
          "still available, but are hidden until you load `old-modules`:\n")
    print("```\nmodule load old-modules\nmodule avail\n```\n")
    print("Many of these programs no longer run, because they need system libraries that "
          "Rocky Linux 9 does not have.  Please use a current module if there is one, and "
          "test an old one before relying on it.  This table shows what was found when this "
          "page was generated:\n")
    print(f"- {counts['loads'] + counts['noprogs']} load, and no missing libraries were found.")
    print(f"- {counts['allmissing'] + counts['mainmissing']} load, but their main program cannot run.")
    print(f"- {counts['somemissing']} load, but some of their programs are missing "
          "system libraries.  These may still work, if the programs you need are not affected.")
    print(f"- {counts['notinstalled']} load, but their files are not installed.")
    print(f"- {counts['noload']} do not load.")
    print(f"- {sum(len(v) for v in deps.values())} combinations of modules that need a "
          "compiler load: see [what to load first](#older-modules-that-need-a-compiler).\n")
    print("Loading a module and finding no missing libraries does not guarantee that a "
          "program works.  The check only covers programs that the module adds to your PATH.\n")
    groups = collections.defaultdict(list)
    for module, (state, missing, broken, programs) in status.items():
        name, _, version = module.partition("/")
        detail = f"{broken} of {programs} programs" if state == "somemissing" else ""
        if state == "mainmissing":
            main = MAIN_PROGRAM.get(name, name)
            detail = f"`{main}` and {broken - 1} other programs" if broken > 1 else f"`{main}`"
        groups[(name, state, tuple(missing[:3]), detail)].append(version)
    names = sorted({key[0] for key in groups} | set(deps), key=str.lower)
    print("| Module | Versions | Status | Current module |")
    print("| ------ | -------- | ------ | -------------- |")
    for name in names:
        now = ""
        if name in current_versions:
            now = f"`{name}/{current[name]}`" if current[name] else f"`{name}`"
        rows = [(k, v) for k, v in groups.items() if k[0] == name]
        for (_, state, missing, detail), versions in sorted(rows, key=lambda r: r[0][1]):
            text = STATUS_TEXT[state]
            if detail and state == "mainmissing":
                text = f"{detail} {'is' if ' and ' not in detail else 'are'} missing system libraries"
            elif detail:
                text = f"{detail} are missing system libraries"
            if missing:
                text += ", such as " + ", ".join(f"`{m}`" for m in missing)
            if state == "mainmissing":
                text += ", so it will not run"
            shown = ", ".join(sorted(versions, key=version_key)) or "-"
            print(f"| `{name}` | {shown} | {text} | {now} |")
            now = ""
        if name in deps:
            label = "Compiler and MPI" if needs_mpi[name] else "Compiler"
            shown = ", ".join(sorted(deps[name], key=version_key))
            print(f'| `{name}` | {shown} | Needs a <a href="#dep-old-{name}">{label}</a> | {now} |')
    print()
    print("### Older modules that need a compiler\n")
    print("These old modules can only be loaded after an old compiler, and some also need "
          "an MPI module.  Each command was tested when this page was generated.\n")
    write_dependencies(deps, failed, prefix="dep-old", heading=False, old=True)


if __name__ == "__main__":
    main()
