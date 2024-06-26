#!/usr/bin/env python

import os
import datetime
import subprocess

IGNORED = [
    ".git",
    ".obsidian",
    "External",
    "Excalidraw",
    ".trash" ]

global update_count
update_count = 0

def get_file_modified(path: str):
    if not os.path.exists(path): return datetime.datetime(2000, 1, 1)

    time_stamp = os.path.getatime(path)
    return datetime.datetime.fromtimestamp(time_stamp)

def handle_file(path: str):
    parts = path.split('.')
    ext = parts[-1]

    if ext != "xopp": return

    source_file = path
    pdf_file = ".".join(parts[:-1]) + ".pdf"

    source_modified_time = get_file_modified(source_file);
    pdf_modified_time = get_file_modified(pdf_file);

    is_outdated = source_modified_time-pdf_modified_time > datetime.timedelta(0)

    if not is_outdated: return

    global update_count
    update_count += 1

    cmd = f"xournalpp -p \"{pdf_file}\" \"{source_file}\" 2> /dev/null"
    subprocess.run(cmd, shell=True)


def search_dir(dir):

    for entry in os.listdir(dir):
        if entry in IGNORED: continue

        entry = f"{dir}/{entry}"

        if os.path.isdir(entry):
            search_dir(entry)
        elif os.path.isfile(entry):
            handle_file(entry)


if __name__ == "__main__":
    search_dir(".")

    if update_count != 0:
        s = f"Updated {update_count} Xournal++ Documents!"
        if update_count == 1: s = s[:-2] + "!"
        print(s)
