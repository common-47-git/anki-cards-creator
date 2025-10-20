from pydantic import BaseModel


class DictEntry(BaseModel):
    spelling: str
    definition: str
    examples: list[str] = []
