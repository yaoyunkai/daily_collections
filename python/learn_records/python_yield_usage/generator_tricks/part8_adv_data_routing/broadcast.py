def broadcast(source, consumers):
    for item in source:
        for c in consumers:
            c.send(item)
