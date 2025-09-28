import requests
import streamlit as st

API_URL = st.secrets["API_URL"]

st.set_page_config(page_title="JSON → PDF/DOCX", layout="centered")

# ── Inject CSS theme ─────────────────────────────────────────
st.markdown("""
<style>
.main {
    background-color: #f5f5dc;  /* beige */
    color: #333333;
    font-family: "Helvetica Neue", sans-serif;
}
h1, h2, h3 {
    color: #3e3e3e;
    font-weight: 600;
}
.stTextInput > div > div > input,
.stTextArea textarea,
.stSelectbox > div > div,
.stRadio > div,
.stFileUploader > div > div {
    border-radius: 12px !important;
    border: 1px solid #d6cfc7;
    box-shadow: 2px 2px 6px rgba(0,0,0,0.1);
    background-color: #fffaf0;
}
.stButton > button,
.stDownloadButton > button {
    background-color: #f5deb3;
    color: #333333;
    font-weight: 600;
    border-radius: 12px;
    border: none;
    padding: 0.6em 1.2em;
    box-shadow: 2px 2px 6px rgba(0,0,0,0.15);
    transition: 0.2s all;
}
.stButton > button:hover,
.stDownloadButton > button:hover {
    background-color: #e6c98b;
    color: #222222;
    transform: translateY(-2px);
}
.stFileUploader label {
    background-color: #f5deb3 !important;
    border-radius: 12px;
    padding: 0.4em 0.8em;
    box-shadow: 2px 2px 6px rgba(0,0,0,0.15);
}
.stFileUploader label:hover {
    background-color: #e6c98b !important;
}
</style>
""", unsafe_allow_html=True)

# ── UI ───────────────────────────────────────────────────────
st.title("📄 JSON → PDF / DOCX")
st.caption("Minimalist beige-themed frontend for your /render API")

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
