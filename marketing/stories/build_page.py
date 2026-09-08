"""Assemble the launch-week review page from the rendered frames.

    python3 marketing/stories/build_page.py
Writes marketing/stories/launch-week-stories.html with the web-size frames
inlined, ready to publish as an Artifact.
"""
import json, html, base64, os
HERE = os.path.dirname(os.path.abspath(__file__))
FR = os.path.join(HERE, "frames")
frames = json.load(open(os.path.join(FR, "frames.json")))
for f in frames:
    f["img"] = "data:image/jpeg;base64," + base64.b64encode(open(f"{FR}/{f['id']}-web.jpg", "rb").read()).decode()

DAYS = [
 (1, "Wed 9 Sep",  "Tease",         "Something is blooming",  "Three frames that say nothing and promise everything. A countdown people can tap to be reminded, a poll to guess, a slider to play with."),
 (2, "Thu 10 Sep", "Reveal",        "Same soul, new home",    "The logo, the site's own hero rebuilt as a story, and one quiz built from events they have actually done."),
 (3, "Fri 11 Sep", "Launch",        "We're live",             "Link sticker day. The live site in a phone, the nine gallery categories, and an Add Yours chain for favourite moments."),
 (4, "Sat 12 Sep", "The Work",      "This or that",           "Four frames, four of their own venues. Polls and sliders only, because Saturday is a scrolling day, not a reading day."),
 (5, "Sun 13 Sep", "The Two of Us", "Introducing each other", "The founders section verbatim, an open Q&A box, and the 450+ figure turned into a quiz."),
 (6, "Mon 14 Sep", "Voices",        "Word for word",          "Two testimonials from the site, the Q&A answers, and one poll that sorts followers into past clients and prospects."),
 (7, "Tue 15 Sep", "Invite",        "Let us step in",         "The ask. A question box that lands in DMs, the stats, the contact headline with two links, and a closer to pin as a highlight."),
]
STICKERS = [
 ("Countdown", "d1-1, d2-3", "Tap to get reminded. Instagram sends a notification at zero, which is a launch-morning push you did not have to write."),
 ("Poll", "d1-2, d4-1, d4-3, d6-4", "Lowest-friction tap on the platform. Results are content for the next frame, so every poll here has a payoff the day after."),
 ("Emoji slider", "d1-3, d4-2", "Even lower friction than a poll. Good for frames that are really just a photograph you want people to sit with."),
 ("Quiz", "d2-2, d5-4", "Smuggles a fact in as a game. The two here carry the range of their work and the 450+ figure."),
 ("Question box", "d4-4, d5-3, d7-1", "Replies arrive as DMs, which is where a lead should arrive. Answer some publicly on Day 6; the rest are a conversation."),
 ("Add Yours", "d3-4", "Chains follower photos onto the launch. 450+ past clients is a lot of camera rolls. Reshare the best through the week."),
 ("Link", "d3-1, d3-3, d7-3, d7-4", "The whole point of the week. Big, centred, never the same frame as a poll, so nothing competes with it."),
 ("None", "d2-1, d5-1, d5-2, d6-1, d6-2, d7-2", "Reveal, quotes and numbers get no sticker. The reaction bar is enough; a poll on a testimonial cheapens it."),
]
def esc(s): return html.escape(s, quote=True)
NF=len(frames); NS=sum(1 for f in frames if not f['sticker'].startswith('None'))
WORDS={18:'eighteen',19:'nineteen',20:'twenty',21:'twenty-one',22:'twenty-two',23:'twenty-three',24:'twenty-four',25:'twenty-five',26:'twenty-six'}

