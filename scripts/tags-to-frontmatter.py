import ovault

vault = ovault.Vault(".")

for note in sorted(vault.notes())[:10]:
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

    text = note.read()

    print(text[:new_end])
    print("------")

