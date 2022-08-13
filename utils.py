def breakChunks(file_path,BUFFER):
    packages = []
    with open(file_path, "rb") as f:
        while True:
            data = f.read(BUFFER)
            if not data: break
            packages.append(data)
    print(packages)

    return packages