p = []
p.append("""<title>Soul Launch Week Stories</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Marcellus&family=Instrument+Serif:ital@1&family=Space+Grotesk:wght@400;500;600&family=Space+Mono:wght@400;700&display=swap" rel="stylesheet">
<style>
:root{
  --porc:#F8F7F4; --ink:#1A1A22; --ink-plum:#2E2228; --ink-soft:#6B6670; --hair:#E7E5E0; --raised:#FFFFFF;
  --accent:#7B3B54; --accent-deep:#5A2A3F; --accent-soft:#A96B85; --blue:#C5D6E9; --blue-deep:#54708C; --blush:#F6DCE3;
  --ok:#3E7A5A; --ok-soft:#DDEDE3; --chg:#A8632E; --chg-soft:#F6E6D6;
  --display:"Marcellus", Georgia, serif; --serif:"Instrument Serif", Georgia, serif;
  --sans:"Space Grotesk", "Helvetica Neue", Arial, sans-serif; --mono:"Space Mono", ui-monospace, Menlo, monospace;
  --gutter:clamp(20px,5vw,72px);
}
@media (prefers-color-scheme:dark){
  :root:not([data-theme="light"]){
    --porc:#16151A; --ink:#F1EFEA; --ink-plum:#EDE6EA; --ink-soft:#A39DA8; --hair:#2C2A31; --raised:#1F1D24;
    --accent:#D19BB3; --accent-deep:#E4B9C9; --accent-soft:#B9849D; --blue:#54708C; --blue-deep:#C5D6E9; --blush:#3A2A32;
    --ok:#8FD3AE; --ok-soft:#1E3328; --chg:#E8A76B; --chg-soft:#3A2B1C;
  }
}
:root[data-theme="dark"]{
  --porc:#16151A; --ink:#F1EFEA; --ink-plum:#EDE6EA; --ink-soft:#A39DA8; --hair:#2C2A31; --raised:#1F1D24;
  --accent:#D19BB3; --accent-deep:#E4B9C9; --accent-soft:#B9849D; --blue:#54708C; --blue-deep:#C5D6E9; --blush:#3A2A32;
  --ok:#8FD3AE; --ok-soft:#1E3328; --chg:#E8A76B; --chg-soft:#3A2B1C;
}
*{box-sizing:border-box}
body{margin:0; background:var(--porc); color:var(--ink); font-family:var(--sans); font-size:15px; line-height:1.55; -webkit-font-smoothing:antialiased}
a{color:var(--accent)}
.wrap{padding-inline:var(--gutter); max-width:1480px; margin-inline:auto}
.mono{font-family:var(--mono); font-size:10.5px; letter-spacing:.14em; text-transform:uppercase; color:var(--ink-soft)}
h1,h2,h3{font-family:var(--display); font-weight:400; margin:0; text-wrap:balance; color:var(--ink)}
.ital{font-family:var(--serif); font-style:italic; color:var(--accent-deep)}
.head{padding-top:clamp(40px,7vh,88px); padding-bottom:clamp(28px,4vw,52px); display:grid; grid-template-columns:1fr auto; gap:32px; align-items:end; border-bottom:1px solid var(--hair)}
.head h1{font-size:clamp(2.4rem,6vw,5.2rem); line-height:1; letter-spacing:.004em; margin-top:14px}
.head p{max-width:58ch; color:var(--ink-plum); margin:20px 0 0; font-size:1.02rem}
.tally{font-family:var(--display); font-size:clamp(2rem,4vw,3.4rem); line-height:1; text-align:right; font-variant-numeric:tabular-nums}
.tally small{display:block; font-family:var(--mono); font-size:10.5px; letter-spacing:.14em; text-transform:uppercase; color:var(--ink-soft); margin-top:8px}
.tally .st{color:var(--ink-soft); font-size:.6em}
@media (max-width:640px){ .head{grid-template-columns:1fr} .tally{text-align:left} }
.arc{display:grid; grid-template-columns:repeat(7,minmax(0,1fr)); border-left:1px solid var(--hair); margin-top:clamp(28px,4vw,52px)}
.arc a{display:block; text-decoration:none; color:inherit; padding:16px 14px 18px; border-right:1px solid var(--hair); border-top:1px solid var(--hair); border-bottom:1px solid var(--hair); position:relative; transition:background 300ms}
.arc a:hover{background:var(--raised)}
.arc a::before{content:""; position:absolute; top:-1px; left:0; width:34px; height:2px; background:var(--accent)}
.arc .d{font-family:var(--mono); font-size:10.5px; letter-spacing:.14em; text-transform:uppercase; color:var(--ink-soft)}
.arc .b{display:block; font-family:var(--display); font-size:clamp(1rem,1.5vw,1.3rem); margin-top:10px; line-height:1.15}
.arc .n{display:block; font-family:var(--mono); font-size:10.5px; letter-spacing:.1em; color:var(--accent); margin-top:10px}
@media (max-width:900px){ .arc{grid-template-columns:repeat(4,minmax(0,1fr))} .arc a:nth-child(n+5){border-top:0} }
@media (max-width:560px){ .arc{grid-template-columns:repeat(2,minmax(0,1fr))} .arc a{border-top:1px solid var(--hair)} }
.sect{padding-block:clamp(40px,6vw,80px); border-bottom:1px solid var(--hair)}
.sect-head{display:flex; align-items:baseline; gap:18px; margin-bottom:8px; flex-wrap:wrap}
.sect-head .idx{font-family:var(--mono); font-size:10.5px; letter-spacing:.14em; color:var(--accent)}
.sect-head h2{font-size:clamp(1.7rem,3.2vw,2.6rem); line-height:1.05}
.sect-head .date{font-family:var(--mono); font-size:10.5px; letter-spacing:.14em; text-transform:uppercase; color:var(--ink-soft); margin-left:auto; white-space:nowrap}
.sect-lede{max-width:64ch; color:var(--ink-plum); margin:8px 0 clamp(24px,3vw,40px); font-size:1.02rem}
.row{display:grid; grid-template-columns:repeat(auto-fill,minmax(300px,1fr)); gap:clamp(18px,2.4vw,32px)}
.fr{display:grid; grid-template-rows:auto 1fr auto auto; background:var(--raised); border:1px solid var(--hair)}
.fr.is-approved{border-color:var(--ok)} .fr.is-change{border-color:var(--chg)}
.fr .ph{aspect-ratio:9/16; background:var(--hair); overflow:hidden; position:relative}
.fr .ph img{width:100%; height:100%; object-fit:cover; display:block}
.fr .ph .id{position:absolute; left:10px; top:10px; font-family:var(--mono); font-size:10px; letter-spacing:.12em; background:rgba(248,247,244,.92); color:#1A1A22; padding:4px 8px}
.fr .ph .state{position:absolute; right:10px; top:10px; font-family:var(--mono); font-size:10px; letter-spacing:.12em; text-transform:uppercase; padding:4px 8px; display:none}
.fr.is-approved .ph .state{display:block; background:var(--ok-soft); color:var(--ok)}
.fr.is-change .ph .state{display:block; background:var(--chg-soft); color:var(--chg)}
.fr .body{padding:16px 18px 6px; display:flex; flex-direction:column; gap:10px}
.fr h3{font-size:1.28rem; line-height:1.15}
.fr .stk{display:inline-flex; align-items:center; gap:8px; font-family:var(--mono); font-size:10.5px; letter-spacing:.12em; text-transform:uppercase; color:var(--accent)}
.fr .stk::before{content:""; width:6px; height:6px; border-radius:50%; background:var(--accent)}
.fr .copy{font-family:var(--display); font-size:1rem; line-height:1.4; color:var(--ink); border-left:2px solid var(--blush); padding-left:12px; margin:0}
.fr .note{color:var(--ink-soft); font-size:.9rem; line-height:1.5; margin:0}
.fr .act{display:grid; grid-template-columns:1fr 1fr; border-top:1px solid var(--hair); margin-top:8px}
.fr .act button{appearance:none; background:none; border:0; padding:13px 10px; font-family:var(--mono); font-size:10.5px; letter-spacing:.14em; text-transform:uppercase; color:var(--ink-soft); cursor:pointer; transition:background 240ms,color 240ms}
.fr .act button:first-child{border-right:1px solid var(--hair)}
.fr .act button:hover{background:var(--porc); color:var(--ink)}
.fr .act button:focus-visible{outline:2px solid var(--accent); outline-offset:-2px}
.fr.is-approved .act .ok{background:var(--ok-soft); color:var(--ok)}
.fr.is-change .act .chg{background:var(--chg-soft); color:var(--chg)}
.fr .cmt{border-top:1px solid var(--hair); padding:10px 18px 14px; display:none}
.fr.is-change .cmt{display:block}
.fr .cmt label{display:block; font-family:var(--mono); font-size:10px; letter-spacing:.12em; text-transform:uppercase; color:var(--chg); margin-bottom:6px}
.fr .cmt textarea{width:100%; min-height:64px; border:1px solid var(--hair); background:var(--porc); color:var(--ink); font:inherit; font-size:.9rem; padding:8px 10px; resize:vertical}
.fr .cmt textarea:focus-visible{outline:2px solid var(--chg); outline-offset:-1px}
.fr .cmt .saved{font-family:var(--mono); font-size:10px; letter-spacing:.1em; color:var(--ink-soft); margin-top:6px; min-height:14px}
.tbl{border-top:1px solid var(--hair)}
.tbl .r{display:grid; grid-template-columns:150px 200px minmax(0,1fr); gap:24px; padding:16px 0; border-bottom:1px solid var(--hair); align-items:baseline}
.tbl .r .k{font-family:var(--display); font-size:1.15rem}
.tbl .r .w{font-family:var(--mono); font-size:10.5px; letter-spacing:.1em; color:var(--accent)}
.tbl .r .v{color:var(--ink-plum)}
@media (max-width:760px){ .tbl .r{grid-template-columns:1fr; gap:6px} }
.rules{display:grid; grid-template-columns:repeat(auto-fit,minmax(260px,1fr)); gap:clamp(18px,3vw,40px)}
.rules h3{font-size:1.15rem; margin-bottom:8px}
.rules p{margin:0; color:var(--ink-plum)}
.foot{padding-block:36px 64px; color:var(--ink-soft); font-size:.9rem}
.foot .ital{font-size:1.15rem}
.offline{display:none; font-family:var(--mono); font-size:10.5px; letter-spacing:.12em; text-transform:uppercase; color:var(--ink-soft); margin-top:8px}
body.no-db .offline{display:block}
@media (prefers-reduced-motion:reduce){ *{transition:none !important} }
</style>
<main class="wrap">
<header class="head">
  <div>
    <span class="mono">Soul Events · Instagram · Wed 9 to Tue 15 September</span>
    <h1>Launch week, <span class="ital">frame by frame.</span></h1>
    <p>Seven days, """ + WORDS[len(frames)] + """ story frames, one arc: tease, reveal, launch, then a week of reasons to come back. Every photograph is from the studio's own decks. The sticker for each frame is named under it, to add in Instagram. Mark each frame approved or send it back with a note; what you mark here is what gets built.</p>
    <span class="offline">Approvals are view-only in this window</span>
  </div>
  <div class="tally"><span id="tOk">0</span><span class="st"> / """ + str(len(frames)) + """</span><small id="tLbl">approved · 0 to change</small></div>
</header>
<nav class="arc" aria-label="The week">
""")
for n, date, bucket, line, _ in DAYS:
    cnt = sum(1 for f in frames if f["day"] == n)
    inter = sum(1 for f in frames if f["day"] == n and not f["sticker"].startswith("None"))
    p.append(f'<a href="#day{n}"><span class="d">Day {n} · {date}</span><span class="b">{esc(bucket)}</span><span class="n">{cnt} frames · {inter} interactive</span></a>\n')
