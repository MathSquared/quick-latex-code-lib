#!/usr/bin/env python
# pylint: disable=missing-docstring,invalid-name
import os
import sys

# the first level is never used for naked code
_nesting_levels = ['part', 'section', 'subsection', 'subsubsection']


def dirs_and_files(path):
    ls = os.listdir(path)
    dirs = [lse for lse in ls if os.path.isdir(os.path.join(path, lse)) and not lse.startswith(".")]
    files = [lse for lse in ls if os.path.isfile(os.path.join(path, lse)) and not lse.startswith(".")]
    return dirs, files


def recursively_add_subsections(srcdir, dirname, nesting):
    dirs, files = dirs_and_files(srcdir)
    res = "\\%s{\\texttt{%s}}\n" % (_nesting_levels[nesting - 1], dirname.replace("_", "\\_"))

    for filex in files:
        res += "\\%s{\\texttt{%s}}\n\\begin{lstlisting}\n" % (_nesting_levels[nesting], (dirname + "/" + filex).replace("_", "\\_"))
        with open(os.path.join(srcdir, filex)) as fx:
            res += fx.read() + "\n\\end{lstlisting}\n\n"

    for dirx in dirs:
        res += recursively_add_subsections(os.path.join(srcdir, dirx), dirname + "/" + dirx, nesting + 1)

    return res


def recursively_add_sections(srcdir):
    dirs, files = dirs_and_files(srcdir)
    res = "\\part{Top level}"

    for filex in files:
        res += "\\section{\\texttt{%s}}\n\\begin{lstlisting}\n" % filex
        with open(os.path.join(srcdir, filex)) as fx:
            res += fx.read() + "\n\\end{lstlisting}\n\n"

    for dirx in dirs:
        res += recursively_add_subsections(os.path.join(srcdir, dirx), dirx, 1)

    return res


def main():
    srcdir = os.path.abspath(sys.argv[1])
    outfile = os.path.abspath(sys.argv[2])
    headfile = os.path.join(srcdir, "../qlib_header.txt")
    footfile = os.path.join(srcdir, "../qlib_footer.txt")

    res = ""
    with open(headfile) as headf:
        res += (headf.read() + "\n")

    res += recursively_add_sections(srcdir)

    with open(footfile) as footf:
        res += (footf.read())

    with open(outfile, "w") as outf:
        outf.write(res)


if __name__ == "__main__":
    sys.exit(main())
