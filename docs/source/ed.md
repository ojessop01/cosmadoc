# ed

ed is the original Unix line editor, from the early 1970s.  It shows no text
on the screen unless you ask: you give it commands such as "print lines 1 to
5" or "replace this text on line 12".  Most people are better served by
[nano](nano.md), [Vim](vi.md) or [Emacs](emacs.md).

ed is still useful for making changes to files from scripts, because its
commands can be read from a file or a pipe.  For example, to replace `old`
with `new` on every line of a file and save it:

```
printf '%s\n' ',s/old/new/g' 'w' 'q' | ed -s myfile.txt
```

Type `man ed` on COSMA for the full list of commands.
