import re
import streamlit as st


def text_to_html(text: str) -> str:
    # Escape osnovnih HTML karaktera
    text = text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")

    # Bold (Markdown stil sa **)
    text = re.sub(r"\*\*(.*?)\*\*", r"<b>\1</b>", text)

    # Linkovi (automatski prepoznaj i ako nema http://)
    text = re.sub(r"(https?://[^\s]+|www\.[^\s]+|[a-zA-Z0-9_-]+\.[a-z]{2,})",
                  r'<a href="https://\1" target="_blank" rel="noopener noreferrer">\1</a>', text)

    # Prazne linije pretvaramo u <p>
    paragraphs = [p.strip() for p in text.split("\n\n") if p.strip()]
    html_body = "".join(f"<p>{p.replace('\n', '<br>')}</p>" for p in paragraphs)

    # Cijeli HTML dokument
    html = f"""<!DOCTYPE html>
<html lang="bs">
<head>
  <meta charset="UTF-8">
  <title>Generisani HTML</title>
</head>
<body>
{html_body}
</body>
</html>"""

    return html


# Streamlit UI
st.title("📝 Pretvarač Teksta u HTML")

unos = st.text_area("Unesi svoj tekst ovdje:", height=250)

if st.button("Generiši HTML"):
    if unos.strip():
        html = text_to_html(unos)

        # Prikaži preview
        st.subheader("📌 HTML Preview")
        st.components.v1.html(html, height=300, scrolling=True)

        # Download dugme
        st.download_button("⬇️ Preuzmi HTML fajl", html, "output.html", "text/html")
    else:
        st.warning("⚠️ Molimo unesite tekst prije generisanja.")
