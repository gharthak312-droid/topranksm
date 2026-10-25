import re, json

src = open('index.html').read()

# ---------- extract FAQ from JSON-LD ----------
faq = []
for block in re.findall(r'<script type="application/ld\+json">(.*?)</script>', src, re.S):
    try:
        data = json.loads(block)
    except Exception:
        continue
    if data.get('@type') == 'FAQPage':
        for q in data.get('mainEntity', []):
            a = q.get('acceptedAnswer', {}).get('text', '')
            a = re.sub(r'<[^>]+>', '', a)
            faq.append((q.get('name', ''), a))
if len(faq) < 3:
    faq = [
        ("What is TopRankSM?", "TopRankSM is the public leaderboard where anyone can claim the #1 spot. Every social platform gets its own board, and the highest claim takes #1. Money = Rank."),
        ("How much does a claim cost?", "Claims start at just $1 (about Rs 280). To take a higher rank, claim at least $1 more than the claim above you."),
        ("How do I place a claim?", "Pick a board on topranksm.com, enter your profile handle, link, country and city, choose your claim amount, and pay. With card payment your claim goes live automatically; with manual payment it goes live after admin approval."),
        ("What payment methods are accepted?", "Card payment is processed securely via Whop. Manual options shown on the website include Easypaisa, Nayapay, Sadapay, Upaisa, Faysal Bank and USDT (TRC20)."),
        ("What is a Season and the Hall of Fame?", "Boards run in Seasons of 3 months. When a Season ends, boards reset and the top champions are saved forever in the Hall of Fame."),
        ("Are claims refundable?", "No. All claims are final and non-refundable. Your listing stays live at its rank for the rest of the Season."),
    ]

# ---------- extract country name->code map ----------
cmap = {}
for n, c in re.findall(r"\{n:'([^']+)',\s*c:'([A-Z]{2})'\}", src):
    cmap[n] = c.lower()
for c, n in re.findall(r"c:'([A-Z]{2})',\s*n:'([^']+)'", src):
    cmap[n] = c.lower()
for n, c in re.findall(r"name:'([^']+)',\s*code:'([A-Z]{2})'", src):
    cmap[n] = c.lower()
print('countries extracted:', len(cmap), '| faq items:', len(faq))

CSS = """
*{margin:0;padding:0;box-sizing:border-box}
body{font-family:'Plus Jakarta Sans','Segoe UI',sans-serif;background:#fff;color:#0c0c0e;min-height:100vh}
a{color:#2563eb}
header{border-bottom:1px solid #e7e7ea;background:#fff;position:sticky;top:0;z-index:5}
.hwrap{max-width:820px;margin:0 auto;padding:12px 20px;display:flex;align-items:center;gap:14px;flex-wrap:wrap}
.logo{font-size:20px;font-weight:800;color:#0c0c0e;text-decoration:none}
.logo span{background:linear-gradient(90deg,#b8860b,#d9a514);-webkit-background-clip:text;-webkit-text-fill-color:transparent}
nav{display:flex;gap:6px;flex-wrap:wrap;margin-left:auto}
nav a{color:#0c0c0e;text-decoration:none;font-weight:600;font-size:14px;padding:7px 12px;border-radius:99px;border:1px solid #e7e7ea}
nav a:hover{border-color:#d9a514}
nav a.on{background:linear-gradient(90deg,#b8860b,#d9a514);color:#fff;border-color:transparent}
.wrap{max-width:820px;margin:0 auto;padding:28px 20px 60px}
h1{font-size:30px;margin-bottom:6px;letter-spacing:-.5px}
h1 span{background:linear-gradient(90deg,#b8860b,#d9a514);-webkit-background-clip:text;-webkit-text-fill-color:transparent}
.sub{color:#6d6d78;margin-bottom:22px;line-height:1.55}
h2{font-size:20px;margin:26px 0 10px}
p,li{line-height:1.75;color:#26262b}
ul{margin:0 0 18px 20px}
.card{border:1px solid #e7e7ea;background:#f6f6f7;border-radius:16px;padding:18px;margin-bottom:14px}
.gold{border:2px solid #f0d98a;background:#fff7df}
.row{display:flex;align-items:center;gap:10px;padding:10px 12px;border:1px solid #e7e7ea;border-radius:12px;margin-bottom:8px;background:#fff}
.rk{font-weight:800;color:#b8860b;min-width:34px;text-align:center}
.row .h{font-weight:700}
.row .m{color:#6d6d78;font-size:13px}
.row .amt{margin-left:auto;font-weight:800;color:#b8860b;white-space:nowrap}
.grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(230px,1fr));gap:12px}
.bcard{border:1px solid #e7e7ea;border-radius:16px;padding:16px;background:#fff}
.bcard h3{font-size:17px;margin-bottom:4px}
.bcard p{color:#6d6d78;font-size:14px;line-height:1.5}
.bcard .cnt{margin-top:8px;font-weight:800;color:#b8860b;font-size:14px}
.qa{border:1px solid #e7e7ea;border-radius:14px;padding:16px;margin-bottom:10px;background:#fff}
.qa h3{font-size:16px;margin-bottom:6px}
.qa p{color:#3c3c44}
.flagimg{width:20px;height:15px;border-radius:2px;vertical-align:-2px;margin-right:6px}
.chip{display:inline-block;background:#f6f6f7;border:1px solid #e7e7ea;border-radius:99px;padding:3px 10px;font-size:12.5px;margin:2px 2px 0 0;color:#3c3c44}
.btn{display:inline-block;background:linear-gradient(90deg,#b8860b,#d9a514);color:#fff;font-weight:800;text-decoration:none;padding:12px 22px;border-radius:12px;margin-top:8px}
.btn:hover{filter:brightness(1.07)}
footer{max-width:820px;margin:0 auto;padding:18px 20px 34px;border-top:1px solid #e7e7ea;color:#6d6d78;font-size:13px}
.empty{color:#6d6d78;padding:14px;border:1px dashed #d9d9de;border-radius:12px;text-align:center}
"""

