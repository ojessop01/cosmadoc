#!/bin/bash
# Regenerate docs/source/modulelist.md, and commit and push it if it changed.
#
# Run it on a COSMA login node, from a clone that can push to the docs
# repository.  For example, to update the page every night at 02:00:
#
#   0 2 * * * /path/to/cosmadoc/docs/tools/update_modulelist.sh >> $HOME/modulelist-update.log 2>&1
#
# The page is only replaced after a complete run whose results look sensible,
# so a failed run leaves the existing page alone and exits with an error.
# A change to the date alone is not committed.  Only one update runs at a time.
set -euo pipefail

repo=$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)
page=docs/source/modulelist.md
stamp() { date '+%Y-%m-%d %H:%M:%S'; }

exec 9> "$repo/.git/update_modulelist.lock"
if ! flock -n 9; then
    echo "$(stamp) another update is still running, so not starting"
    exit 0
fi

if [ -n "$(git -C "$repo" status --porcelain -- "$page")" ]; then
    echo "$(stamp) $page has uncommitted changes, so not updating" >&2
    exit 1
fi
git -C "$repo" pull --ff-only --quiet

if ! python3 "$repo/docs/tools/list_modules.py" --output "$repo/$page"; then
    echo "$(stamp) the module list could not be generated, so the page was left unchanged" >&2
    exit 1
fi

# Ignore the line saying when the list was generated.
if [ -z "$(git -C "$repo" diff -U0 -- "$page" | grep -E '^[-+][^-+]' | grep -v 'This list was generated in')" ]; then
    git -C "$repo" checkout -- "$page"
    echo "$(stamp) no modules have changed"
    exit 0
fi

git -C "$repo" commit --quiet -m "Auto-update of modulelist.md" -- "$page"
git -C "$repo" push --quiet
echo "$(stamp) the module list was updated and pushed"
