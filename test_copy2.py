import os
import time
import threading

# --- Konfigurasjon ---
FILE_SIZE_MB = 1000
SOURCE_FILE = "testfile.dat"

# Sett disse til faktiske steder på din maskin:
HDD_PATH = "/Volumes/Untitled/ssd_test.dat"
SSD_PATH = "/Volumes/Lenovo PS8/hdd_test.dat"


def generate_random_file(filename, size_mb):
    """Lager en fil på gitt størrelse (MB) med tilfeldige data."""
    print(f"Lager testfil på {size_mb} MB...")
    with open(filename, "wb") as f:
        for _ in range(size_mb):
            f.write(os.urandom(1024 * 1024))  # 1 MB per loop
    print("Testfil ferdig.")


def copy_file(src, dst, label, results):
    """Kopierer filen og måler tid."""
    os.makedirs(os.path.dirname(dst), exist_ok=True)  # lag mappe hvis ikke finnes

    start_time = time.time()
    with open(src, "rb") as fsrc, open(dst, "wb") as fdst:
        while chunk := fsrc.read(1024 * 1024):  # 1 MB per chunk
            fdst.write(chunk)
    elapsed = time.time() - start_time
    results[label] = elapsed
    print(f"{label} ferdig: {elapsed:.2f} sekunder")


def cleanup(files):
    """Sletter filer etter bruk."""
    for f in files:
        try:
            if os.path.exists(f):
                os.remove(f)
        except Exception as e:
            print(f"Kunne ikke slette {f}: {e}")


def main():
    # Lag testfil
    generate_random_file(SOURCE_FILE, FILE_SIZE_MB)

    results = {}

    print("Starter kopiering samtidig...")
    t1 = threading.Thread(target=copy_file, args=(SOURCE_FILE, SSD_PATH, "SSD", results))
    t2 = threading.Thread(target=copy_file, args=(SOURCE_FILE, HDD_PATH, "HDD", results))

    t1.start()
    t2.start()
    t1.join()
    t2.join()

    print("\n--- Resultater ---")
    if "SSD" in results:
        print(f"SSD tid: {results['SSD']:.2f} sekunder")
    if "HDD" in results:
        print(f"HDD tid: {results['HDD']:.2f} sekunder")

    if "SSD" in results and "HDD" in results:
        total = max(results["SSD"], results["HDD"])
        print(f"Total tid brukt (parallelt): {total:.2f} sekunder")

    # Rydd opp
    cleanup([SOURCE_FILE, SSD_PATH, HDD_PATH])


if __name__ == "__main__":
    main()