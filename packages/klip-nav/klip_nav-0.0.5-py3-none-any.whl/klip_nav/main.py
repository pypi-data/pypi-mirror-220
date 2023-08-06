from klip_nav.tui import App
from klip_nav.utils import SortedClippings
import argparse


def main():
    parser = argparse.ArgumentParser(
        prog="klip-nav", description="TUI for kindle clippings"
    )
    parser.add_argument("clippings_file")
    args = parser.parse_args()
    App(
        clippings=SortedClippings(args.clippings_file),
        filename=args.clippings_file,
    )


if __name__ == "__main__":
    main()
