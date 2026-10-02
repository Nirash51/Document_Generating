import html
import os
from datetime import date

import requests
import streamlit as st

from dotenv import load_dotenv


load_dotenv()


BACKEND_URL = os.getenv(
    "BACKEND_URL",
    "http://127.0.0.1:8000"
).rstrip("/")


APP_NAME = os.getenv(
    "APP_NAME",
    "LegalEase"
)


st.set_page_config(

    page_title=APP_NAME,

    page_icon="⚖️",

    layout="wide",

    initial_sidebar_state="expanded",
)


# ------------------------------------------------
# CUSTOM CSS
# ------------------------------------------------

st.markdown(
    """
<style>

.stApp {

    background:
        linear-gradient(
            135deg,
            #06111f,
            #0b1c2d
        );

    color: #edf6ff;
}


.hero {

    padding: 28px;

    border-radius: 20px;

    background:
        linear-gradient(
            135deg,
            #102a43,
            #073b4c
        );

    border:
        1px solid #1d6070;

    margin-bottom: 20px;
}


.hero h1 {

    margin: 0;

    color: #e8fbff;

    font-size: 42px;
}


.hero p {

    color: #b8d8df;

    margin-top: 8px;

    font-size: 17px;
}


.notice {

    padding: 14px;

    border-left:
        4px solid #36c2b4;

    background: #0e2530;

    border-radius: 8px;

    color: #cceef0;
}


.preview {

    background: #0d1827;

    border:
        1px solid #25455c;

    border-radius: 16px;

    padding: 22px;

    min-height: 450px;

    max-height: 650px;

    overflow-y: auto;

    color: #e8f1f7;

    font-family:
        Georgia,
        serif;

    line-height: 1.7;

    white-space: pre-wrap;
}


</style>
""",
    unsafe_allow_html=True
)


# ------------------------------------------------
# SESSION STATE
# ------------------------------------------------

if "document_text" not in st.session_state:

    st.session_state.document_text = ""


if "last_model" not in st.session_state:

    st.session_state.last_model = ""


# ------------------------------------------------
# HEADER
# ------------------------------------------------

st.markdown(
    """
<div class="hero">

<h1>⚖️ LegalEase</h1>

<p>
AI-Powered Legal Document Generator
</p>

</div>
""",
    unsafe_allow_html=True
)


st.markdown(
    """
<div class="notice">

<strong>Important:</strong>
LegalEase provides AI-assisted drafting.
It is not a substitute for professional
legal advice or legal review.

</div>
""",
    unsafe_allow_html=True
)


st.write("")


# ------------------------------------------------
# SIDEBAR
# ------------------------------------------------

with st.sidebar:

    st.header(
        "📄 Document Details"
    )


    document_type = st.selectbox(

        "Document Type",

        [

            "Employment Contract",

            "Non-Disclosure Agreement",

            "Lease Agreement",

            "Freelance Work Contract",

            "Employment Offer Letter",

            "Service Agreement",

            "General Agreement",

            "Custom",
        ]
    )


    if document_type == "Custom":

        document_type = st.text_input(

            "Custom Document Type",

            value="General Agreement"
        )


    parties = st.text_area(

        "Parties Involved",

        placeholder=(
            "Jane Doe (Service Provider), "
            "TechNova Inc. (Client)"
        ),

        height=100
    )


    terms = st.text_area(

        "Terms & Conditions",

        placeholder=(
            "Payment within 30 days; "
            "Confidentiality must be maintained; "
            "Termination with 15 days notice"
        ),

        height=150,

        help=(
            "Separate each clause "
            "with a semicolon (;)."
        )
    )


    dates = st.date_input(

        "Effective Date",

        value=date.today()
    ).isoformat()


    jurisdiction = st.text_input(

        "Jurisdiction",

        value="Not specified"
    )


    language = st.selectbox(

        "Language",

        [

            "English",

            "Tamil",

            "Hindi",

            "Malayalam",

            "Telugu",
        ]
    )


    brand_name = st.text_input(

        "Brand Name",

        value=APP_NAME
    )


    generate_button = st.button(

        "✨ Generate Document",

        type="primary",

        use_container_width=True
    )


# ------------------------------------------------
# GENERATE DOCUMENT
# ------------------------------------------------

