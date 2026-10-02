from fastapi.testclient import TestClient

from backend.main import app

from backend.services.document_service import (
    format_docx,
    format_pdf,
)


client = TestClient(app)


def test_root():

    response = client.get("/")

    assert response.status_code == 200

    data = response.json()

    assert data["status"] == "running"


def test_health():

    response = client.get(
        "/health"
    )

    assert response.status_code == 200

    data = response.json()

    assert "gemini_configured" in data

    assert "model" in data


def test_example():

    response = client.get(
        "/example"
    )

    assert response.status_code == 200

    data = response.json()

    assert (
        data["document_type"]
        == "Freelance Work Contract"
    )


def test_generate_validation():

    response = client.post(

        "/generate",

        json={

            "document_type": "",

            "parties": "A and B",

            "terms":
                "Confidentiality",

            "dates":
                "2026-10-02",
        }
    )

    assert response.status_code == 422


def test_txt_export():

    response = client.post(

        "/export",

        json={

            "document_type":
                "NDA",

            "text":
                "# NDA\n\n"
                "Confidential information.",

            "format":
                "txt",

            "terms":
                ["Confidentiality"],

            "brand_name":
                "LegalEase",
        }
    )


    assert response.status_code == 200

    assert (
        response
        .headers["content-type"]
        .startswith("text/plain")
    )


def test_docx_generation():

    data = format_docx(

        "# NDA\n\n"
        "Confidential information.",

        "NDA",

        ["Confidentiality"],

        "LegalEase"
    )


    # DOCX files are ZIP files.

    assert data[:2] == b"PK"


def test_pdf_generation():

    data = format_pdf(

        "# NDA\n\n"
        "Confidential information.",

        "NDA",

        ["Confidentiality"],

        "LegalEase"
    )


    assert data.startswith(
        b"%PDF"
    )


def test_docx_export_endpoint():

    response = client.post(

        "/export",

        json={

            "document_type":
                "NDA",

            "text":
                "# NDA\n\n"
                "Confidential information.",

            "format":
                "docx",

            "terms":
                ["Confidentiality"],

            "brand_name":
                "LegalEase",
        }
    )


    assert response.status_code == 200

    assert response.content[:2] == b"PK"