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