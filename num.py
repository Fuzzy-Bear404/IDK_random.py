# generate_filenames.py
def generate_filenames(out_file="filenames.txt"):
    with open(out_file, "w", encoding="utf-8") as f:
        for n in range(0, 10_000_000):
            f.write(f"{n:07d}_1\n")

if __name__ == "__main__":
    generate_filenames()
