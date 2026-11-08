import fitz, re, os

doc = fitz.open('npnf202_socrates_sozomen.pdf')
os.makedirs('_npnf202_clean', exist_ok=True)

RANGES = {
 'soc1': (56,135), 'soc2': (136,225), 'soc3': (226,271), 'soc4': (272,327),
 'soc5': (328,374), 'soc6': (375,414), 'soc7': (415,470),
 'soz1': (552,595), 'soz2': (596,652), 'soz3': (653,694), 'soz4': (695,747),
 'soz5': (748,791), 'soz6': (792,866), 'soz7': (867,917), 'soz8': (918,964),
 'soz9': (965,985),
}

def body_lines(pno):
    page = doc[pno-1]
    d = page.get_text('dict')
    out = []
    for b in d['blocks']:
        if b['type'] != 0: continue
        for l in b['lines']:
            parts = []
            for sp in l['spans']:
                f = sp['font']; sz = sp['size']
                if sz < 10: continue
                if not f.startswith('Minion') and not f.startswith('Gentium'): continue
                if sz > 12: continue
                t = sp['text']
                if t.strip(): parts.append(t)
            if not parts: continue
            x0 = min(sp['bbox'][0] for sp in l['spans'] if sp['text'].strip())
            out.append((x0, ''.join(parts)))
    return out

def make_paras(page_ranges):
    all_lines = []
    for a, b in page_ranges:
        for p in range(a, b+1):
            all_lines.extend(body_lines(p))
    xs = sorted(x for x, t in all_lines)
    typical_left = xs[int(len(xs)*0.1)] if xs else 0
    out_paras = []
    cur = []
    def flush():
        if not cur: return
        txt = ''
        for t in cur:
            if not txt:
                txt = t
            elif txt.endswith('-') and t[:1].islower():
                txt = txt[:-1] + t
            elif txt and not txt.endswith(('-', ' ')) and t[:1].islower():
                txt += ' ' + t
            else:
                txt += ' ' + t
        out_paras.append(txt.strip())
        cur.clear()
    for x0, t in all_lines:
        ts = t.strip()
        if re.match(r'^(Chapter [IVX]+\.|Book [IVX]+\.)', ts):
            flush(); out_paras.append(ts); continue
        if re.match(r'^HISTORY OF', ts) or ts.upper().startswith('THE ECCLESIASTICAL'):
            flush(); out_paras.append(ts); continue
        # new paragraph if line is indented relative to typical left margin
        if cur and x0 > typical_left + 3:
            flush()
        cur.append(ts)
    flush()
    return '\n\n'.join(out_paras)

for name, (a, b) in RANGES.items():
    txt = make_paras([(a, b)])
    open(f'_npnf202_clean/{name}.txt', 'w').write(txt)
    print(name, len(txt), txt.count('Chapter'))
