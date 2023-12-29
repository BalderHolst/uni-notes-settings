#!/usr/bin/env python

import os
import sys

IGNORED = [
    ".git",
    ".obsidian",
    "External",
    "Excalidraw",
    ".trash"
]

def handle_file(path: str):
    print(path)

def search_dir(dir):

    for entry in os.listdir(dir):
        if entry in IGNORED: continue

        entry = f"{dir}/{entry}"

        if os.path.isdir(entry):
            search_dir(entry)
        elif os.path.isfile(entry):
            handle_file(entry)


if __name__ == "__main__":
    search_dir("../..")
