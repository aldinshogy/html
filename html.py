import re
import streamlit as st
import streamlit.components.v1 as components

def text_to_html(text: str) -> str:
    # Escape osnovnih HTML karaktera
    text = text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")

    # Bold (Markdown stil sa **)
    text = re.sub(r"\*\*(.*?)\*\*", r"<b>\1</b>", text)

    # Linkovi (automatski prepoznaj i dodaj <a> tag)
    def link_repl(match):
        url = match.group(0)
        if not url.startswith(("http://", "https://")):
            url = "https://" + url
        return f'<a href="{url}" target="_blank" rel="noopener noreferrer">{match.group(0)}</a>'

    link_pattern = r"(https?://[^\s]+|www\.[^\s]+|[a-zA-Z0-9_-]+\.[a-z]{2,})"
    text = re.sub(link_pattern, link_repl, text)

    # Prazne linije i novi redovi pretvaramo u <br>
    html_body = text.replace("\n", "<br>")

    return html_body

# Streamlit UI
st.title("📝 Pretvarač Teksta u HTML")

unos = st.text_area("Unesi svoj tekst ovdje:", height=250)

if st.button("Generiši HTML"):
    if unos.strip():
        html = text_to_html(unos)
        
        # HTML preview
        st.subheader("📌 HTML Preview")
        components.html(html, height=300, scrolling=True)
        
        # Sirovi HTML kod za kopiranje
        st.subheader("📋 Sirovi HTML kod")
        st.code(html, language="html")
    else:
        st.warning("⚠️ Molimo unesite tekst prije generisanja.")
