# This file is designed to be run from inside the vault directory

import sys
sys.path.insert(0, '.obsidian/scripts/image-download')

from image_download import download_image
from pathlib import Path
import re

vault = Path()
notes_dir = vault / "notes"
attachment_dir = vault / "auto-attached"

# def download_image(url):
#     filename = re.sub("[^ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789\.=]", "_", url)

def localize(file: Path):
    with file.open() as f:
        lines = f.readlines()

    for line in lines:
        m = re.search(r"!\[(.+)\]\((.+)\)", line)
        if m:
            print(m.group())
            desc = m.group(1)
            url = m.group(2)
            path = download_image(url, attachment_dir)

if __name__ == "__main__":
    if not attachment_dir.exists():
        attachment_dir.mkdir()

    for note in notes_dir.iterdir():
        localize(note)


