import sys

from .host import main


def entry():
    main(sys.argv[1:])
