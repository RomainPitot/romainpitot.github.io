# Generates a minimal, valid, single-page placeholder PDF for cv.pdf so the
# "Download CV" buttons don't 404. Replace assets output (../cv.pdf) with a
# real resume export whenever it's ready — no need to touch this script again.
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "cv.pdf")

lines = [
    "Romain Pitot",
    "Gameplay Programmer -- Unity / C#",
    "",
    "This CV is a placeholder. The real resume PDF will replace this file",
    "at the same path (cv.pdf) once it is ready.",
    "",
    "Contact: romainpitot.dev@gmail.com",
    "LinkedIn: linkedin.com/in/romain-pitot",
    "GitHub: github.com/romainpitot",
]

content_stream = "BT /F1 18 Tf 60 760 Td 22 TL\n"
content_stream += "(%s) Tj T*\n" % lines[0]
content_stream += "/F1 12 Tf\n"
for line in lines[1:]:
    escaped = line.replace("\\", r"\\").replace("(", r"\(").replace(")", r"\)")
    content_stream += "(%s) Tj T*\n" % escaped
content_stream += "ET"

objects = []
objects.append("<< /Type /Catalog /Pages 2 0 R >>")
objects.append("<< /Type /Pages /Kids [3 0 R] /Count 1 >>")
objects.append("<< /Type /Page /Parent 2 0 R /Resources << /Font << /F1 4 0 R >> >> "
                "/MediaBox [0 0 612 792] /Contents 5 0 R >>")
objects.append("<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica >>")
stream_bytes = content_stream.encode("latin-1")
objects.append(("<< /Length %d >>\nstream\n" % len(stream_bytes)).encode("latin-1") +
                stream_bytes + b"\nendstream")

pdf = bytearray()
pdf += b"%PDF-1.4\n"
offsets = [0]
for i, obj in enumerate(objects, start=1):
    offsets.append(len(pdf))
    pdf += ("%d 0 obj\n" % i).encode("latin-1")
    if isinstance(obj, bytes):
        pdf += obj
    else:
        pdf += obj.encode("latin-1")
    pdf += b"\nendobj\n"

xref_start = len(pdf)
pdf += ("xref\n0 %d\n" % (len(objects) + 1)).encode("latin-1")
pdf += b"0000000000 65535 f \n"
for off in offsets[1:]:
    pdf += ("%010d 00000 n \n" % off).encode("latin-1")
pdf += b"trailer\n"
pdf += ("<< /Size %d /Root 1 0 R >>\n" % (len(objects) + 1)).encode("latin-1")
pdf += b"startxref\n"
pdf += (str(xref_start) + "\n").encode("latin-1")
pdf += b"%%EOF"

with open(OUT, "wb") as f:
    f.write(pdf)

print("wrote", OUT, len(pdf), "bytes")
