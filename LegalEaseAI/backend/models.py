from typing import Literal

from pydantic import BaseModel, Field, field_validator


class DocumentRequest(BaseModel):

    document_type: str = Field(
        ...,
        min_length=2,
        max_length=120
    )

    parties: str = Field(
        ...,
        min_length=2,
        max_length=4000
    )

    terms: str = Field(
        ...,
        min_length=2,
        max_length=10000
    )

    dates: str = Field(
        ...,
        min_length=2,
        max_length=200
    )

    jurisdiction: str = Field(
        default="Not specified",
        max_length=200
    )

    language: str = Field(
        default="English",
        max_length=80
    )

    brand_name: str = Field(
        default="LegalEase",
        max_length=120
    )

    @field_validator(
        "document_type",
        "parties",
        "terms",
        "dates",
        "jurisdiction",
        "language",
        "brand_name"
    )
    @classmethod
    def strip_values(cls, value: str) -> str:

        value = value.strip()

        if not value:
            raise ValueError(
                "Value cannot be empty"
            )

        return value


class GenerateResponse(BaseModel):

    document_type: str

    text: str

    model: str


class ExportRequest(BaseModel):

    document_type: str = Field(
        ...,
        min_length=2,
        max_length=120
    )

    text: str = Field(
        ...,
        min_length=1,
        max_length=100000
    )

    format: Literal[
        "txt",
        "docx",
        "pdf"
    ]

    terms: list[str] = Field(
        default_factory=list,
        max_length=100
    )

    brand_name: str = Field(
        default="LegalEase",
        max_length=120
    )