from pydantic import BaseModel


class DictEntry(BaseModel):
    spelling: str
    transcription: str | None = None
    definition: str
    examples: list[str] = []
