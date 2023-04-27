import argparse

from mana_client import ManaClient

parser = argparse.ArgumentParser()
parser.add_argument("commands", nargs="+")

args = parser.parse_args()


def main():
    ManaClient()(*args.commands)


if __name__ == "__main__":
    main()
