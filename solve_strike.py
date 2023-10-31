import sys
from algorithms.offline import offline
from algorithms.strike import Instance


def main():
    if len(sys.argv) != 2:
        print("Usage: python3 offline.py <instance>")
        sys.exit(1)
    I = Instance.from_file(f"input/{sys.argv[1]}")
    for flying, staying in offline(I):
        print(f"{flying}, {staying}")

if __name__ == '__main__':
    main()