if generate_button:

    if not document_type.strip():

        st.error(
            "Please enter a document type."
        )

    elif not parties.strip():

        st.error(
            "Please enter the parties."
        )

    elif not terms.strip():

        st.error(
            "Please enter the terms."
        )

    else:

        payload = {

            "document_type":
                document_type,

            "parties":
                parties,

            "terms":
                terms,

            "dates":
                dates,

            "jurisdiction":
                jurisdiction,

            "language":
                language,

            "brand_name":
                brand_name,
        }


        try:

            with st.spinner(
                "Generating legal document..."
            ):

                response = requests.post(

                    f"{BACKEND_URL}/generate",

                    json=payload,

                    timeout=180
                )


            if response.ok:

                data = response.json()


                st.session_state.document_text = (
                    data["text"]
                )


                st.session_state.last_model = (
                    data.get(
                        "model",
                        ""
                    )
                )


                st.success(
                    "Document generated successfully!"
                )


            else:

                try:

                    detail = (
                        response
                        .json()
                        .get(
                            "detail",
                            response.text
                        )
                    )

                except Exception:

                    detail = response.text


                st.error(
                    f"Backend Error: {detail}"
                )


        except requests.RequestException as exc:

            st.error(

                "Cannot connect to the "
                f"FastAPI backend at "
                f"{BACKEND_URL}.\n\n"
                f"Error: {exc}"
            )


# ------------------------------------------------
# MAIN CONTENT
# ------------------------------------------------

left_column, right_column = st.columns(
    [1.1, 1]
)


# ------------------------------------------------
# EDITOR
# ------------------------------------------------

with left_column:

    st.subheader(
        "✏️ Editable Document"
    )


    st.session_state.document_text = (
        st.text_area(

            "Edit your document",

            value=(
                st.session_state.document_text
            ),

            height=560,

            label_visibility="collapsed"
        )
    )


# ------------------------------------------------
# PREVIEW
# ------------------------------------------------

with right_column:

    st.subheader(
        "👁️ Document Preview"
    )


    if st.session_state.document_text:

        safe_text = html.escape(

            st.session_state.document_text
        )


        st.markdown(

            f"""
<div class="preview">

{safe_text}

</div>
""",

            unsafe_allow_html=True
        )


        if st.session_state.last_model:

            st.caption(
                "AI Model: "
                f"{st.session_state.last_model}"
            )


    else:

        st.info(
            "Generate a document to see "
            "the live preview."
        )


# ------------------------------------------------
# DOWNLOAD
# ------------------------------------------------

st.divider()

st.subheader(
    "⬇️ Download Document"
)


terms_list = [

    item.strip()

    for item in terms.split(";")

    if item.strip()
]


download_columns = st.columns(3)


formats = [

    (
        "txt",
        "📄 Download TXT",
        "text/plain"
    ),

    (
        "docx",
        "📝 Download DOCX",
        "application/"
        "vnd.openxmlformats-officedocument."
        "wordprocessingml.document"
    ),

    (
        "pdf",
        "📕 Download PDF",
        "application/pdf"
    ),
]


for column, (
    file_format,
    button_label,
    mime_type
) in zip(
    download_columns,
    formats
):

    with column:

        if st.session_state.document_text:

            try:

                export_response = requests.post(

                    f"{BACKEND_URL}/export",

                    json={

                        "document_type":
                            document_type,

                        "text":
                            st.session_state.document_text,

                        "format":
                            file_format,

                        "terms":
                            terms_list,

                        "brand_name":
                            brand_name,
                    },

                    timeout=60
                )


                if export_response.ok:

                    st.download_button(

                        label=button_label,

                        data=(
                            export_response.content
                        ),

                        file_name=(
                            f"legalease-document."
                            f"{file_format}"
                        ),

                        mime=mime_type,

                        key=(
                            f"download_{file_format}"
                        ),

                        use_container_width=True
                    )

                else:

                    st.error(
                        f"{file_format.upper()} "
                        "export failed."
                    )


            except requests.RequestException as exc:

                st.error(
                    f"Export failed: {exc}"
                )

        else:

            st.button(

                button_label,

                disabled=True,

                key=(
                    f"disabled_{file_format}"
                ),

                use_container_width=True
            )


# ------------------------------------------------
# FOOTER
# ------------------------------------------------

st.divider()

st.caption(

    "LegalEase | "
    "AI-assisted legal document drafting | "
    "Review important documents professionally "
    "before use."
)