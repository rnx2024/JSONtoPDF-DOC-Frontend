import io
import json
import requests
import streamlit as st
from typing import Optional

# ── Config ─────────────────────────────────────────────────────────────────────
API_BASE = st.secrets.get("API_BASE", "https://your-api.example.com")
API_PATH = st.secrets.get("API_PATH", "/render")
API_URL  = API_BASE.rstrip("/") + API_PATH
API_KEY  = st.secrets.get("API_KEY")              # optional
API_KEY_HEADER = st.secrets.get("API_KEY_HEADER", "X-API-Key")  # or "Authorization"

DEFAULT_TIMEOUT = (10, 60)  # (connect, read)

# ── Helpers ────────────────────────────────────────────────────────────────────
def infer_filename_from_headers(headers: dict, fallback: str) -> str:
    cd = headers.get("Content-Disposition", "")
    for part in cd.split(";"):
        part = part.strip()
        if part.lower().startswith("filename="):
            v = part.split("=", 1)[1].strip('"')
            return v or fallback
    return fallback

def build_headers(user_api_key: Optional[str] = None) -> dict:
    hdrs = {}
    key = user_api_key or API_KEY
    if key:
        if API_KEY_HEADER.lower() == "authorization" and not key.lower().startswith("bearer "):
            hdrs["Authorization"] = f"Bearer {key}"
        else:
            hdrs[API_KEY_HEADER] = key
    return hdrs

def post_render(
    json_text: Optional[str],
    text_file: Optional[bytes],
    text_filename: Optional[str],
    output: str,
    title: Optional[str],
    image_file: Optional[bytes],
    image_filename: Optional[str],
    user_api_key: Optional[str],
) -> requests.Response:
    data = {"output": output}
    if title:
        data["title"] = title

    files = {}

    if json_text:
        data["json_text"] = json_text

    if text_file:
        files["text"] = (text_filename or "text.txt", io.BytesIO(text_file))

    if image_file:
        files["image"] = (image_filename or "image.bin", io.BytesIO(image_file))

    hdrs = build_headers(user_api_key)

    return requests.post(API_URL, data=data, files=files or None, headers=hdrs, timeout=DEFAULT_TIMEOUT, stream=True)

# ── UI ─────────────────────────────────────────────────────────────────────────
st.set_page_config(page_title="JSON → PDF/DOCX", layout="centered")

st.title("JSON → PDF / DOCX")
st.caption("Front-end for your /render endpoint (multipart/form-data).")

with st.form("render_form"):
    col1, col2 = st.columns(2)
    with col1:
        output = st.selectbox("Output format *", ["pdf", "docx"], index=0)
        title = st.text_input("Title (optional)")
        user_api_key = st.text_input("API Key (optional if set in secrets)", type="password")
    with col2:
        mode = st.radio("Input mode *", ["Paste JSON text", "Upload text file"], index=0)

    json_area = None
    text_upload = None
    image_upload = st.file_uploader("Optional image (sent as `image`)", type=["png", "jpg", "jpeg", "webp", "gif"], accept_multiple_files=False)

    if mode == "Paste JSON text":
        json_area = st.text_area("json_text (string). Paste valid JSON or a JSON-like string.", height=180, placeholder='{"title":"Report","items":[...]}')
    else:
        text_upload = st.file_uploader("text (binary). Upload a .txt or .md file.", type=["txt", "md"], accept_multiple_files=False)

    submitted = st.form_submit_button("Render")

# Validate and submit
if submitted:
    # Basic validation: require either json_text or text file
    json_text = (json_area or "").strip()
    text_bytes = None
    text_name = None
    img_bytes = None
    img_name = None

    if mode == "Upload text file":
        if text_upload is not None:
            text_bytes = text_upload.read()
            text_name = text_upload.name
        else:
            st.error("Please upload a text file or switch to JSON mode.")
            st.stop()
    else:
        if not json_text:
            st.error("Please paste JSON text or switch to file mode.")
            st.stop()
        # Optional sanity check: if it looks like JSON, verify it parses
        try:
            json.loads(json_text)
        except Exception:
            # Non-strict: allow plain strings if your API permits
            pass

    if image_upload is not None:
        img_bytes = image_upload.read()
        img_name  = image_upload.name

    with st.status("Submitting to API…", expanded=False):
        try:
            resp = post_render(
                json_text=json_text if mode == "Paste JSON text" else None,
                text_file=text_bytes,
                text_filename=text_name,
                output=output,
                title=title or None,
                image_file=img_bytes,
                image_filename=img_name,
                user_api_key=user_api_key or None,
            )
        except requests.RequestException as e:
            st.error(f"Request failed: {e}")
            st.stop()

    if resp.status_code >= 400:
        # try to show json error
        err = None
        try:
            err = resp.json()
        except Exception:
            err = resp.text[:2000]
        st.error(f"API error {resp.status_code}: {err}")
        st.stop()

    # Stream into memory then offer download
    content = resp.content
    filename_fallback = f"output.{output}"
    filename = infer_filename_from_headers(resp.headers, filename_fallback)

    st.success("Rendered successfully.")
    st.download_button(
        "Download file",
        data=content,
        file_name=filename,
        mime="application/pdf" if output == "pdf" else "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
    )

    # Quick preview for PDF if small enough
    if output == "pdf" and len(content) < 5_000_000:
        st.divider()
        st.subheader("Inline preview")
        st.pdf(content)
