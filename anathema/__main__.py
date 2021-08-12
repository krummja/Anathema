"""
This is the main entrypoint of the application.
The game's `main` is in `start.py`.

Use command line opt -h to list running options.
"""
from typing import List, Any, Optional
import getopt
import sys


def main(_args: Optional[List[Any]] = None) -> None:
    opts, args = getopt.getopt(sys.argv[1:], "h", ["help"])
    for opt, arg in opts:
        if opt == "-h":
            print(sys.argv[0], "[]")
            print("  -h          Display this help message")
            sys.exit()

    from anathema.start import start  # type: ignore
    start()
    sys.exit()


if __name__ == '__main__':
    main()
