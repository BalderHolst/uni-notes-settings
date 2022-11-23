from scrape_formulas import * 
from get_file_tags import get_file_tags


def create_formelsamling(vault: Path, out_dir: Path):
    formelsamlinger = {
        "matematik": [],
        "fysik": [],
        "elektronik": [],
        }

    formulas = parse_vault(vault, verbose=True)

    last_title = None
    last_file = None

    for formula in formulas:
        formula_lines = []

        new_title = formula['title'] != last_title
        new_file = formula['file'] != last_file

        last_title = formula['title']
        last_file = formula['file']

        source_name = Path(formula['file']).stem

        if new_file:
            formula_lines.append(f"## {source_name} ([[{source_name}|link]])")

        if new_title and formula['title'] != source_name:
            formula_lines.append(f"\n#### {formula['title']}")
            formula_lines.append(f"Se [[{source_name}#" + re.sub(r'[\[\]]', '',formula['title']) + "]].")


        formula_lines.append(f"\n$${formula['formula']}$$\n")

        for symbol in formula['symbols']:
            formula_lines.append(f"${symbol['symbol']}$ : {symbol['description']}")

        # Føj linjer til de formelsamlinger de hører til.
        for tag in get_file_tags(vault / formula['file']):
            if tag in formelsamlinger:
                if new_file:
                    formelsamlinger[tag].append("\n".join(formula_lines))
                else:
                    formelsamlinger[tag][-1] = formelsamlinger[tag][-1] + "\n".join(formula_lines)
            else:
                print(f"Ignoring tag: {tag!r}")




    if not out_dir.is_absolute():
        out_dir = vault / out_dir


    for subject, lines in formelsamlinger.items():
        lines = "\n\n---\n\n".join(lines)
        out_file = out_dir / f"{subject}.md"

        print(f"Saving to {out_file}...", end=" ")

        with out_file.open("w") as f:
            f.writelines(lines)

        print("done.")



if __name__ == "__main__":
    vault = Path.home() / "Documents/uni/noter"

    create_formelsamling(vault, Path("formelsamling"))

