import json, html, os, glob, shutil
SRC=os.path.dirname(os.path.abspath(__file__)); OUT=os.path.join(SRC,'..','public')
CH=["始計","作戰","謀攻","軍形","兵勢","虛實","軍爭","九變","行軍","地形","九地","火攻","用間"]
NUM="一二三四五六七八九十"
def cn(n): return NUM[n-1] if n<=10 else "十"+NUM[n-11]
items=[]
for f in sorted(glob.glob(os.path.join(SRC,'data','*.json'))): items+=json.load(open(f,encoding='utf-8'))
N=len(items); e=html.escape
seq={}
for i,it in enumerate(items,1):
    seq[it['c']]=seq.get(it['c'],0)+1; it['n']=i; it['s']=seq[it['c']]
FONTS='<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Noto+Serif+TC:wght@500;700;900&family=Noto+Sans+TC:wght@400;500;700&display=swap">'
def page(title, rel, cur, content, extra=""):
    toc=[f'<a class="t-home{" on" if cur=="home" else ""}" href="{rel}index.html">首頁 · 今日一則</a>',
         f'<a class="t-inv{" on" if cur=="invest" else ""}" href="{rel}invest.html">孫子兵法與股市投資</a>']
    curc = items[cur-1]['c'] if isinstance(cur,int) else None
    for c in range(1,14):
        lis="".join(f'<li><a href="{rel}r/{it["n"]:03d}.html"{" class=\"on\" aria-current=\"page\"" if it["n"]==cur else ""}><span class="no">{it["n"]:02d}</span>{e(it["t"])}</a></li>' for it in items if it['c']==c)
        toc.append(f'<details class="tc"{" open" if c==curc else ""}><summary><span class="cno">第{cn(c)}</span>{CH[c-1]}篇</summary><ol>{lis}</ol></details>')
    return f'''<!doctype html><html lang="zh-Hant"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<title>{e(title)}</title>{FONTS}<link rel="stylesheet" href="{rel}style.css"></head><body>
<div class="layout">
<aside class="side"><details class="toc" id="toc"><summary>目錄 <small>十三篇 · {N} 則</small></summary><nav>{"".join(toc)}</nav></details></aside>
<div class="content">{content}</div>
</div>
<script>
(function(){{var d=document.getElementById("toc"),m=matchMedia("(min-width:960px)");function s(){{if(m.matches)d.open=true;}}s();m.addEventListener("change",s);
var on=document.querySelector(".toc a.on");if(on&&m.matches)on.scrollIntoView({{block:"center"}});}})();
</script>{extra}</body></html>'''
def ul(xs): return "<ul>"+"".join(f"<li>{e(x)}</li>" for x in xs)+"</ul>"
shutil.rmtree(OUT,ignore_errors=True); os.makedirs(os.path.join(OUT,'r'))
for it in items:
    i=it['n']; c=it['c']
    prev=f'<a href="{i-1:03d}.html" rel="prev"><span>上一則</span>{e(items[i-2]["t"])}</a>' if i>1 else '<span></span>'
    nxt=f'<a href="{i+1:03d}.html" rel="next" class="next"><span>下一則</span>{e(items[i]["t"])}</a>' if i<N else '<span></span>'
    long=' long' if len(it['o'])>70 else ''
    content=f'''<main>
<header><div class="eyebrow">第 {i} 則 · {CH[c-1]}篇 第{cn(c)}</div><h1>{e(it['t'])}</h1>
<div class="meta"><span>{CH[c-1]}篇(第 {it['s']} 則)</span><span>十三篇 · {c} / 13</span><span>{i} / {N}</span></div></header>
<div class="source{long}"><div class="slip">{e(it['o'])}</div>
<div class="translation"><h2>白話翻譯 <small>TRANSLATION</small></h2><p>{e(it['tr'])}</p></div></div>
<section><h2>重點解析 <small>KEY POINTS</small></h2>{ul(it['k'])}</section>
<section><h2>現代應用 <small>HARDWARE &amp; SOFTWARE</small></h2>{ul(it['e'])}</section>
<section class="inv"><h2>股市投資 <small>INVESTING</small></h2>{ul(it['i'])}<a class="more" href="../invest.html#ch{c}">{CH[c-1]}篇的投資原則總覽 →</a></section>
<section class="question"><h2>今日一問 <small>REFLECT</small></h2><p>{e(it['q'])}</p></section>
<nav class="pager">{prev}{nxt}</nav></main>'''
    open(os.path.join(OUT,'r',f'{i:03d}.html'),'w',encoding='utf-8').write(page(f"{it['t']}|孫子兵法每日導讀","../",i,content))
