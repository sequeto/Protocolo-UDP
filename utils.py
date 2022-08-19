def breakChunks(file_path,BUFFER):
    packages = []
    sequence_number = 1

    with open(file_path, "rb") as f:
        while True:
            if(sequence_number == 256):
                sequence_number = 1
            data = f.read(BUFFER)
            if not data: break
            packages.append({
                "data": data,
                "seq_number": sequence_number
            })
            # sequence_number = sequence_number + (len(data));
            sequence_number = sequence_number + 1;

    return packages