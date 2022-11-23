import re
from pathlib import Path

def get_file_tags(path) ->  list:
    tags = []

    lines = None

    with open(path, 'r') as f:
        lines = f.readlines()

    for line in lines:
        line = line.replace("\n", "")
        m = re.search(r"^#(\w+)", line)
        if m:
            tags.append(m.group(1))
    return(tags)

if __name__ == "__main__":
    print(get_file_tags(Path("/home/Balder/Documents/uni/noter/notes/Gnidning.md")))