# index
groups=""
for c in range(1,14):
    lis="".join(f'<li><a href="r/{it["n"]:03d}.html"><span class="no">{it["n"]:02d}</span>{e(it["t"])}</a></li>' for it in items if it['c']==c)
    groups+=f'<section class="chap" id="ch{c}"><h2><span class="cno">第{cn(c)}</span>{CH[c-1]}篇</h2><ol>{lis}</ol></section>'
titles=json.dumps([it['t'] for it in items],ensure_ascii=False); chs=json.dumps([CH[it['c']-1]+"篇" for it in items],ensure_ascii=False)
content=f'''<main class="home">
<header class="hero"><div class="eyebrow">十三篇 · {N} 則</div><h1>孫子兵法每日導讀</h1>
<p class="lede">每天一則,依十三篇順序。每則都有原文、白話翻譯、重點解析,以及在硬體與軟體工程、股市投資上的應用。</p></header>
<a class="today" id="today" href="r/001.html"><span class="eyebrow">今日一則</span><strong id="today-t">{e(items[0]["t"])}</strong><span id="today-m" class="meta">始計篇 · 第 1 則</span></a>
<a class="today alt" href="invest.html"><span class="eyebrow">專題</span><strong>孫子兵法與股市投資</strong><span class="meta">十三篇的投資原則、六條核心規則與下單前檢查清單</span></a>
<div class="chapters">{groups}</div>
<footer class="foot">從 2026 年 11 月 23 日開始,每天輪到下一則,{N} 天一輪。</footer></main>'''
extra=f'''<script>(function(){{var T={titles},C={chs},N=T.length;var s=Date.UTC(2026,10,23),n=new Date(),t=Date.UTC(n.getFullYear(),n.getMonth(),n.getDate());
var i=((Math.floor((t-s)/864e5)%N)+N)%N;document.getElementById("today").href="r/"+String(i+1).padStart(3,"0")+".html";
document.getElementById("today-t").textContent=T[i];document.getElementById("today-m").textContent=C[i]+" · 第 "+(i+1)+" 則";}})();</script>'''
open(os.path.join(OUT,'index.html'),'w',encoding='utf-8').write(page("孫子兵法每日導讀","", "home", content, extra))
# invest
V=json.load(open(os.path.join(SRC,'invest.json'),encoding='utf-8'))
core="".join(f'<li><a href="r/{int(n):03d}.html"><strong>{e(t)}</strong></a><p>{e(d)}</p></li>' for t,d,n in V['core'])
chap=""
for x in V['chapters']:
    c=x['c']; links="".join(f'<a href="r/{n:03d}.html">{n:02d} {e(items[n-1]["t"])}</a>' for n in x['n'])
    chap+=f'<section class="ic" id="ch{c}"><h3><span class="cno">第{cn(c)}</span>{CH[c-1]}篇 <span class="p">{e(x["p"])}</span></h3>{ul(x["r"])}<div class="refs">{links}</div></section>'
ck="".join(f'<li><input type="checkbox" id="ck{k}"><label for="ck{k}">{e(q)}</label></li>' for k,q in enumerate(V['checklist']))
content=f'''<main class="invest">
<header><div class="eyebrow">專題</div><h1>孫子兵法與股市投資</h1><p class="lede">{e(V["intro"])}</p></header>
<section><h2>六條核心規則 <small>CORE RULES</small></h2><ol class="core">{core}</ol></section>
<section><h2>十三篇逐篇應用 <small>BY CHAPTER</small></h2><div class="ics">{chap}</div></section>
<section class="ck"><h2>下單前七問 <small>CHECKLIST</small></h2><ul class="cklist">{ck}</ul><p class="note">勾選只是給你自己看的,重新整理頁面就會清空。本頁是古典兵法的思維整理,不是個別投資建議。</p></section>
</main>'''
open(os.path.join(OUT,'invest.html'),'w',encoding='utf-8').write(page("孫子兵法與股市投資","", "invest", content))
shutil.copy(os.path.join(SRC,'style.css'),OUT); print("built",N)
