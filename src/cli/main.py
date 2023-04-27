import argparse

from request import Request

parser = argparse.ArgumentParser()
parser.add_argument("commands", nargs="+")

args = parser.parse_args()


def main():
    response = Request(*args.commands)()


if __name__ == "__main__":
    main()