p.append("</nav>\n")
for n, date, bucket, line, lede in DAYS:
    p.append(f'<section class="sect" id="day{n}">\n  <div class="sect-head"><span class="idx">DAY {n}</span><h2>{esc(bucket)}, <span class="ital">{esc(line.lower())}.</span></h2><span class="date">{esc(date)}</span></div>\n  <p class="sect-lede">{esc(lede)}</p>\n  <div class="row">\n')
    for f in [x for x in frames if x["day"] == n]:
        p.append(f'''    <article class="fr" data-id="{f['id']}">
      <div class="ph"><img src="{f['img']}" alt="Draft story frame: {esc(f['title'])}" loading="lazy" width="540" height="960"><span class="id">{f['id'].upper()}</span><span class="state"></span></div>
      <div class="body"><h3>{esc(f['title'])}</h3><span class="stk">{esc(f['sticker'])}</span><p class="copy">{esc(f['copy'])}</p><p class="note">{esc(f['note'])}</p></div>
      <div class="act"><button type="button" class="ok">Approve</button><button type="button" class="chg">Change</button></div>
      <div class="cmt"><label for="n-{f['id']}">What to change</label><textarea id="n-{f['id']}" placeholder="Different photo, shorter line, drop the sticker..."></textarea><div class="saved"></div></div>
    </article>
''')
    p.append("  </div>\n</section>\n")
