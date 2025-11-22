from pathlib import Path
from src.settings.config import Config
from src.services import base
from src.services.base import create_anki_note, clear_terminal
from questionary import checkbox
from src.dictionaries import cambridge_dict
from src.models.dict_entry import DictEntry


def get_word_entries(word: str) -> list[DictEntry]:
    """
    Fetch word entries (definitions + examples) from Cambridge dictionary.
    """
    word = word.strip()
    if not word:
        return []

    entries: list[DictEntry] = cambridge_dict.get_word_entry(word)
    if not entries:
        print(f"Word '{word}' not found. Skipping.\n")
    return entries


def select_definitions(entries: list[DictEntry]) -> list[DictEntry]:
    """
    Let the user select definitions for a word.
    Returns the selected entries.
    """
    if not entries:
        return []

    print()
    selected_defs = checkbox(
        f"SELECT DEFINITIONS FOR '{entries[0].spelling.upper()}'\n\n",
        choices=[e.definition for e in entries],
    ).ask()

    if not selected_defs:
        return []

    return [e for e in entries if e.definition in selected_defs]


def select_examples(entry: DictEntry) -> DictEntry:
    """
    Let the user select examples for a given entry.
    Updates the entry.examples list.
    """

    print()
    if entry.examples:
        selected_examples = checkbox(
            f"'{entry.spelling.upper()}' — {entry.definition.upper()}\n\n",
            choices=entry.examples,
        ).ask()
        entry.examples = selected_examples or []
    else:
        entry.examples = []
    return entry


def process_words(words: list[str]) -> list:
    """
    Process a list of words: fetch entries, select definitions and examples,
    and create Anki notes.
    """
    all_notes = []

    for word in words:
        entries = get_word_entries(word)
        if not entries:
            continue

        selected_entries = select_definitions(entries)
        if not selected_entries:
            continue


        for entry in selected_entries:
            entry = select_examples(entry)
            note = create_anki_note(entry.spelling, entry.definition, entry.examples, entry.transcription)
            all_notes.append(note)
        
        clear_terminal()

    return all_notes


def update_env_file(path: str, deck: str):
    """Write or update EN_TO_EN_PATH and EN_TO_EN_DECK in .env."""
    env_path = Path(__file__).resolve().parent.parent / "settings" / ".env"
    env_lines = []
    if env_path.exists():
        env_lines = env_path.read_text(encoding="utf-8").splitlines()

    # Remove old lines for these keys
    env_lines = [
        line
        for line in env_lines
        if not line.startswith("EN_TO_EN_PATH=")
        and not line.startswith("EN_TO_EN_DECK=")
    ]

    # Add updated values
    env_lines.append(f"EN_TO_EN_PATH={path}")
    env_lines.append(f"EN_TO_EN_DECK={deck}")

    env_path.write_text("\n".join(env_lines) + "\n", encoding="utf-8")
    print(f"[INFO] Updated .env at {env_path}")


def resolve_config(path: str | None = None, deck: str | None = None) -> tuple[str, str]:
    """Resolve path & deck: CLI args > .env > defaults."""
    config = Config.load()
    resolved_path = path or config.en_to_en.PATH or ""
    resolved_deck = deck or config.en_to_en.DECK or "Autodeck"

    if not resolved_path:
        raise ValueError("No path specified and none found in .env")

    update_env_file(resolved_path, resolved_deck)
    return resolved_path, resolved_deck


def run(words: list[str], path: str | None = None, deck: str | None = None):
    """
    Full workflow: resolve config, process words, create & save Anki deck.
    """
    path, deck = resolve_config(path, deck)
    notes = process_words(words)

    if not notes:
        print("No notes were created. Exiting.")
        return

    deck_obj = base.create_anki_deck(deck, notes)
    base.save_deck(path, deck_obj)
    print(f"[INFO] Deck saved successfully to {path}")

