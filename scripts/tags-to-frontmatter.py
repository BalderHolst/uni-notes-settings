import ovault

vault = ovault.Vault(".")

W = 25

for note in sorted(vault.notes()):
    tokens = [t for t in note.tokens() if not t.is_whitespace() ]

    tags = []
    new_end = None

    for token in reversed(tokens):
        match token:
            case token.Tag():
                tags.append(token.tag)
            case token.Divider():
                new_end = token.span.start
            case other:
                if new_end != None:
                    new_end = other.span.end
                break

    if new_end == None:
        continue


    print(note.name.strip(), " " * (W - len(note.name)), tags)

    text = note.read()


    note.write(text[:new_end])

    f = note.frontmatter()
    if f == None: f = ovault.Frontmatter()
    f.set("tags", tags)
    note.set_frontmatter(f)