NAV = [('index.html', 'Home'), ('boards.html', 'Boards'), ('today.html', 'Today'), ('rules.html', 'Rules'), ('hall-of-fame.html', 'Hall of Fame'), ('countries.html', 'Countries'), ('faq.html', 'FAQ')]

def page(fname, title, desc, active, body, js='', head_extra=''):
    nav = ''.join('<a href="%s"%s>%s</a>' % (h, ' class="on"' if h == active else '', t) for h, t in NAV)
    html = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>%s</title>
<meta name="description" content="%s">
<link rel="canonical" href="https://topranksm.com/%s">
<meta property="og:title" content="%s">
<meta property="og:description" content="%s">
<meta property="og:type" content="website">
<meta property="og:url" content="https://topranksm.com/%s">
<meta property="og:image" content="https://topranksm.com/og-image%%20(1).jpg">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="%s">
<meta name="twitter:description" content="%s">
<meta name="twitter:image" content="https://topranksm.com/og-image%%20(1).jpg">
<link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;600;700;800&display=swap" rel="stylesheet">
<style>%s</style>
%s</head>
<body>
<header><div class="hwrap"><a class="logo" href="index.html">&#127942; TopRank<span>SM</span></a><nav>%s</nav></div></header>
<div class="wrap">
%s
</div>
<footer>&copy; 2026 TopRankSM &middot; <a href="terms.html">Terms</a> &middot; <a href="privacy.html">Privacy</a> &middot; <a href="refunds.html">Refunds</a> &middot; <a href="pricing.html">Pricing</a></footer>
%s
</body>
</html>""" % (title, desc, fname, title, desc, fname, title, desc, CSS, head_extra, nav, body, ('<script>' + js + '</script>') if js else '')
    open(fname, 'w').write(html)
    print('wrote', fname, len(html))

CORE = """
var SB='https://bgtdixpgosanjchwnomu.supabase.co',KEY='sb_publishable_cven97RCNBVYCeWUt2E76w_yKq-RSOE';
function api(p){return fetch(SB+'/rest/v1/'+p,{headers:{apikey:KEY,Authorization:'Bearer '+KEY}}).then(function(r){return r.json()})}
function usd(p){var v=p/280;return '$'+(p%280===0? String(v) : v.toFixed(2))}
function esc(s){return String(s==null?'':s).replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;')}
function row(i,b,boardLine){return '<div class="row"><div class="rk">#'+(i+1)+'</div><div><div class="h">'+esc(b.handle||'')+'</div><div class="m">'+boardLine+'</div></div><div class="amt">'+usd(b.amount||0)+'</div></div>'}
"""

BOARDS = [
    ('tiktok', 'TikTok', 'Short-video creators and viral stars.'),
    ('facebook', 'Facebook', 'Pages, profiles and public figures.'),
    ('instagram', 'Instagram', 'Creators, influencers and brands.'),
    ('youtube', 'YouTube', 'Channels and video creators.'),
    ('twitter', 'X', 'Posts, profiles and public voices.'),
    ('snapchat', 'Snapchat', 'Snap stars and creators.'),
    ('linkedin', 'LinkedIn', 'Professionals and companies.'),
    ('threads', 'Threads', 'Threads profiles and creators.'),
    ('websites', 'Websites', 'Any website that wants the top spot.'),
    ('apps', 'Apps', 'Mobile apps and games.'),
    ('fans', 'Fan Board', 'One board for everyone — the biggest claim overall wins.'),
]
BNAME = {b[0]: b[1] for b in BOARDS}

# ---------------- RULES ----------------
rules_body = """
<h1>Rules — <span>TopRankSM</span></h1>
<p class="sub">How the public leaderboard works. Simple, public and the same for everyone.</p>
<h2>How it works</h2>
<ul>
<li><b>Pick a board</b> — there are 11 boards: TikTok, Facebook, Instagram, YouTube, X, Snapchat, LinkedIn, Threads, Websites, Apps and the Fan Board.</li>
<li><b>Place your claim</b> — enter your profile handle, link, country and city, and your claim amount.</li>
<li><b>Highest claim takes #1</b> — your claim is your rank. Money = Rank.</li>
</ul>
<h2>Claiming rules</h2>
<ul>
<li>First claim on any board: <b>$1</b> (about Rs 280).</li>
<li>Minimum raise: <b>$1</b> above the current top claim.</li>
<li><b>Restricted listings:</b> adult, gambling, weapons and scam/Ponzi websites or apps cannot be claimed — the claim form blocks them automatically.</li>
<li><b>Tie rule:</b> if two claims are equal, the earlier claim keeps the higher rank.</li>
<li>Every claim is <b>public</b> — anyone can see every challenger, amount and rank, including the public click counter on each listing.</li>
<li>Claims must be for a <b>real, public profile, page, website or app</b>. Fake or abusive entries can be removed by the admin.</li>
</ul>
<h2>Payments</h2>
<ul>
<li><b>Card payment</b> (via Whop): your claim goes <b>live automatically</b> as soon as the payment succeeds.</li>
<li><b>Manual payment</b> (Easypaisa, Nayapay, Sadapay, Upaisa, Faysal Bank or USDT TRC20 — details on the home page): your claim goes live after the admin verifies and approves it.</li>
<li>All claims are <b>final and non-refundable</b> — see the <a href="refunds.html">Refund Policy</a>.</li>
</ul>
<h2>Seasons &amp; the Hall of Fame</h2>
<ul>
<li>Boards run in <b>Seasons of 3 months</b>. Season 1 ends on 18 January 2027.</li>
<li>When a Season ends, the boards reset and the <b>top 10 of every board</b> are saved forever in the <a href="hall-of-fame.html">Hall of Fame</a>.</li>
</ul>
<a class="btn" href="index.html">Claim your #1 spot</a>
"""
page('rules.html', 'Rules — TopRankSM', 'TopRankSM rules: how claiming works, $1 minimum claim and raise, card and manual payments, 3-month Seasons and the Hall of Fame.', 'rules.html', rules_body)

# ---------------- BOARDS ----------------
cards = ''.join('<div class="bcard"><h3>%s</h3><p>%s</p><div class="cnt" id="cnt-%s">… live claims</div></div>' % (n, d, i) for i, n, d in BOARDS)
boards_body = """
<h1>Boards — <span>TopRankSM</span></h1>
<p class="sub">11 public leaderboards. One for every platform — plus Websites, Apps and the cross-platform Fan Board. The counts below are live.</p>
<div class="grid">%s</div>
<a class="btn" href="index.html">Claim on a board</a>
""" % cards
boards_js = CORE + """
api('claims?select=board&status=eq.live&limit=2000').then(function(rows){
  var c={}; (rows||[]).forEach(function(r){c[r.board]=(c[r.board]||0)+1});
  Object.keys(c).forEach(function(k){var el=document.getElementById('cnt-'+k); if(el) el.textContent=c[k]+' live claims';});
  %s.forEach(function(id){var el=document.getElementById('cnt-'+id); if(el && el.textContent.indexOf('live')<0) el.textContent='0 live claims';});
}).catch(function(){});
""" % json.dumps([b[0] for b in BOARDS])
page('boards.html', 'Boards — TopRankSM', 'All 11 TopRankSM leaderboards: TikTok, Facebook, Instagram, YouTube, X, Snapchat, LinkedIn, Threads, Websites, Apps and the Fan Board — with live claim counts.', 'boards.html', boards_body, boards_js)

# ---------------- TODAY ----------------
today_body = """
<h1>Today — <span>TopRankSM</span></h1>
<p class="sub">Fresh claims placed today, and every challenger currently live on the boards.</p>
<h2>Today's claims</h2>
<div id="todayList"><div class="empty">Loading…</div></div>
<h2>All Challengers</h2>
<div id="allList"><div class="empty">Loading…</div></div>
<a class="btn" href="index.html">Place your claim</a>
"""
today_js = CORE + """
var BN=%s;
function line(b){var s=esc(BN[b.board]||b.board||''); if(b.country) s+=' · '+esc(b.country); if(b.city) s+=' · '+esc(b.city); return s}
api('claims?select=board,handle,link,amount,challenger,country,city,t&status=eq.live&order=amount.desc&limit=500').then(function(rows){
  rows=rows||[];
  var all=document.getElementById('allList');
  all.innerHTML=rows.length? rows.map(function(b,i){return row(i,b,line(b))}).join('') : '<div class="empty">No live claims yet — be the first.</div>';
  var today=new Date().toLocaleDateString('en-CA',{timeZone:'Asia/Karachi'});
  var tb=rows.filter(function(b){ if(!b.t) return false; var d=new Date(b.t); if(isNaN(d)) return false; return d.toLocaleDateString('en-CA',{timeZone:'Asia/Karachi'})===today; });
  var tl=document.getElementById('todayList');
  tl.innerHTML=tb.length? tb.map(function(b,i){return row(i,b,line(b))}).join('') : '<div class="empty">No claims yet today — the day is young.</div>';
}).catch(function(){document.getElementById('allList').innerHTML='<div class="empty">Could not load claims right now.</div>';});
""" % json.dumps(BNAME)
page('today.html', 'Today — TopRankSM', "Today's claims and all live challengers on TopRankSM — the public leaderboard where anyone can claim #1 from $1.", 'today.html', today_body, today_js)

# ---------------- HALL OF FAME ----------------
hof_body = """
<h1>Hall of Fame — <span>TopRankSM</span></h1>
<p class="sub">When a Season ends, the top 10 of every board are immortalized here forever. Season 1 ends on <b>18 January 2027</b>.</p>
<div id="hofList"><div class="empty">Loading…</div></div>
<h2>Current leaders</h2>
<div id="leadList"><div class="empty">Loading…</div></div>
<a class="btn" href="index.html">Become a champion</a>
"""
hof_js = CORE + """
var BN=%s;
function line(b){var s=esc(BN[b.board]||b.board||''); if(b.country) s+=' · '+esc(b.country); return s}
api('hall_of_fame?select=*&order=season.desc,amount.desc&limit=200').then(function(rows){
  var el=document.getElementById('hofList');
  if(!rows || !rows.length){ el.innerHTML='<div class="empty">No champions yet — Season 1 is still running. The first names will be crowned here on 18 January 2027.</div>'; return; }
  el.innerHTML=rows.map(function(b,i){return row(i,b,line(b)+' · Season '+(b.season||''))}).join('');
}).catch(function(){document.getElementById('hofList').innerHTML='<div class="empty">No champions yet — Season 1 is still running.</div>';});
api('claims?select=board,handle,amount,country&status=eq.live&order=amount.desc&limit=10').then(function(rows){
  var el=document.getElementById('leadList');
  el.innerHTML=(rows&&rows.length)? rows.map(function(b,i){return row(i,b,line(b))}).join('') : '<div class="empty">No live claims yet.</div>';
}).catch(function(){});
""" % json.dumps(BNAME)
page('hall-of-fame.html', 'Hall of Fame — TopRankSM', 'The TopRankSM Hall of Fame: Season champions from all 11 boards, saved forever — plus the current leaders.', 'hall-of-fame.html', hof_body, hof_js)

# ---------------- COUNTRIES ----------------
countries_body = """
<h1>Countries — <span>TopRankSM</span></h1>
<p class="sub">Challengers from around the world. Every country competes on the same boards — here is who is claiming, live.</p>
<div id="ctyList"><div class="empty">Loading…</div></div>
<a class="btn" href="index.html">Claim for your country</a>
"""
countries_js = CORE + """
var CMAP=%s;
api('claims?select=country,city,amount,handle&status=eq.live&limit=2000').then(function(rows){
  var by={};
  (rows||[]).forEach(function(r){ var c=(r.country||'').trim(); if(!c) return; by[c]=by[c]||{n:0,amt:0,top:'',topAmt:-1,cities:{}};
    by[c].n++; by[c].amt+=r.amount||0; if((r.amount||0)>by[c].topAmt){by[c].topAmt=r.amount||0; by[c].top=r.handle||'';}
    if(r.city) by[c].cities[r.city]=(by[c].cities[r.city]||0)+1; });
  var list=Object.keys(by).map(function(k){return {name:k,v:by[k]}}).sort(function(a,b){return b.v.n-a.v.n || b.v.amt-a.v.amt});
  var el=document.getElementById('ctyList');
  if(!list.length){ el.innerHTML='<div class="empty">No claims yet — your country could be first.</div>'; return; }
  el.innerHTML=list.map(function(x,i){ var cc=CMAP[x.name]; var flag=cc? '<img class="flagimg" src="https://flagcdn.com/w40/'+cc+'.png" alt="'+esc(x.name)+' flag" onerror="this.style.display=\\'none\\'">' : '';
    var cities=Object.keys(x.v.cities).sort(function(a,b){return x.v.cities[b]-x.v.cities[a]}).slice(0,3).map(function(cn){return '<span class="chip">'+esc(cn)+' · '+x.v.cities[cn]+'</span>'}).join('');
    return '<div class="row"><div class="rk">#'+(i+1)+'</div><div><div class="h">'+flag+esc(x.name)+'</div><div class="m">'+x.v.n+' claims · top: '+esc(x.v.top)+' ('+usd(x.v.topAmt)+')</div><div>'+cities+'</div></div><div class="amt">'+usd(x.v.amt)+'</div></div>'; }).join('');
}).catch(function(){document.getElementById('ctyList').innerHTML='<div class="empty">Could not load right now.</div>';});
""" % json.dumps(cmap)
page('countries.html', 'Countries — TopRankSM', 'TopRankSM challengers by country: live claim counts, top challengers and top cities from all over the world.', 'countries.html', countries_body, countries_js)

# ---------------- FAQ ----------------
qa = ''.join('<div class="qa"><h3>%s</h3><p>%s</p></div>' % (q, a) for q, a in faq)
faq_body = """
<h1>FAQ — <span>TopRankSM</span></h1>
<p class="sub">Quick answers about the public leaderboard.</p>
%s
<a class="btn" href="index.html">Claim your #1 spot</a>
""" % qa
faq_schema = '<script type="application/ld+json">\n' + json.dumps({"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in faq]}, ensure_ascii=False) + '\n</script>\n'
page('faq.html', 'FAQ — TopRankSM', 'TopRankSM FAQ: what it is, how claiming works, $1 minimum claim, payments, Seasons and the Hall of Fame, refunds.', 'faq.html', faq_body, head_extra=faq_schema)

print('ALL PAGES DONE')
