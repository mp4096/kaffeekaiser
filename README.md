# Usage

To create tally sheets: Go to `kreuzliste` and run `python create.py <config filename>`,
for example

```sh
python create.py example.yml
```

The create.py file will make a .tex file from the configuration given in 
example.yml and run pdflatex to export a .pdf file.

# Requirements

All this stuff was tested with Python 3.6 and TeXLive on Xubuntu 16.04 LTS.
If you have problems with MiKTeX and Windows, use `\usepackage{lmodern}`
instead of `\usepackage{CormorantGaramond}`.

The exexample.yml file will generate an excellent alternate version of this
document with a header logo in the upper right. Before executing the command
above, download the logo file to the build directory and name it exheader.png
TUM academics might want to use these excellent graphics from their alma mater:

https://portal.mytum.de/corporatedesign/150_jahre_tum/index_150/150_jahre_tum/badge/index_150_logo
