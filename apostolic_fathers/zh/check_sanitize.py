#!/usr/bin/env python3
"""成稿卫生检查：检测译文行中的草稿残留。
用法: python3 zh/check_sanitize.py
检查项：
1. 译文行(> 开头)与注行(- 开头)中混入的 ASCII 英文单词（允许：LXX、GHZ、CC、BY、SA、DOI、PDF、phoenix、Knopf 等白名单）
2. 「（校订」「见下）」等草稿标记
3. 重复的节行（同章内 "> N " 编号重复）
"""
import re, sys, unicodedata

ALLOW = {"LXX","GHZ","CC","BY","SA","DOI","PDF","phoenix","Knopf","Lake","Lightfoot","Harmer","Tauber","Macdonald","Zenodo","Loeb","Hades","LSB","A","B","C","L","S","Wis","Sir","Ecclus","Tob","Bar","Mt","Mk","Lk","Jn","Rom","Cor","Gal","Eph","Phil","Col","Thess","Tim","Tit","Philem","Heb","Jas","Pet","Jud","Rev","Gen","Exod","Lev","Num","Deut","Josh","Judg","Sam","Kgs","Chr","Ezra","Neh","Esth","Job","Ps","Prov","Eccl","Song","Isa","Jer","Lam","Ezek","Dan","Hos","Joel","Amos","Obad","Jonah","Mic","Nah","Hab","Zeph","Hag","Zech","Mal","Macc","Codex","Alexandrinus","Constantinopolitanus","Hierosolymitanus","Bryennios","Kennett","Morin","Bensly","Schmidt","Rosch","Namur","Florennes","Akhmim","Vaticanus","Sinaiticus","subscription"}
path = sys.argv[1] if len(sys.argv) > 1 else "zh/1_clement_zh.md"
bad = []
seen = {}
chapter = None
for i, line in enumerate(open(path), 1):
    s = line.rstrip("\n")
    if s.startswith("## "):
        chapter = s
        seen = {}
        continue
    if "（校订" in s or "见下）" in s:
        bad.append((i, "draft-marker", s))
    if s.startswith("> ") or s.startswith("- "):
        words = re.findall(r"[A-Za-z][A-Za-z'’\-]*", s)
        for w in words:
            if w not in ALLOW and not w.lower() in {a.lower() for a in ALLOW}:
                bad.append((i, "ascii-word:" + w, s))
        m = re.match(r"> (\d+) ", s)
        if m:
            key = (chapter, m.group(1))
            if key in seen:
                bad.append((i, "duplicate-verse:" + str(key), s))
            seen[key] = i
if bad:
    for i, kind, s in bad:
        print(f"{i}: [{kind}] {s[:80]}")
    sys.exit(1)
print("SANITY OK:", path)
