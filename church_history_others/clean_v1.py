import fitz, re
doc = fitz.open('npnf201_eusebius_history_constantine.pdf')
raw="\n".join(doc[i].get_text() for i in range(doc.page_count))
blocks=raw.split("===PDFPAGE ")
def strip_mech(b):
    # remove running heads: a 1-4 digit alone then Title-case heading, and bare page numbers
    lines=b.split("\n")
    out=[]
    i=0
    while i<len(lines):
        s=lines[i].strip()
        # skip bare numbers that look like page numbers or footnote leads -> collect as candidate
        out.append(s)
        i+=1
    return out
print("blocks(pseudo):", len(blocks))
# Save a "mechanical-noise-removed" version (keep footnotes) for reading
lines=raw.split("\n")
def is_runninghead(s):
    # Title-case running head heuristics
    return False
cleaned=[]
import re
i=0
N=len(lines)
removed_pdf=[]
removed_run=[]
foot=[]
while i<N:
    s=lines[i].strip()
    if re.match(r'^(===PDFPAGE \d+===|<<<PDFPAGE \d+>>>)$', s):
        i+=1; continue
    # drop standalone page numbers that are between footnotes and running heads,
    # heuristic: digit-only 1..4 AND not ending with period -> but footnote leads also digit-only.
    # We'll just drop pure 3-digit page-numbers that are followed by a title-case line.
    i+=1
    cleaned.append(s)
open('教会史_eusebius_church_history/_book1_mech.txt','w').write("\n".join(cleaned))
print("saved _book1_mech.txt lines:", len(cleaned))
