from config import RAW_DATA_PATH
import os


def main():

    print("Waymark Data Engineering Pipeline")

    print("Reading files from:")

    print(RAW_DATA_PATH)

    files = os.listdir(RAW_DATA_PATH)

    print("\nAvailable Files")

    for file in files:
        print(file)


if __name__ == "__main__":
    main()