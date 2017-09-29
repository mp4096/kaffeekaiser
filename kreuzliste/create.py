import codecs
from datetime import date
import os
import random
import re
from string import Template
import subprocess
import sys
import tempfile
import yaml


def run_pdflatex(path_to_file, filename):
    args = ["pdflatex", "--interaction=nonstopmode", filename]
    with open(os.devnull, 'w') as FNULL:
        res = subprocess.run(args, cwd=path_to_file, stdout=FNULL).returncode
    return res


def make_main_file(single_sheets, data):
    context = {}
    context["language"] = data["language"]
    context["includes"] = "\n\n\\clearpage\n\n".join(single_sheets)
    return Template(data["main_file_template"]).substitute(context)


def make_single_sheet(group, users, data):
    context = {}
    context["title"] = group
    context["datestamp"] = date.today().isoformat()
    context["creator_id"] = data["creator_id"]
    context["quote"] = random.choice(data["quotes"])

    context["contents"] = ", ".join((
        create_tikz_contents(data["offset"] + i*data["increment"], u)
        for i, u in enumerate(users)
        ))
    return Template(data["single_sheet_template"]).substitute(context)


def create_tikz_contents(y_pos, user_spec):
    position = "{:f} cm".format(y_pos)
    first_line = user_spec["last_name"]
    if "supervisor" in user_spec:
        second_line = "({:s})".format(user_spec["supervisor"])
    else:
        second_line = user_spec["first_name"]
    return "/".join((position, first_line, second_line))


def create_tally_sheets(filename):
    with codecs.open(filename, "r", encoding="utf-8") as f:
        data = yaml.load(f)

    single_sheets = (
        make_single_sheet(group, users, data)
        for group, users in data["groups"].items()
        )

    tex_filename = Template(data["filename_template"]).substitute(
        datestamp=date.today().isoformat(),
        )

    with codecs.open(tex_filename, "w", encoding="utf-8") as f:
        f.write(make_main_file(single_sheets, data))

    for i in range(data["num_pdflatex_runs"]):
        print("Running pdflatex ({:d}/{:d})...".format(
            i + 1,
            data["num_pdflatex_runs"],
            ))
        run_pdflatex(".", tex_filename)

    clean_temp_files()


def clean_temp_files():
    temp_file_extensions = [
        r"\.aux",
        r"\.out",
        r"\.log",
        r"\.synctex\.gz",
        r"\.preview\.pdf",
        ]
    temp_files_pattern = "({:s})$".format("|".join(temp_file_extensions))
    for f in os.listdir("."):
        if re.search(temp_files_pattern, f):
            os.remove(os.path.join(".", f))


if __name__ == "__main__":
    create_tally_sheets(sys.argv[1])
