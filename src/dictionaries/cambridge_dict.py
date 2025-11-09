import requests
from bs4 import BeautifulSoup as BS
from src.models.dict_entry import DictEntry

CAMBRIDGE_URL = "https://dictionary.cambridge.org/dictionary/english/{word}"


def _fetch_html(word_spelling: str) -> str | None:
    """
    Fetch the HTML content of a Cambridge Dictionary page for a given word.
    Returns the HTML text or None if the request fails.
    """
    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/91.0.4472.124 Safari/537.36"
        )
    }
    url = CAMBRIDGE_URL.format(word=word_spelling)

    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        return response.text
    except requests.exceptions.RequestException as e:
        print(f"No access to the dictionary: {e}")
        return None


def _parse_definitions(soup: BS) -> list:
    """
    Extract definition blocks from the parsed HTML.
    Each block represents one meaning of the word.
    """
    return soup.find_all("div", class_="ddef_h")


def _extract_definition_text(definition_block) -> str | None:
    """
    Extract and clean the definition text from a definition block.
    """
    definition_div = definition_block.find("div", class_="def ddef_d db")
    if not definition_div:
        return None

    definition_text = (
        " ".join(definition_div.get_text(separator=" ").split())
        .replace(":", "")
        .strip()
    )
    return definition_text


def _extract_examples(definition_block) -> list[str]:
    """
    Extract example sentences following a definition block.
    """
    examples = []
    def_body = definition_block.find_next_sibling("div", class_="def-body ddef_b")
    if not def_body:
        return examples

    example_divs = def_body.find_all("div", class_="examp dexamp")
    for div in example_divs:
        text = " ".join(div.get_text(separator=" ").split()).strip()
        if text:
            examples.append(text)
    return examples


def _get_first_us_transcription(soup: BS) -> str | None:
    """
    Get the first US IPA transcription on the page.
    Returns None if not found.
    """
    us_block = soup.find("span", class_="us dpron-i")
    if not us_block:
        return None

    ipa_span = us_block.find("span", class_="ipa")
    return ipa_span.get_text(strip=True) if ipa_span else None


def _build_dict_entries(word_spelling: str, definition_blocks: list, transcription: str | None) -> list[DictEntry]:
    """
    Build DictEntry objects from definition blocks.
    Avoid duplicate definitions.
    Use the same transcription for all definitions (first US IPA found).
    """
    entries: list[DictEntry] = []
    seen_definitions = set()

    for block in definition_blocks:
        definition_text = _extract_definition_text(block)
        if not definition_text or definition_text in seen_definitions:
            continue

        seen_definitions.add(definition_text)

        examples = _extract_examples(block)

        entries.append(
            DictEntry(
                spelling=word_spelling,
                transcription=transcription or "", 
                definition=definition_text,
                examples=examples,
            )
        )

    return entries


def get_word_entry(word_spelling: str) -> list[DictEntry]:
    """
    Fetch word entries (definitions + example sentences + first US transcription)
    from Cambridge Dictionary.
    """
    html = _fetch_html(word_spelling)
    if not html:
        return []

    soup = BS(html, "lxml")

    definition_blocks = _parse_definitions(soup)
    if not definition_blocks:
        print(f"Word '{word_spelling}' not found, make sure you wrote it right.")
        return []

    transcription = _get_first_us_transcription(soup)

    return _build_dict_entries(word_spelling, definition_blocks, transcription)
