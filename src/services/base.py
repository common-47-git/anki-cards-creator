import os
import genanki
from datetime import date
from src.anki_note_types.word_card import word_card_model
import logging


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger(__name__)


def create_anki_note(word: str, definition: str, examples: list[str], transcription: str | None = None) -> genanki.Note:
    """
    Create a genanki.Note from a word, definition, and examples.
    Converts the examples list into HTML line breaks for Anki.
    """
    examples_text = "<br>".join(examples) if examples else ""
    return genanki.Note(model=word_card_model, fields=[word, transcription, definition, examples_text])


def create_anki_deck(
    name: str, notes: list[genanki.Note], deck_id: int = 1234567890
) -> genanki.Deck:
    """
    Create an Anki deck with the given notes.
    """
    deck = genanki.Deck(deck_id, name)
    for note in notes:
        deck.add_note(note)
    return deck


def save_deck(path: str, deck: genanki.Deck) -> None:
    """
    Save the Anki deck to the specified directory as a .apkg file.
    The filename will include the current date.
    """
    today = date.today()

    if not os.path.isdir(path):
        logger.error("Directory does not exist: %s", path)
        return

    final_file = os.path.join(path, f"anki_question_{today}.apkg")

    try:
        genanki.Package(deck).write_to_file(final_file)
        logger.info("Deck saved successfully: %s", final_file)
    except Exception as e:
        logger.exception("Failed to save deck: %s", e)


def clear_terminal():
    # For Windows
    if os.name == 'nt':
        _ = os.system('cls')
    # For macOS and Linux
    else:
        _ = os.system('clear')

