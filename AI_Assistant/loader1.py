from pypdf import PdfReader

def load_pdf(file_path):

    reader = PdfReader(file_path)

    text = ""

    for page in reader.pages:
        text += page.extract_text()

    return text
## Improve the chunking function to include an overlap of words between chunks
def chunk_text(text, chunk_size=300, overlap=50):

    words = text.split()

    chunks = []

    start = 0

    while start < len(words):

        end = start + chunk_size

        chunk = " ".join(words[start:end])

        chunks.append(chunk)

        start += chunk_size - overlap

    return chunks