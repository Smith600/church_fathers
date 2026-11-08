import fitz, re, sys
doc = fitz.open('npnf201_eusebius_history_constantine.pdf')

def page_texts():
    for i in range(doc.page_count):
        yield doc[i].get_text()

raw = "\n".join(page_texts())
# normalize: keep logical lines
lines = raw.split("\n")

def clean(lines):
    out=[]
    i=0
    n=len(lines)
    while i<n:
        ln=lines[i].rstrip()
        s=ln.strip()
        # skip PDFPAGE markers
        if re.match(r'^(===PDFPAGE \d+===|<<<PDFPAGE \d+>>>)$', s):
            i+=1; continue
        # remove inline HTML-style artifacts
        s=s
        out.append(s)
        i+=1
    return out

# Find narrative chapter headings to structure by book
# We'll just print Book I region raw for manual inspection first
text_lines = raw.split("\n")
# find Book I. start (line index) and Book II. start
def find_book(marker):
    import re
    for idx,l in enumerate(text_lines):
        if l.strip()==marker:
            return idx
    return -1
b1=text_lines.index("Book I.\n") if "Book I.\n" in text_lines else None
# use regex
for idx,l in enumerate(text_lines):
    if l.strip()=="Book I.":
        start=idx; break
for idx,l in enumerate(text_lines):
    if l.strip()=="Book II.":
        end=idx; break
print("Book I raw lines:", start+1, "to", end+1, "count", end-start)
with open('教会史_eusebius_church_history/_book1_raw.txt','w') as f:
    f.write("\n".join(text_lines[start:end+1]))
print("wrote raw")
