import re
from pathlib import Path
from sys import dont_write_bytecode

notes_dir = Path("notes").absolute()
# out_dir = Path("test_notes")
out_dir = notes_dir


for file in notes_dir.iterdir():

    file_dropdowns = []

    
    with file.open() as f:
        lines = f.readlines()
    

    in_dropdown = False

    dropdown_start = None
    dropdown_title = None
    dropdown_lines = []

    for line_nr, line in enumerate(lines):
        m = re.search(r"^```ad-example", line)

        
        if m:
            in_dropdown = True
            dropdown_start = line_nr
            dropdown_lines = []

        elif in_dropdown:
            if re.search(r"^```", line):
                in_dropdown = False
                file_dropdowns.append({
                    "title": dropdown_title,
                    "start_line": dropdown_start,
                    "end_line": line_nr,
                    "lines": dropdown_lines
                    })
                print(file_dropdowns[-1])
                print(f"Reached end of dropdown {dropdown_title!r}")
                continue
            elif re.search(r"^collapse", line):
                continue
            m = re.search(r"^title:\s+(.+)$", line)
            if m:
                dropdown_title = m.group(1)
                print(f"\nFound title: {dropdown_title!r} in file: {file.name!r}")
                continue
            
            dropdown_lines.append(">" + line)

    def create_title(title):
        return(f"\n>[!Note]- {title}\n")

    file_dropdowns.reverse()
        
    for dropdown in file_dropdowns:
        lines = lines[:dropdown['start_line']] + [create_title(dropdown['title'])] + dropdown['lines'] + lines[dropdown["end_line"] + 1:]



    new_file = out_dir / file.name

    with new_file.open('w') as f:
        f.writelines(lines)





