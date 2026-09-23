"""Build a small self-contained PDF from ebook.md using only Python stdlib."""
from pathlib import Path
import re

ROOT = Path(__file__).parent
SOURCE = ROOT / "ebook.md"
OUTPUT = ROOT / "impressao-3d-para-iniciantes.pdf"
W, H = 595, 842
objects = [None]

def add(data):
    objects.append(data if isinstance(data, bytes) else data.encode("latin-1"))
    return len(objects) - 1

def pdfstr(s):
    s = s.replace("’", "'").replace("–", "-").replace("—", "-").replace("×", "x")
    raw = s.encode("cp1252", "replace")
    return b"(" + raw.replace(b"\\", b"\\\\").replace(b"(", b"\\(").replace(b")", b"\\)") + b")"

font = add(b"<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica /Encoding /WinAnsiEncoding >>")
bold = add(b"<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica-Bold /Encoding /WinAnsiEncoding >>")
pages = []

def jpeg_object(path):
    data = path.read_bytes()
    # Generated images are baseline JPEGs (verified by file).
    return add(b"<< /Type /XObject /Subtype /Image /Width 512 /Height 512 /ColorSpace /DeviceRGB /BitsPerComponent 8 /Filter /DCTDecode /Length " + str(len(data)).encode() + b" >>\nstream\n" + data + b"\nendstream")

cover = jpeg_object(ROOT / "generated/GH-16-capa.jpg")

def make_page(items, cover_page=False):
    commands = ["q 0.96 0.95 0.91 rg 0 0 595 842 re f Q"]
    if cover_page:
        commands += ["q 0.06 0.20 0.24 rg 0 0 595 842 re f Q", "q 0.75 0.34 0.28 rg 0 0 595 14 re f Q"]
        commands += ["q 0 0 595 460 cm /Im0 Do Q"]
        commands += ["BT /F2 29 Tf 0.97 0.96 0.92 rg 54 720 Td " + pdfstr("IMPRESSÃO 3D") .decode("latin-1") + " Tj ET"]
        commands += ["BT /F2 26 Tf 0.97 0.96 0.92 rg 54 681 Td " + pdfstr("PARA INICIANTES").decode("latin-1") + " Tj ET"]
        commands += ["BT /F1 15 Tf 0.97 0.96 0.92 rg 55 637 Td " + pdfstr("Do Primeiro Modelo à Primeira Venda").decode("latin-1") + " Tj ET"]
        commands += ["BT /F1 11 Tf 0.97 0.96 0.92 rg 55 602 Td " + pdfstr("Guia prático para começar, aprender e testar").decode("latin-1") + " Tj ET"]
        stream = "\n".join(commands).encode("latin-1")
        content = add(b"<< /Length " + str(len(stream)).encode() + b" >>\nstream\n" + stream + b"\nendstream")
        pages.append((content, {"Im0": cover}))
        return

    y = 790
    for kind, text in items:
        if kind == "image":
            image = jpeg_object(ROOT / text)
            if y < 240:
                break
            commands += [f"q 300 0 0 180 147 {y-190} cm /Im{len(pages)} Do Q"]
            # one embedded image per page; image marker is followed by a page break in parser
            y -= 205
            continue
        if kind == "space":
            y -= 7
            continue
        size = 17 if kind == "h1" else 12.5 if kind == "h2" else 10.3
        leading = size * (1.45 if kind in ("h1", "h2") else 1.48)
        if kind == "h1":
            y -= 7
        max_chars = 66 if size > 12 else 93
        lines = []
        for para in text.split("\n"):
            if not para:
                lines.append("")
                continue
            while len(para) > max_chars:
                cut = para.rfind(" ", 0, max_chars)
                if cut < 1: cut = max_chars
                lines.append(para[:cut]); para = para[cut:].strip()
            lines.append(para)
        for line in lines:
            if y < 55:
                break
            face = "F2" if kind in ("h1", "h2") else "F1"
            color = "0.06 0.20 0.24" if kind in ("h1", "h2") else "0.12 0.14 0.15"
            commands.append(f"BT /{face} {size} Tf {color} rg 52 {y:.1f} Td ".replace(" Td ", " Td ") + pdfstr(line).decode("latin-1") + " Tj ET")
            y -= leading
        if y < 80:
            break
    stream = "\n".join(commands).encode("latin-1", "replace")
    content = add(b"<< /Length " + str(len(stream)).encode() + b" >>\nstream\n" + stream + b"\nendstream")
    pages.append((content, {}))

make_page([], True)
text = SOURCE.read_text(encoding="utf-8").splitlines()
current = []
for line in text:
    if line.startswith("!["):
        path = re.search(r"\]\(([^)]+)\)", line).group(1)
        current.append(("image", path))
        make_page(current)
        current = []
    elif line.startswith("# "):
        current.append(("h1", line[2:].strip()))
    elif line.startswith("## "):
        if current and any(kind != "space" for kind, _ in current):
            make_page(current)
            current = []
        current.append(("h2", line[3:].strip()))
    elif not line.strip() or line.strip() == "---":
        current.append(("space", ""))
    else:
        line = re.sub(r"\*\*(.*?)\*\*", r"\1", line)
        line = re.sub(r"`(.*?)`", r"\1", line)
        line = line.replace("- [ ]", "[ ]")
        current.append(("p", line.strip()))
if current:
    make_page(current)

page_ids = []
for content, images in pages:
    xobjects = " ".join(f"/{name} {obj} 0 R" for name, obj in images.items())
    resources = f"<< /Font << /F1 {font} 0 R /F2 {bold} 0 R >> /XObject << {xobjects} >> >>" if xobjects else f"<< /Font << /F1 {font} 0 R /F2 {bold} 0 R >> >>"
    page_ids.append(add(f"<< /Type /Page /Parent PAGES 0 R /MediaBox [0 0 {W} {H}] /Resources {resources} /Contents {content} 0 R >>"))
kids = " ".join(f"{n} 0 R" for n in page_ids)
pages_id = add(f"<< /Type /Pages /Kids [{kids}] /Count {len(page_ids)} >>")
for n in page_ids:
    objects[n] = objects[n].replace(b"PAGES 0 R", f"{pages_id} 0 R".encode())
catalog = add(f"<< /Type /Catalog /Pages {pages_id} 0 R >>")

out = bytearray(b"%PDF-1.4\n%\xe2\xe3\xcf\xd3\n")
offsets = [0]
for i, obj in enumerate(objects[1:], 1):
    offsets.append(len(out))
    out += f"{i} 0 obj\n".encode() + obj + b"\nendobj\n"
xref = len(out)
out += f"xref\n0 {len(objects)}\n0000000000 65535 f \n".encode()
for off in offsets[1:]:
    out += f"{off:010d} 00000 n \n".encode()
out += f"trailer\n<< /Size {len(objects)} /Root {catalog} 0 R >>\nstartxref\n{xref}\n%%EOF\n".encode()
OUTPUT.write_bytes(out)
print(f"{OUTPUT}: {len(pages)} páginas, {len(out)} bytes")
