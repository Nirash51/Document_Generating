from google import genai
from google.genai import types

from backend.config import get_settings


class GeminiConfigurationError(RuntimeError):
    pass


class GeminiGenerationError(RuntimeError):
    pass


class GeminiDocumentGenerator:

    def __init__(self):

        self.settings = get_settings()

        if not self.settings.gemini_api_key:

            raise GeminiConfigurationError(
                "GEMINI_API_KEY is not configured. "
                "Create a .env file and add your Gemini API key."
            )

        self.client = genai.Client(
            api_key=self.settings.gemini_api_key
        )

    @staticmethod
    def _build_prompt(
        document_type: str,
        parties: str,
        terms: str,
        dates: str,
        jurisdiction: str,
        language: str,
    ) -> str:

        prompt = f"""
You are LegalEase, an AI-assisted legal document drafting system.

Your task is to create a professional DRAFT legal document.

IMPORTANT SAFETY AND ACCURACY RULES:

1. This is drafting assistance and not legal advice.
2. Do not claim that the document is legally valid in every jurisdiction.
3. Do not invent personal information.
4. Do not invent signatures.
5. Do not invent registration numbers.
6. Do not invent statutes or case citations.
7. Preserve all names, dates, amounts and obligations supplied by the user.
8. Do not silently change user-provided facts.
9. Use clear professional legal language.
10. If jurisdiction-specific information is required but not supplied,
    clearly indicate that professional review is required.
11. Return only the document.
12. Use Markdown headings.
13. Include signature sections where appropriate.

DOCUMENT TYPE:

{document_type}

PARTIES:

{parties}

TERMS AND CONDITIONS:

{terms}

EFFECTIVE DATE:

{dates}

JURISDICTION:

{jurisdiction}

LANGUAGE:

{language}

Create an appropriately structured document.

Suggested structure:

# Document Title

## 1. Parties

## 2. Purpose

## 3. Definitions

## 4. Scope

## 5. Rights and Responsibilities

## 6. Payment / Consideration

## 7. Confidentiality

## 8. Intellectual Property

## 9. Term and Termination

## 10. Dispute Resolution

## 11. Governing Law

## 12. General Provisions

## 13. Signatures

Only include sections that are relevant to the selected document type.

Make sure the final document is internally consistent.
"""

        return prompt.strip()

    def generate_document(
        self,
        document_type: str,
        parties: str,
        terms: str,
        dates: str,
        jurisdiction: str = "Not specified",
        language: str = "English",
    ) -> str:

        prompt = self._build_prompt(
            document_type,
            parties,
            terms,
            dates,
            jurisdiction,
            language,
        )

        candidate_models = [self.settings.gemini_model]
        for fallback in ("gemini-3.7-flash", "gemini-flash-latest", "gemini-3.5-flash-lite"):
            if fallback not in candidate_models:
                candidate_models.append(fallback)

        last_error = None

        for model_name in candidate_models:
            try:
                response = self.client.models.generate_content(
                    model=model_name,
                    contents=prompt,
                    config=types.GenerateContentConfig(
                        temperature=0.2,
                        max_output_tokens=12000,
                    ),
                )

                generated_text = getattr(response, "text", None)
                if not generated_text:
                    continue

                generated_text = generated_text.strip()
                if not generated_text:
                    continue

                self.last_used_model = model_name
                return generated_text

            except Exception as exc:
                last_error = exc
                error_str = str(exc)
                if any(code in error_str for code in ("503", "UNAVAILABLE", "429", "404")):
                    continue
                raise GeminiGenerationError(
                    f"Gemini generation failed: {exc}"
                ) from exc

        raise GeminiGenerationError(
            f"All candidate Gemini models failed. Last error: {last_error}"
        ) from last_error