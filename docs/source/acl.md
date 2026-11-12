# Sharing files with access control lists

Normal Unix permissions let you give access to three groups of people: the
file's owner, the file's group, and everyone else.  On COSMA, everyone in your
project is usually in the same group.  To give access to someone outside your
project, or to just one person, use an **access control list (ACL)**.  ACLs
work on the Lustre data file systems (`/cosma5`, `/cosma7`, `/cosma8`, `/snap7`
and `/snap8`).

An ACL is a list of extra permissions, for named users or groups, attached to
a file or folder.  The commands are `setfacl` to change it and `getfacl` to
show it.

## Seeing whether a file has an ACL

`ls -l` shows a `+` after the permissions of a file or folder that has an
ACL:

```
$ ls -ld shared
drwxr-sr-x+ 2 me   mygroup 4096 Nov 12 10:00 shared
```

`getfacl` shows the full list:

```
$ getfacl shared
# file: shared
# owner: me
# group: mygroup
user::rwx
user:colleague:r-x
group::r-x
mask::r-x
other::r-x
default:user::rwx
default:user:colleague:r-x
...
```

## Giving one person access to a file

To let the user `colleague` read a file:

```
setfacl -m u:colleague:r /cosma8/data/PROJECT/USER/results.hdf5
```

`-m` adds or changes an entry.  `u:` names a user and `g:` a group, and the
permissions are any of `r` (read), `w` (write) and `x` (execute, or for a
folder, enter it).

## Sharing a whole folder

To share a folder and everything that will be created in it, set two
entries: one for the folder as it is now, and a **default** entry
(`-d`), which is copied to every new file and folder created inside it.

```
# the folder itself, and everything already in it
setfacl -R -m u:colleague:rX /cosma8/data/PROJECT/USER/shared

# everything created in it from now on
setfacl -R -d -m u:colleague:rX /cosma8/data/PROJECT/USER/shared
```

`-R` applies the change to everything already inside the folder.  A capital
`X` gives execute permission only to folders (and to files that are already
executable), which is what you want for read-only sharing.

New files created in the folder then get the entry automatically.
`getfacl` on a new file shows `user:colleague:r-x  #effective:r--`, which
means the person can read it: the `effective` value is what applies.

### The person also needs to reach the folder

To reach `/cosma8/data/PROJECT/USER/shared`, the other person needs execute
(`x`) permission on every folder above it.  If they get `Permission denied`
even though the folder's ACL is right, check the folders above it:

```
namei -m /cosma8/data/PROJECT/USER/shared
```

Each folder listed must allow them `x`, either for "other" (the last letter of
the permissions) or through an ACL.  To give only that person access to your
own folder, without opening it to everyone:

```
setfacl -m u:colleague:x /cosma8/data/PROJECT/USER
```

This lets them pass through your folder to the shared one, but not list what
else is in it.

## Removing access

```
# remove one person's entry from a file or folder
setfacl -x u:colleague /cosma8/data/PROJECT/USER/results.hdf5

# remove one person from a folder and everything in it, including the default
setfacl -R -x u:colleague -x d:u:colleague /cosma8/data/PROJECT/USER/shared

# remove all ACL entries from a folder and everything in it
setfacl -R -b /cosma8/data/PROJECT/USER/shared
```

## Things to know

- **ACLs are easy to forget**, because `ls -l` only shows them as a `+`.  Check
  with `getfacl` before sharing a folder that holds anything else.
- **The mask limits what any ACL entry can give.**  If a person's entry shows
  `#effective:` with fewer permissions than you set, the mask is the reason.
  Changing the group permissions with `chmod` also changes the mask.
- **Write access is shared responsibility.**  If you give someone write
  access, they can delete or change your files.  Give read access unless they
  really need to write.
- **Copying can drop ACLs.**  `cp` and `rsync` do not keep ACLs unless asked
  (`cp -a`, or `rsync -A`).  Files created inside a folder with a default ACL
  get it anyway.
- **For a whole group of people**, it may be easier to ask cosma-support about
  a shared project or group, rather than keeping a long list of names.

For more detail, see `man setfacl` and `man getfacl`.
