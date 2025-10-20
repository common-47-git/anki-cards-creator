import argparse
from src.services import en_to_en


def main():
    parser = argparse.ArgumentParser(
        description="A script to make simple Anki word cards."
    )
    parser.add_argument("words", nargs="+", help="List the words separated by spaces.")
    parser.add_argument(
        "--path",
        type=str,
        required=False,
        help="Path to save the Anki deck (optional if defined in .env).",
    )
    parser.add_argument(
        "--deck",
        type=str,
        required=False,
        help="Name of an Anki deck (optional if defined in .env).",
    )
    args = parser.parse_args()

    en_to_en.run(args.words, args.path, args.deck)


if __name__ == "__main__":
    main()
