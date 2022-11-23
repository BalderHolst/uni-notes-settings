from pathlib import Path
import re
import json

ignore_headers = [
        "Formler", 
        "Løsningsformlen", 
        "Alternative", 
        "Løsning",
        "Løsninger",
        "Forskrift"
        ]

# Dette er en regex
void_headers = [
        "Bevis",
        "Eksempel"
        ]


def parse_file(file: Path | str) -> list[dict]:
    if isinstance(file, str):
        file = Path(file)

    formulas = []

    def is_header(string):
        if re.search(r"^#+ .+", string):
            return True
        return False
    
    def is_symbol_def(string):
        if re.search(r"^\$.+\$ ?: ?", string):
            return(True)
        return(False)
    
    def extract_header(line):
        return(re.sub(r"^#+ ", r"", line).replace("\n", ""))
    
    def line_to_symbol_dict(line):
        parts = line.split(":") # Split symbol and description
        desc = re.sub("^ ?", "", parts[1]) # Delete leading space if any
        return({
            "symbol": re.sub("^\$?(.+)\$ ?$", r"\1" , parts[0].replace("\s", "")), # Delete whitespace
                "description": desc.replace("\n", "")
                })

    
    with file.open() as f:
        lines = f.readlines()

    for line_nr, line in enumerate(lines):
        m = re.search(r"\$\$.+\$\$", line)

        if m:
            title = None
            symbols = []

            formula = m.group()[2:-2]

            # Scan lines after for symbol descriptors
            for after_line in lines[line_nr:]:
                if is_symbol_def(after_line):
                    symbols.append(line_to_symbol_dict(after_line))
                    continue
                if is_header(after_line) and not extract_header(after_line) in ignore_headers:
                    break

            # Scan previous lines for formula title
            for i in range(line_nr, -1, -1):
                if is_header(lines[i]): # Check if line is a header
                    title = extract_header(lines[i])
                    if title in ignore_headers:
                        title = None
                    else:
                        break
                elif(is_symbol_def(lines[i])):
                    symbol = line_to_symbol_dict(lines[i])

                    # if the symbol is part of the formula, but not already a definded symbol (sammenligner uden mellemrum)
                    if symbol['symbol'].replace(' ','') in formula.replace(' ','') and symbol['symbol'].replace(' ','') not in [s['symbol'].replace(' ','') for s in symbols]:
                        symbols.append(symbol)


            formula = {
                "file": str(file),
                "title": title,
                "formula": formula,
                "symbols": symbols
                }

            if formula['title'] in void_headers:
                continue

            formulas.append(formula)
    return(formulas)
        

def parse_vault(vault: Path, verbose=False, source_vault=None):

    excluded_dirs = [
            ".obsidian",
            ".git",
            "formelsamling"
            ]

    if source_vault is None:
        source_vault = vault

    formulas = []
    for file in vault.iterdir():
        
        if file.is_dir() and not str(file.relative_to(vault)) in excluded_dirs:
            if verbose:
                print(f"found dir: {file}")
            formulas += parse_vault(file, verbose=verbose, source_vault=source_vault)
            continue
        elif file.suffix != ".md":
            continue
        
        if verbose:
            print(f"parsing file: {file.name!r}", end="")

        file_formulas = parse_file(file)
        
        if verbose:
            print(f" -> found {len(file_formulas)}")

        formulas.extend(file_formulas)

    # change paths to be relative
    for n, formula in enumerate(formulas):
        full_path = Path(formula['file'])
        if full_path.is_absolute():
            formulas[n]['file'] = str(full_path.relative_to(source_vault))
            print(formulas[n]['file'] )



    return(formulas)

def scrape_to(vault: Path, json_path: Path | str, verbose=False):
    with open(str(json_path), 'w') as f:
        json.dump(parse_vault(vault, verbose=verbose), f, indent=4)

if __name__ == "__main__":
    vault = Path.home() / "Documents/uni/noter"
    scrape_to(vault, "formulas.json", verbose=False)
    # for formula in parse_file("/home/Balder/Documents/uni/noter/Newtons Afkølingslov.md"):
    #     print(f"{formula['title']}: '{formula['formula']}'")
    #     for symbol in formula['symbols']:
    #         print("\t" + str(symbol['symbol']) + "  --  " + str(symbol['description']))
    

