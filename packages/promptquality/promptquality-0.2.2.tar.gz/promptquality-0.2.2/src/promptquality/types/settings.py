from typing import List, Optional

from pydantic import BaseModel, ConfigDict


class Settings(BaseModel):
    """
    Settings for a prompt run that a user can configure.
    """

    model_alias: Optional[str]
    temperature: Optional[float]
    max_tokens: Optional[int]
    stop_sequences: Optional[List[str]]

    top_p: Optional[int]
    frequency_penalty: Optional[float]
    presence_penalty: Optional[float]

    model_config = ConfigDict(protected_namespaces=())
