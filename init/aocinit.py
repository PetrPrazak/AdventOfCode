# Advent of code working directories creator
# IMPORTANT Remember to edit the USER_SESSION_ID & author values with yours
# uses requests module. If not present use pip install requests
# Author = Alexe Simon
# Date = 06/12/2018
# original code at https://github.com/AlexeSimon/adventofcode
import datetime
import os
import sys
import re
import pathlib
# USER SPECIFIC PARAMETERS
# Folders will be created here. If you want to make a parent folder, change this to ex "./adventofcode/"
base_pos = "../"
# Get your session by inspecting the session cookie content in your web browser while connected to adventofcode and paste it here as plain text in between the ". Leave at is to not download inputs.
USER_SESSION_ID = ""
# Set to false to not download statements. Note that only part one is downloaded (since you need to complete it to access part two)
DOWNLOAD_STATEMENTS = True
# if set to True the script will try to convert the puzzle text to the Markdown
CONVERT_TO_MD = True
# Set to false to not download inputs. Note that if the USER_SESSION_ID is wrong or left empty, inputs will not be downloaded.
DOWNLOAD_INPUTS = True
# Set to false to not make code templates. Note that even if OVERWRITE is set to True, it will never overwrite codes.
MAKE_CODE_TEMPLATE = True
# Set to false to not create a direct url link in the folder.
MAKE_URL = False
# If you really need to download the whole thing again, set this to true. As the creator said, AoC is fragile; please be gentle. Statements and Inputs do not change. This will not overwrite codes.
OVERWRITE = False

# DATE SPECIFIC PARAMETERS
starting_advent_of_code_year = 2021  # You can go as early as 2015.
# The setup will download all advent of code data up until that date included
last_advent_of_code_year = 2021
# If the year isn't finished, the setup will download days up until that day included for the last year
last_advent_of_code_day = 7
# Imports
try:
    import requests
except ImportError:
    sys.exit("You need requests module. Install it by running pip install requests.")

try:
    from md import markdownify as md, ATX
except ImportError:
    md = lambda t, *args, **kwargs: t
    CONVERT_TO_MD = False

# Code
MAX_RECONNECT_ATTEMPT = 2
years = range(starting_advent_of_code_year, last_advent_of_code_year+1)
days = range(last_advent_of_code_day, 26)
# ex use : https://adventofcode.com/2017/day/19/input
aoc_link = "https://adventofcode.com/"
USER_AGENT = "adventofcode_working_directories_creator"
session_id = os.environ.get('AOC_SESSION_ID', None) or USER_SESSION_ID
py_template = ""

def get_template():
    global py_template
    if py_template:
        return py_template
    file = str(pathlib.Path(__file__).resolve().parent) + "/template.py"
    with open(file) as templ:
        py_template = templ.read()
        return py_template
    py_template = "# AOC {year}/{day}"
    return py_template


def template(year, day):
    link = aoc_link
    return get_template().format(**locals())


def md_header(y,d):
    return f"""# Day {d}
Copyright (c) Eric Wastl
#### [Source](https://adventofcode.com/{y}/day/{d})

## Part 1
"""

def make_md(text):
    text = re.sub(r"(<code>)(<em>)",r"\2\1", text)
    text = re.sub(r"(</em>)(</code>)",r"\2\1", text)
    return md(text, heading_style=ATX)


print("Setup will download data and create working directories and files for adventofcode.")
if not os.path.exists(base_pos):
    os.mkdir(base_pos)
for y in years:
    print(f"Year {y}")
    str_y = str(y)
    year_pos = base_pos + str_y
    if not os.path.exists(year_pos):
        os.mkdir(year_pos)
    for d in (d for d in days if (y < last_advent_of_code_year or d <= last_advent_of_code_day)):
        str_d = str(d)
        print(f"    Day {d}")
        day_pos = f"{year_pos}/{d:02}"
        if not os.path.exists(day_pos):
            os.mkdir(day_pos)

        template_file = f"{day_pos}/aoc{y}_{d:02}.py"
        if MAKE_CODE_TEMPLATE and not os.path.exists(template_file):
            with open(template_file, "w+") as code:
                code.write(template(y, d))

        day_link = f"{aoc_link}{y}/day/{d}"
        if DOWNLOAD_INPUTS and (not os.path.exists(day_pos+"/input.txt") or OVERWRITE) and session_id:
            done = False
            error_count = 0
            while not done:
                try:
                    with requests.get(url=day_link+"/input", cookies={"session": session_id}, headers={"User-Agent": USER_AGENT}) as response:
                        if response.ok:
                            data = response.text
                            with open(day_pos+"/input.txt", "w+") as input:
                                input.write(data.rstrip("\n"))
                            with open(day_pos+"/test.txt", "w+") as test:
                                test.write("\n")
                        else:
                            print("        Server response for input is not valid.")
                    done = True
                except requests.exceptions.RequestException:
                    error_count += 1
                    if error_count > MAX_RECONNECT_ATTEMPT:
                        print("        Giving up.")
                        done = True
                    elif error_count == 0:
                        print("        Error while requesting input from server. Request probably timed out. Trying again.\r", end="")
                    else:
                        print("        Trying again.\r", end="")
                except Exception as e:
                    print("        Non handled error while requesting input from server.", e)
                    done = True

        readme_path = day_pos+ ("/README.md" if CONVERT_TO_MD else "/statement.html")
        if DOWNLOAD_STATEMENTS and (not os.path.exists(readme_path) or OVERWRITE):
            done = False
            error_count = 0
            while not done:
                try:
                    with requests.get(url=day_link, cookies={"session": session_id}, headers={"User-Agent": USER_AGENT}) as response:
                        if response.ok:
                            html = response.text
                            start = html.find("<article")
                            end = html.rfind("</article>")+len("</article>")
                            end_success = html.rfind("<p class=\"day-success\">")
                            text = html[start:max(end, end_success)]
                            if CONVERT_TO_MD:
                                text = make_md(text)
                            with open(readme_path, "w+") as statement:
                                if CONVERT_TO_MD:
                                    statement.write(md_header(y,d))
                                statement.write(text)
                        done = True
                except requests.exceptions.RequestException:
                    error_count += 1
                    if error_count > MAX_RECONNECT_ATTEMPT:
                        print("        Error while requesting statement from server. Request probably timed out. Giving up.")
                        done = True
                    else:
                        print("        Error while requesting statement from server. Request probably timed out. Trying again.\r", end="")
                except Exception as e:
                    print("        Non handled error while requesting statement from server. " + str(e))
                    done = True

        linkurl_path = day_pos+"/link.url"
        if MAKE_URL and (not os.path.exists(linkurl_path) or OVERWRITE):
            with open(linkurl_path, "w+") as url:
                url.write(f"[InternetShortcut]\nURL={day_link}\n")

print("Setup complete : adventofcode working directories and files initialized with success.")
