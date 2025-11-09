from pydantic import BaseModel


class DictEntry(BaseModel):
    spelling: str
    transcription: str = ""
    definition: str
    examples: list[str] = []
