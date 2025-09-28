import requests
import streamlit as st

API_URL = st.secrets["API_URL"]

st.set_page_config(page_title="JSON to PDF/DOCX Converter", layout="centered")

# ── Inject CSS theme ─────────────────────────────────────────
st.markdown("""
<style>
/* General beige button style */
button[kind="primary"],
button[kind="secondary"],
.stButton > button,
.stDownloadButton > button {
    background-color: #f5deb3 !important;
    color: #333333 !important;
    font-weight: 600 !important;
    border-radius: 12px !important;
    border: none !important;
    padding: 0.6em 1.2em !important;
    box-shadow: 2px 2px 6px rgba(0,0,0,0.15) !important;
    transition: 0.2s all;
}
button[kind="primary"]:hover,
button[kind="secondary"]:hover,
.stButton > button:hover,
.stDownloadButton > button:hover {
    background-color: #e6c98b !important;
    color: #222222 !important;
    transform: translateY(-2px);
}

/* File uploader Browse button */
[data-testid="stFileUploaderBrowseButton"] {
    background-color: #f5deb3 !important;
    color: #333333 !important;
    font-weight: 600 !important;
    border-radius: 12px !important;
    border: none !important;
    padding: 0.4em 1em !important;
    box-shadow: 2px 2px 6px rgba(0,0,0,0.15) !important;
    transition: 0.2s all;
}
[data-testid="stFileUploaderBrowseButton"]:hover {
    background-color: #e6c98b !important;
    color: #222222 !important;
    transform: translateY(-2px);
}

/* Form submit button (Render Document) */
div.stForm button[type="submit"] {
    background-color: #f5deb3 !important;
    color: #333333 !important;
    font-weight: 600 !important;
    border-radius: 12px !important;
    border: none !important;
    padding: 0.6em 1.2em !important;
    box-shadow: 2px 2px 6px rgba(0,0,0,0.15) !important;
    transition: 0.2s all;
}
div.stForm button[type="submit"]:hover {
    background-color: #e6c98b !important;
    color: #222222 !important;
    transform: translateY(-2px);
}

/* Title in beige */
h1 {
    color: #f5deb3 !important;
    font-weight: 700 !important;
}
</style>
""", unsafe_allow_html=True)



# ── UI ───────────────────────────────────────────────────────
st.title("📄 JSON to PDF / DOCX Converter")
st.caption("Your Free Converter | Developed by Rhanny Urbis")

with st.form("render_form"):
    output = st.selectbox("Output format", ["pdf", "docx"])
    title = st.text_input("Document title (optional)")
    mode = st.radio("Input mode", ["Paste JSON text", "Upload text file"])

    json_area = None
    text_upload = None
    if mode == "Paste JSON text":
        json_area = st.text_area("JSON text", height=150)
    else:
        text_upload = st.file_uploader("Upload text file", type=["txt", "md"])

    image_upload = st.file_uploader("Optional image", type=["png", "jpg", "jpeg", "gif"])

    submitted = st.form_submit_button("Render Document")

if submitted:
    files = {}
    data = {"output": output}
    if title:
        data["title"] = title
    if json_area:
        data["json_text"] = json_area
    if text_upload:
        files["text"] = (text_upload.name, text_upload.read())
    if image_upload:
        files["image"] = (image_upload.name, image_upload.read())

    try:
        resp = requests.post(API_URL, data=data, files=files or None, timeout=60)
        if resp.status_code == 200:
            st.success("Rendered successfully")
            filename = f"output.{output}"
            st.download_button("Download File", resp.content, file_name=filename)
        else:
            st.error(f"Error {resp.status_code}: {resp.text}")
    except Exception as e:
        st.error(f"Request failed: {e}")
