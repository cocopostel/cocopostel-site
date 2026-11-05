const P=window.POSTS||[];
const T={iran:/iran|irgc|tehran|hormuz|gulf|oman|saudi|uae|qatar|ukmto|tanker|centcom|minab/i,
me:/israel|lebanon|syria|iraq|yemen|gaza|hezbollah|kata.?ib|jerusalem|egypt|jordan|houthi|iran|saudi/i,
ua:/ukrain|russia|kyiv|moscow|zelensk|putin|geran/i,
us:/trump|biden|congress|senate|white house|election|democrat|republican|ntsb|new york|florida|washington|venezuela|rubio|vance/i};
const esc=s=>String(s||'').replace(/[&<>"]/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]));
const head=t=>{let h=t.split(/\n/)[0].replace(/^🚨\s*/,'');return h.length>150?h.slice(0,147).replace(/\s+\S*$/,'')+'…':h};
const body=t=>t.split(/\n\s*\n/).slice(1).join('\n\n');
const brk=t=>t.startsWith('🚨');
const kick=p=>brk(p.text)?'Breaking':'Update';
const fin=s=>s&&!/[.!?")]$/.test(s.trim())?s.trim()+'…':s;
const trim0=(s,n)=>s.length>n?s.slice(0,n).replace(/\s+\S*$/,'')+'…':s;
const trim=(s,n)=>fin(trim0(s,n));
const paras=s=>String(s||'').split(/\n\s*\n/).filter(Boolean).map(p=>`<p>${esc(p)}</p>`).join('');

function render(tab){
 const L=P.filter(p=>tab=='all'||T[tab].test(p.text));
 const empty=document.getElementById('empty');
 if(empty) empty.hidden=L.length>0;
 const lead=L.find(p=>brk(p.text))||L[0];const rest=L.filter(p=>p!==lead);
 const leadEl=document.getElementById('lead');
 if(leadEl) leadEl.innerHTML=lead?`<a href="${lead.url}" target="_blank" rel="noopener">${lead.img?`<img src="${lead.img}" alt="Image from the @CocoPostel post">`:''}<div class="kick" style="margin-top:12px">${kick(lead)}</div><h2>${esc(head(lead.text))}</h2></a><p>${esc(trim(body(lead.text),700))}</p><div class="meta">${lead.t} · <a href="${lead.url}" target="_blank" rel="noopener">Read on X</a></div>`:'';
 const latest=document.getElementById('latest');
 if(latest) latest.innerHTML=rest.slice(0,7).map(p=>`<li><div class="meta">${p.t.split(', ')[1]} · ${p.t.split(', ')[0]}</div><h3><a href="${p.url}" target="_blank" rel="noopener">${brk(p.text)?'<span class="kick">Breaking </span>':''}${esc(head(p.text))}</a></h3></li>`).join('');
 const more=document.getElementById('more');
 if(more) more.innerHTML=rest.slice(7).map(p=>`<article class="card"><a href="${p.url}" target="_blank" rel="noopener">${p.img?`<img loading="lazy" src="${p.img}" alt="Image from the @CocoPostel post">`:''}<h3>${esc(head(p.text))}</h3></a><p>${esc(trim(body(p.text),180))}</p><div class="meta">${p.t}</div></article>`).join('');
}

function renderReportList(R){
 const box=document.getElementById('reports');
 if(!box) return;
 box.innerHTML=R.map(r=>`<article class="card"><div class="kick">Report</div><h3><a href="report.html?id=${encodeURIComponent(r.slug)}">${esc(r.title)}</a></h3><p>${esc(r.summary)}</p><div class="meta">${esc(r.t)} GMT · <a href="report.html?id=${encodeURIComponent(r.slug)}">Read the report</a></div>${shareBar(r,true)}</article>`).join('');
}


function shareBar(r,compact){
 const u=location.origin+'/report.html?id='+encodeURIComponent(r.slug);
 const t=r.title;
 const eu=encodeURIComponent(u),et=encodeURIComponent(t);
 return `<div class="share${compact?' compact':''}" data-slug="${esc(r.slug)}"><span class="share-label">Share</span>
 <a class="sb" href="https://x.com/intent/post?text=${et}&url=${eu}" target="_blank" rel="noopener">X</a>
 <a class="sb" href="https://wa.me/?text=${et}%20${eu}" target="_blank" rel="noopener">WhatsApp</a>
 <a class="sb" href="https://t.me/share/url?url=${eu}&text=${et}" target="_blank" rel="noopener">Telegram</a>
 <a class="sb" href="https://www.facebook.com/sharer/sharer.php?u=${eu}" target="_blank" rel="noopener">Facebook</a>
 <button class="sb" type="button" data-act="link">Copy link</button>
 <button class="sb" type="button" data-act="text">Copy report</button>
 <button class="sb native" type="button" data-act="native"${navigator.share?'':' hidden'}>More</button></div>`;
}
document.addEventListener('click',async e=>{
 const b=e.target.closest('.share button');if(!b)return;
 const box=b.closest('.share');const slug=box.dataset.slug;
 const r=(window.__REPORTS||[]).find(x=>x.slug===slug);if(!r)return;
 const u=location.origin+'/report.html?id='+encodeURIComponent(slug);
 const full=r.title+'\n\n'+r.summary+'\n\n'+String(r.body||'').replace(/\\n/g,'\n')+'\n\n'+u;
 const act=b.dataset.act;
 try{
  if(act==='native'&&navigator.share){await navigator.share({title:r.title,text:r.summary,url:u});return}
  await navigator.clipboard.writeText(act==='link'?u:full);
 }catch(_){const ta=document.createElement('textarea');ta.value=act==='link'?u:full;document.body.appendChild(ta);ta.select();try{document.execCommand('copy')}catch(__){}ta.remove()}
 const o=b.textContent;b.textContent='Copied';setTimeout(()=>b.textContent=o,1500);
});
document.addEventListener('DOMContentLoaded',()=>{});

function renderReportPage(R){
 const id=new URLSearchParams(location.search).get('id')||'';
 const r=R.find(x=>x.slug===id)||R[0];
 const root=document.getElementById('report');
 if(!root||!r){
  if(root) root.innerHTML='<p class="empty">Report not found. <a href="index.html#press">Back to From the Press</a></p>';
  return;
 }
 document.title=r.title+' · CocoPostel News';
 root.innerHTML=`<p class="back"><a href="index.html#press">← Back to From the Press</a></p>
 <div class="kick">Report</div>
 <h1 class="report-title">${esc(r.title)}</h1>
 <div class="meta report-meta">${esc(r.t)} GMT · London</div>
 <div class="report-standfirst">${esc(r.summary)}</div>
 <div class="report-body">${paras(r.body)}</div>
 ${shareBar(r,false)}`;
}

const onHome=!!document.getElementById('lead');
if(onHome){
 document.querySelectorAll('#tabs button').forEach(b=>b.onclick=()=>{document.querySelectorAll('#tabs button').forEach(x=>x.classList.remove('on'));b.classList.add('on');render(b.dataset.t)});
 render('all');
 const tk=P.filter(p=>brk(p.text)).slice(0,8).map(p=>`<a href="${p.url}" target="_blank" rel="noopener">${esc(head(p.text))}</a>`).join('');
 const ticker=document.getElementById('ticker'); if(ticker) ticker.innerHTML=tk+tk;
 setTimeout(()=>{if(!document.querySelector('#live iframe')){const f=document.getElementById('fallback'); if(f) f.hidden=false}},6000);
}
const dl=document.getElementById('dateline');
if(dl) dl.textContent='London · '+new Date().toLocaleDateString('en-GB',{timeZone:'Europe/London',weekday:'long',day:'numeric',month:'long',year:'numeric'});

fetch('assets/reports.json?v='+Date.now()).then(r=>r.json()).then(R=>{
 window.__REPORTS=R; if(document.getElementById('report')) renderReportPage(R);
 else renderReportList(R);
}).catch(()=>{const press=document.getElementById('press'); if(press) press.hidden=true; const report=document.getElementById('report'); if(report) report.innerHTML='<p class="empty">Could not load the report.</p>';});
