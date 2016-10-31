#!/usr/bin/env python
# pylint: disable=missing-docstring,invalid-name
import os
import re
import sys

def edit_source(src):
    # Standard boilerplate
    src = re.sub("#include ?<bits/stdc\\+\\+\\.h>\\n{1,2}", "", src)
    src = re.sub("using namespace std;\\n{1,2}", "", src)
    src = re.sub("# *pylint:.+?\\n{1,2}", "", src)

    # Blank lines before top-of-file constructs
    src = re.sub("\\n\\n(#include|import|namespace \\{|class)", "\\n\\1", src)

    # Short if statements in C++
    src = re.sub("([ \\t]+)((?:if|for|while) ?\\(.{1,25}\\))\\n[ \\t]+(.{1,30})\\n", "\\1\\2 \\3\\n", src)

    # Short blocks in C++
    src = re.sub("([ \\t]+)(.{1,30} \\{)\\n[ \\t]+(.{1,30})\\n\\1\\}\\n", "\\1\\2 \\3 }\\n", src)

    return src


def dirs_and_files(path):
    ls = os.listdir(path)
    dirs = sorted([lse for lse in ls if os.path.isdir(os.path.join(path, lse)) and not lse.startswith(".")])
    files = sorted([lse for lse in ls if os.path.isfile(os.path.join(path, lse)) and not lse.startswith(".")])
    return dirs, files


def recursively_add_subsections(srcdir, dirname, nesting, nesting_levels):
    dirs, files = dirs_and_files(srcdir)
    res = "\\%s{\\texttt{%s}}\n" % (nesting_levels[nesting - 1], dirname.replace("_", "\\_"))

    for filex in files:
        res += "\\%s{\\texttt{%s}}\n\\begin{lstlisting}\n" % (nesting_levels[nesting], (dirname + "/" + filex).replace("_", "\\_"))
        with open(os.path.join(srcdir, filex)) as fx:
            res += edit_source(fx.read()) + "\n\\end{lstlisting}\n\n"

    for dirx in dirs:
        res += recursively_add_subsections(os.path.join(srcdir, dirx), dirname + "/" + dirx, nesting + 1, nesting_levels)

    return res


def recursively_add_sections(srcdir, nesting_levels):
    dirs, files = dirs_and_files(srcdir)
    res = "\\part{Top level}"

    for filex in files:
        res += "\\section{\\texttt{%s}}\n\\begin{lstlisting}\n" % filex.replace("_", "\\_")
        with open(os.path.join(srcdir, filex)) as fx:
            res += edit_source(fx.read()) + "\n\\end{lstlisting}\n\n"

    for dirx in dirs:
        res += recursively_add_subsections(os.path.join(srcdir, dirx), dirx, 1, nesting_levels)

    return res


def main():
    srcdir = os.path.abspath(sys.argv[1])
    outfile = os.path.abspath(sys.argv[2])
    headfile = os.path.join(srcdir, "../qlib_header.txt")
    footfile = os.path.join(srcdir, "../qlib_footer.txt")
    nestfile = os.path.join(srcdir, "../qlib_nesting.txt")

    nesting_levels = []
    with open(nestfile) as nestf:
        for line in nestf:
            nesting_levels.append(line.rstrip())

    res = ""
    with open(headfile) as headf:
        res += (headf.read() + "\n")

    res += recursively_add_sections(srcdir, nesting_levels)

    with open(footfile) as footf:
        res += (footf.read())

    with open(outfile, "w") as outf:
        outf.write(res)


if __name__ == "__main__":
    sys.exit(main())
