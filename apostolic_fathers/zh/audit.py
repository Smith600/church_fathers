#!/usr/bin/env python3
"""S1 自动审计：节号对齐、术语一致性、标点规范。用法: python3 zh/audit.py"""
import re, glob, sys
from collections import defaultdict

# 1) 希腊节号全集
gr = set()
for f in glob.glob('zh/src/batch*_gr.txt'):
    for ln in open(f):
        m = re.match(r'^(\d+)\.(\d+) ', ln)
        if m: gr.add((int(m.group(1)), int(m.group(2))))
        m2 = re.match(r'^(SB)\.(\d+) ', ln)
        if m2: gr.add(('SB', 1))

# 2) 中文节号
zh = set()
chap = None
CN = {'零':0,'一':1,'二':2,'三':3,'四':4,'五':5,'六':6,'七':7,'八':8,'九':9,'十':10}
def cn2int(s):
    # 支持 一..九十九 简单形式
    if s in CN: return CN[s]
    if s.startswith('十'): return 10 + (CN[s[1]] if len(s)>1 else 0)
    if '十' in s:
        a,b = s.split('十'); return CN[a]*10 + (CN[b] if b else 0)
    return None
for ln in open('zh/1_clement_zh.md'):
    m = re.match(r'^## 卷首', ln); 
    if m: chap = 0; continue
    m = re.match(r'^## 卷末署名', ln)
    if m: chap = 'SB'; continue
    m = re.match(r'^## 第(.+?)章', ln)
    if m: chap = cn2int(m.group(1)); continue
    m = re.match(r'^> (\d+) ', ln)
    if m and chap is not None: zh.add((chap, int(m.group(1))))
    if chap == 0 and ln.startswith('> '): zh.add((0,1))
    if chap == 'SB' and ln.startswith('> '): zh.add(('SB',1))

miss = sorted(gr - zh); extra = sorted(zh - gr)
print('== 节号对齐 ==')
print('希腊节数:', len(gr), '中文节数:', len(zh))
print('中文缺失:', miss if miss else '无')
print('中文多余:', extra if extra else '无')

# 3) 术语一致性（计数供裁决）
text = open('zh/1_clement_zh.md').read()
groups = {
 'στάσις 系': ['纷争','叛乱','党争','派系争斗','分裂'],
 '顺服系': ['顺服','顺从','听从'],
 '敬畏系': ['敬畏','惧怕','害怕'],
 '喜乐系': ['喜乐','欢喜','欢欣'],
 '称呼系': ['弟兄们','弟兄，'],
 '寄居系': ['寄居','客居','旅居'],
 '教会职分': ['长老','监督','执事'],
}
print('== 术语计数（供裁决，非自动改） ==')
for g, ws in groups.items():
    print(g, {w: len(re.findall(w, text)) for w in ws})

# 4) 标点/格式
print('== 标点规范 ==')
print('中文引号「」:', text.count('「'), text.count('」'))
print('ASCII 双引号在译文行:', sum(1 for l in text.split('\n') if l.startswith('> ') and '"' in l))
print('连续空格行:', sum(1 for l in text.split('\n') if '  ' in l and l.startswith('> ')))
print('省略号规范（……）:', len(re.findall(r'……', text)), '三点...:', len(re.findall(r'(?<!\.)\.\.\.(?!\.)', text)))