p.append('<section class="sect" id="stickers">\n  <div class="sect-head"><span class="idx">HOW</span><h2>Where the interactivity <span class="ital">actually comes from.</span></h2></div>\n  <p class="sect-lede">Instagram counts every tap on a story as engagement, and ranks the account on it. ' + WORDS[NS].capitalize() + ' of the ' + WORDS[NF] + ' frames get a native sticker, added in the Instagram app when posting; the frames themselves stay clean. Which one, and why, per type:</p>\n  <div class="tbl">\n')
for k, where, why in STICKERS:
    p.append(f'    <div class="r"><span class="k">{esc(k)}</span><span class="w">{esc(where)}</span><span class="v">{esc(why)}</span></div>\n')
p.append('''  </div>
</section>
<section class="sect" id="rules">
  <div class="sect-head"><span class="idx">RULES</span><h2>Five things that make <span class="ital">the week work.</span></h2></div>
  <div class="rules">
    <div><h3>Every poll pays off</h3><p>Day 1's guess is answered on Day 2. Day 3's "which first" decides Day 4's order. Day 6's "one of yours?" tells Day 7 who to speak to. Nothing is asked for its own sake.</p></div>
    <div><h3>Link sticker gets a clean frame</h3><p>Never on the same frame as a poll or a slider. On launch day it is the biggest thing on screen and it is there three times.</p></div>
    <div><h3>Answer the question boxes</h3><p>Day 4 and Day 5 open two of them. Reply to a handful publicly on Day 6 in the "You asked" template, and reply to the rest in DMs the same day. Unanswered boxes read as an unanswered phone.</p></div>
    <div><h3>Pin two frames as a highlight</h3><p>The launch frame (D3-1) and the closer (D7-4) go into a "New home" highlight before the week ends, so the link outlives the 24 hours.</p></div>
    <div><h3>Stickers go on in Instagram</h3><p>Every frame is a clean 1080×1920 image. The sticker to add, and its options where it has them, is written under each frame. D6-3 is a template to answer questions in; everything else is ready to post as drawn.</p></div>
  </div>
</section>
<footer class="foot">
  <span class="ital">Pouring our Heart &amp; Soul into turning your dreams to reality.</span><br>
  Frames are drafts at 1080×1920. Stickers shown are mock-ups; the real ones are added in the Instagram app when posting. Photographs are Soul Events' own, from the event decks supplied on 6 September.
</footer>
</main>
<script>
(function(){
  "use strict";
  var cards = Array.prototype.slice.call(document.querySelectorAll(".fr"));
  var tOk = document.getElementById("tOk"), tLbl = document.getElementById("tLbl");
  var state = {}, db = null, timers = {};
  function paint(){
    var ok = 0, chg = 0;
    cards.forEach(function(c){
      var s = state[c.dataset.id] || {};
      c.classList.toggle("is-approved", s.status === "approved");
      c.classList.toggle("is-change", s.status === "change");
      c.querySelector(".state").textContent = s.status === "approved" ? "Approved" : (s.status === "change" ? "Change" : "");
      var ta = c.querySelector("textarea");
      if (document.activeElement !== ta && typeof s.note === "string" && ta.value !== s.note) ta.value = s.note;
      if (s.status === "approved") ok++; if (s.status === "change") chg++;
    });
    tOk.textContent = ok; tLbl.textContent = "approved · " + chg + " to change";
  }
  function write(id, patch){
    state[id] = Object.assign({}, state[id] || {}, patch, {at: Date.now()});
    paint();
    if (db) db.doc("reviews/" + id).set(state[id]).catch(function(){});
  }
  cards.forEach(function(c){
    var id = c.dataset.id, ta = c.querySelector("textarea"), saved = c.querySelector(".saved");
    c.querySelector(".ok").addEventListener("click", function(){
      write(id, {status: (state[id] && state[id].status === "approved") ? null : "approved"});
    });
    c.querySelector(".chg").addEventListener("click", function(){
      write(id, {status: (state[id] && state[id].status === "change") ? null : "change"});
      if (state[id].status === "change") ta.focus();
    });
    ta.addEventListener("input", function(){
      window.clearTimeout(timers[id]); saved.textContent = "";
      timers[id] = window.setTimeout(function(){
        write(id, {note: ta.value});
        saved.textContent = db ? "Saved" : "Not saved in this window";
      }, 600);
    });
  });
  paint();
  if (!(window.claude && window.claude.use)) { document.body.classList.add("no-db"); return; }
  window.claude.use("db").then(function(ns){
    if (!ns) { document.body.classList.add("no-db"); return; }
    db = ns;
    db.collection("reviews").onSnapshot(function(snap){
      snap.docs.forEach(function(d){ state[d.id] = d.data() || {}; });
      paint();
    }, function(){ document.body.classList.add("no-db"); });
  }).catch(function(){ document.body.classList.add("no-db"); });
})();
</script>
''')
out = os.path.join(HERE, "launch-week-stories.html")
open(out, "w").write("".join(p))
print("wrote", out, round(os.path.getsize(out) / 1e6, 2), "MB")
