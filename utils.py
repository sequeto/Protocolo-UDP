def breakChunks(file_path,BUFFER):
    packages = []
    sequence_number = 0

    with open(file_path, "rb") as f:
        while True:
            data = f.read(BUFFER)
            if not data: break
            packages.append({
                "data": data,
                "seq_number": sequence_number
            })
            # sequence_number = sequence_number + (len(data));
            sequence_number = sequence_number + 1;

    return packages