"""This is the main entrypoint of the application."""
from typing import List, Any, Optional
import getopt
import sys


def main(args: Optional[List[Any]] = None) -> None:
    opts, args = getopt.getopt(sys.argv[1:], "h", ["help"])
    for opt, arg in opts:
        if opt == "-h":
            print(sys.argv[0], "[]")
            print("  -h          Display this help message")
            sys.exit()

    from anathema.main import main  # type: ignore
    main()
    sys.exit()


if __name__ == '__main__':
    main()
