from pathlib import Path
import os
import sys

def main():
    args = [f'"{i}"' if len(i.split()) > 1 else i for i in sys.argv[1:]]
    os.system(f"pytest {' '.join(args)} {Path(__file__).parent}")

if __name__ == "__main__":
    main()
