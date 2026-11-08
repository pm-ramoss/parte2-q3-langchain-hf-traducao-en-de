from pydantic import BaseModel, Field


class TranslateRequest(BaseModel):
    text: str = Field(..., min_length=1, max_length=5000, examples=["The weather is nice today."])


class TranslateResponse(BaseModel):
    original_text: str
    translated_text: str
    source_language: str = "en"
    target_language: str = "de"
    model: str
