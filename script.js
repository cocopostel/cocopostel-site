const P=window.POSTS||[];
const T={iran:/iran|irgc|tehran|hormuz|gulf|oman|saudi|uae|qatar|ukmto|tanker|centcom|minab/i,
me:/israel|lebanon|syria|iraq|yemen|gaza|hezbollah|kata.?ib|jerusalem|egypt|jordan|houthi|iran|saudi/i,
ua:/ukrain|russia|kyiv|moscow|zelensk|putin|geran/i,
us:/trump|biden|congress|senate|white house|election|democrat|republican|ntsb|new york|florida|washington|venezuela|rubio|vance/i};
const esc=s=>s.replace(/[&<>"]/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]));
const head=t=>{let h=t.split(/\n/)[0].replace(/^🚨\s*/,'');return h.length>150?h.slice(0,147).replace(/\s+\S*$/,'')+'…':h};
const body=t=>t.split(/\n\s*\n/).slice(1).join('\n\n');
const brk=t=>t.startsWith('🚨');
const kick=p=>brk(p.text)?'Breaking':'Update';
const fin=s=>s&&!/[.!?")]$/.test(s.trim())?s.trim()+'…':s;
const trim0=(s,n)=>s.length>n?s.slice(0,n).replace(/\s+\S*$/,'')+'…':s;
const trim=(s,n)=>fin(trim0(s,n));
function render(tab){
 const L=P.filter(p=>tab=='all'||T[tab].test(p.text));
 document.getElementById('empty').hidden=L.length>0;
 const lead=L.find(p=>brk(p.text))||L[0];const rest=L.filter(p=>p!==lead);
 document.getElementById('lead').innerHTML=lead?`<a href="${lead.url}" target="_blank" rel="noopener">${lead.img?`<img src="${lead.img}" alt="Image from the @CocoPostel post">`:''}<div class="kick" style="margin-top:12px">${kick(lead)}</div><h2>${esc(head(lead.text))}</h2></a><p>${esc(trim(body(lead.text),700))}</p><div class="meta">${lead.t} · <a href="${lead.url}" target="_blank" rel="noopener">Read on X</a></div>`:'';
 document.getElementById('latest').innerHTML=rest.slice(0,7).map(p=>`<li><div class="meta">${p.t.split(', ')[1]} · ${p.t.split(', ')[0]}</div><h3><a href="${p.url}" target="_blank" rel="noopener">${brk(p.text)?'<span class="kick">Breaking </span>':''}${esc(head(p.text))}</a></h3></li>`).join('');
 document.getElementById('more').innerHTML=rest.slice(7).map(p=>`<article class="card"><a href="${p.url}" target="_blank" rel="noopener">${p.img?`<img loading="lazy" src="${p.img}" alt="Image from the @CocoPostel post">`:''}<h3>${esc(head(p.text))}</h3></a><p>${esc(trim(body(p.text),180))}</p><div class="meta">${p.t}</div></article>`).join('');
}
document.querySelectorAll('#tabs button').forEach(b=>b.onclick=()=>{document.querySelectorAll('#tabs button').forEach(x=>x.classList.remove('on'));b.classList.add('on');render(b.dataset.t)});
render('all');
const tk=P.filter(p=>brk(p.text)).slice(0,8).map(p=>`<a href="${p.url}" target="_blank" rel="noopener">${esc(head(p.text))}</a>`).join('');
document.getElementById('ticker').innerHTML=tk+tk;
document.getElementById('dateline').textContent='London · '+new Date().toLocaleDateString('en-GB',{timeZone:'Europe/London',weekday:'long',day:'numeric',month:'long',year:'numeric'});
setTimeout(()=>{if(!document.querySelector('#live iframe'))document.getElementById('fallback').hidden=false},6000);

fetch('assets/reports.json?v='+Date.now()).then(r=>r.json()).then(R=>{document.getElementById('reports').innerHTML=R.map(r=>`<article class="card"><div class="kick">News</div><h3>${esc(r.title)}</h3><p>${esc(r.summary)}</p><div class="meta">${r.t} GMT</div></article>`).join('')}).catch(()=>{document.getElementById('press').hidden=true});
