const $=id=>document.getElementById(id);
const INR=n=>'₹'+Number(n||0).toLocaleString('en-IN',{maximumFractionDigits:2});
const NUM=n=>Number.isFinite(Number(n))?Number(n).toLocaleString('en-IN',{maximumFractionDigits:1}):'—';
const num=v=>{const n=Number(v);return Number.isFinite(n)?n:null};
const CFG={backendUrl:'',accessKey:'',selectedU:'NIFTY',selectedExpiry:'',side:'BUY',...JSON.parse(localStorage.getItem('tradepilotV3cfg')||'{}')};
let C=CFG,M={connected:false,underlyings:{},chain:[],selected:null,timer:null},P={account:{equity:100000,available:100000,openPnl:0,realized:0,estimatedCharges:0},positions:[],orders:[],rules:[]},R=null;
function saveCfg(){localStorage.setItem('tradepilotV3cfg',JSON.stringify(C))}
function backend(){return String(C.backendUrl||'').replace(/\/$/,'')}
async function api(path,opts={}){if(!backend())throw new Error('Set your private backend URL first.');const headers={'Content-Type':'application/json','X-TradePilot-Key':C.accessKey||'',...(opts.headers||{})};const r=await fetch(backend()+path,{cache:'no-store',...opts,headers});let d;try{d=await r.json()}catch{d={error:'Invalid backend response'}}if(!r.ok)throw new Error(d.error||d.message||`HTTP ${r.status}`);return d}
function paintMoney(el,v){el.textContent=INR(v);el.classList.toggle('green',v>0);el.classList.toggle('redtxt',v<0)}
function drawAccount(){paintMoney($('equity'),P.account?.equity??100000);paintMoney($('available'),P.account?.available??100000);paintMoney($('openPnl'),P.account?.openPnl??0);paintMoney($('realized'),P.account?.realized??0);const ch=Number(P.account?.estimatedCharges||0);if($('chargesNote'))$('chargesNote').textContent='Est. 2026 charges: '+INR(ch);}
function fmtChange(q){if(!q||!Number.isFinite(Number(q.ltp)))return ['—','Waiting for Angel One','muted'];const c=Number(q.netChange||0),pct=Number(q.percentChange||0);return [INR(q.ltp),(c>=0?'+':'')+c.toFixed(2)+' ('+(pct>=0?'+':'')+pct.toFixed(2)+'%)',c>=0?'green':'redtxt']}
function drawUnderlyings(){for(const [k,px,chg] of [['NIFTY','niftyPx','niftyChg'],['BANKNIFTY','bankPx','bankChg']]){const [a,b,c]=fmtChange(M.underlyings[k]);$(px).textContent=a;$(chg).textContent=b;$(chg).className='mini '+c}$('niftyCard').classList.toggle('active',C.selectedU==='NIFTY');$('bankCard').classList.toggle('active',C.selectedU==='BANKNIFTY')}
function drawConnection(msg=''){const b=$('liveBadge');if(M.connected){b.textContent='Angel One: LIVE';b.className='pill live';$('connectionNotice').className='notice good';$('connectionNotice').textContent=msg||'Connected to your private backend. Live setup radar, market prices, and paper automation run on the server even when your phone screen is closed.'}else{b.textContent='Angel One: not connected';b.className='pill off';$('connectionNotice').className='notice';$('connectionNotice').textContent=msg||'The phone app is hosted on GitHub Pages. Angel One credentials stay only on your private backend server.'}}
function drawSelected(){const c=M.selected;if(!c){$('selectedContract').textContent='Tap a CE or PE in the option chain';$('selectedContract').className='symbolbox muted';$('placeOrder').disabled=true;return}$('selectedContract').innerHTML=`<b>${c.tradingSymbol}</b><br><span class="mini muted">${c.expiry} • ${c.optionType} • LTP ${INR(c.ltp)} • lot ${c.lotSize||'—'}</span>`;$('selectedContract').className='symbolbox';$('qty').placeholder=c.lotSize?`lot ${c.lotSize}`:'quantity';$('placeOrder').disabled=!M.connected;updateOrderButton()}
function updateOrderButton(){const side=C.side||'BUY',b=$('placeOrder');b.textContent=side+' — PAPER ORDER';b.className='full '+(side==='BUY'?'buy':'sell');$('buyTab').classList.toggle('active',side==='BUY');$('sellTab').classList.toggle('active',side==='SELL')}
function drawRadar(){
  const badge=$('radarBadge'),autoBtn=$('toggleAutoTrade'),guard=$('dailyGuard'),lvls=$('radarLevels'),setupsRoot=$('radarSetups');
  if(!R){
    badge.textContent=M.connected?'Loading radar…':'Connect backend to scan';
    badge.className='pill';
    autoBtn.disabled=true;
    return;
  }
  const live=!!R.marketOpen;
  badge.textContent=live?'LIVE SCANNING (IST)':'Market Closed • Last Session';
  badge.className='pill '+(live?'live':'warn');
  const cfg=R.config||{autoTrade:false,maxDailyLoss:3000,maxDailyTrades:2};
  autoBtn.disabled=!M.connected;
  autoBtn.textContent='Auto-Paper-Trade: '+(cfg.autoTrade?'ON (1 Lot)':'OFF');
  autoBtn.className=cfg.autoTrade?'buy':'ghost';
  const d=R.daily||{todayPnl:0,maxDailyLoss:3000,killSwitchHit:false,scannerTradesToday:0,maxDailyTrades:2};
  guard.textContent=(d.killSwitchHit?'LOCKED • ':'')+'Today '+INR(d.todayPnl)+' / -'+INR(d.maxDailyLoss)+' • '+d.scannerTradesToday+'/'+d.maxDailyTrades+' auto';
  guard.className='pill '+(d.killSwitchHit?'off':(d.todayPnl>0?'live':''));

  const idx=R.indices?.[C.selectedU];
  if(idx&&idx.levels){
    const L=idx.levels,biasCls=idx.htfBias==='BULLISH'?'green':(idx.htfBias==='BEARISH'?'redtxt':'');
    const strad=idx.straddle?`${INR(idx.straddle.combined)} (${idx.straddle.strike})`:'Connect live';
    lvls.innerHTML=`
      <div class="lvl"><span>${C.selectedU} 15m Bias</span><b class="${biasCls}">${idx.htfBias}</b></div>
      <div class="lvl"><span>PDH / PDL</span><b>${NUM(L.pdh)} / ${NUM(L.pdl)}</b></div>
      <div class="lvl"><span>15m ORB</span><b>${NUM(L.orbHigh)} / ${NUM(L.orbLow)}</b></div>
      <div class="lvl"><span>5m EMA 20</span><b>${NUM(L.ema20)}</b></div>
      <div class="lvl"><span>ATR (14)</span><b>${NUM(L.atr14)} pts</b></div>
      <div class="lvl"><span>ATM Straddle</span><b>${strad}</b></div>`;
  }else{
    lvls.innerHTML='';
  }

  const list=(R.setups||[]);
  if(!list.length){
    setupsRoot.innerHTML='<div class="empty">No high-reward (1:3 R:R) setup triggered yet. Radar automatically checks every closed 5-minute candle during 9:30 AM – 2:15 PM IST.</div>';
    return;
  }
  setupsRoot.innerHTML=list.map(s=>{
    const isCe=s.direction==='CE',isLive=s.status==='LIVE';
    const optHtml=s.contract?`
      <div class="setupMetrics">
        <div class="lvl"><span>Suggested Strike</span><b>${s.contract.tradingSymbol}</b></div>
        <div class="lvl"><span>Option Entry</span><b>${INR(s.optionEntry)}</b></div>
        <div class="lvl"><span>Option SL / TG</span><b>${INR(s.optionSl)} / ${INR(s.optionTarget)}</b></div>
        <div class="lvl"><span>Est. Risk / Reward</span><b>${INR(s.estRiskInr)} / <span class="green">${INR(s.estRewardInr)}</span></b></div>
      </div>`:`<div class="mini muted" style="margin-top:6px">Spot Entry ${NUM(s.spotEntry)} • Spot SL ${NUM(s.spotSl)} • Spot Target ${NUM(s.spotTarget)} (1:${s.rr} R:R)</div>`;
    const btn=isLive&&s.contract?`<div class="positionActions"><button class="${isCe?'buy':'sell'}" style="width:100%" data-arm="${s.id}">1-TAP ARM PAPER TRADE — ${s.contract.tradingSymbol} (${s.lotSize} QTY)</button></div>`:`<div class="mini muted" style="margin-top:7px">${isLive?'Waiting for Angel One option quote…':'Last session verified signal ('+s.date+' '+s.time+' IST). Live 1-tap arming activates during market hours.'}</div>`;
    return `<div class="setupCard ${isCe?'ce':'pe'}">
      <div class="positionTop">
        <div><b>${s.index} ${s.direction} • ${s.strategy}</b><div class="mini muted">${s.date} ${s.time} IST • Spot ${NUM(s.spotEntry)} → Target ${NUM(s.spotTarget)} (SL ${NUM(s.spotSl)})</div></div>
        <span class="pill ${isLive?'live':'warn'}">${isLive?'LIVE SETUP':'LAST SESSION'}</span>
      </div>
      <div class="mini" style="margin-top:6px;color:#cfe2f7">${s.reason}</div>
      ${optHtml}
      ${btn}
    </div>`;
  }).join('');
  setupsRoot.querySelectorAll('[data-arm]').forEach(b=>b.onclick=()=>armRadarSetup(b.dataset.arm));
}
function drawChain(){const root=$('chain');if(!M.chain.length){root.innerHTML='<div class="empty">No option contracts loaded.</div>';return}const by={};for(const c of M.chain){by[c.strike]??={};by[c.strike][c.optionType]=c}const rows=Object.entries(by).sort((a,b)=>Number(a[0])-Number(b[0]));root.innerHTML=rows.map(([strike,o])=>{const ce=o.CE,pe=o.PE;const btn=c=>c?`<div class="contract" data-token="${c.token}"><div class="ltp">${INR(c.ltp)}</div><small>${c.tradingSymbol}</small></div>`:'<div></div>';return `<div class="chainRow">${btn(ce)}<div class="mini muted">CE</div><div class="strike">${Number(strike).toLocaleString('en-IN')}</div><div class="mini muted" style="text-align:right">PE</div>${btn(pe)}</div>`}).join('');root.querySelectorAll('.contract').forEach(x=>x.onclick=()=>{M.selected=M.chain.find(c=>String(c.token)===x.dataset.token);drawSelected()})}
function drawPositions(){const root=$('positions');if(!P.positions?.length){root.innerHTML='<div class="empty">No open positions.</div>';return}root.innerHTML=P.positions.map(p=>`<div class="position"><div class="positionTop"><div><b>${p.side} ${p.tradingSymbol}</b><div class="mini muted">${p.qty} qty • Entry ${INR(p.entry)} • LTP ${INR(p.ltp)}</div></div><b class="${Number(p.pnl)>=0?'green':'redtxt'}">${INR(p.pnl)}</b></div><div class="mini muted">SL ${p.sl?INR(p.sl):'—'}${p.trailed?' (TRAILED BE)':''} • Target ${p.target?INR(p.target):'—'} • ${p.source}</div><div class="positionActions"><button class="ghost" data-exit="${p.id}">EXIT PAPER POSITION</button></div></div>`).join('');root.querySelectorAll('[data-exit]').forEach(b=>b.onclick=()=>exitPosition(b.dataset.exit))}
function drawRules(){const root=$('rules');if(!P.rules?.length){root.innerHTML='<div class="empty">No automation rules armed.</div>';return}root.innerHTML=P.rules.map(r=>`<div class="position"><div class="positionTop"><b>${r.side} ${r.tradingSymbol}</b><button class="ghost" style="max-width:80px;padding:6px" data-cancel="${r.id}">Cancel</button></div><div class="mini muted">${r.triggerType==='NOW'?'Next live price':r.triggerType+' '+INR(r.triggerPrice)} • Qty ${r.qty} • SL ${r.sl||'—'} • Target ${r.target||'—'} • ${r.status}</div></div>`).join('');root.querySelectorAll('[data-cancel]').forEach(b=>b.onclick=()=>cancelRule(b.dataset.cancel))}
function drawOrders(){const root=$('orders');if(!P.orders?.length){root.innerHTML='<tr><td colspan="7" class="empty">No paper orders yet.</td></tr>';return}root.innerHTML=P.orders.slice().reverse().slice(0,60).map(o=>`<tr><td>${(o.time||'—').slice(0,19).replace('T',' ')}</td><td>${o.symbol}</td><td class="${o.side==='BUY'?'green':'redtxt'}">${o.side}</td><td>${o.qty}</td><td>${INR(o.price)}</td><td>${o.status}</td><td class="${Number(o.pnl||0)>=0?'green':'redtxt'}">${o.pnl==null?'—':INR(o.pnl)}</td></tr>`).join('')}
function drawAll(){drawAccount();drawUnderlyings();drawConnection();drawRadar();drawSelected();drawPositions();drawRules();drawOrders()}
async function state(){const d=await api('/api/paper/state');P=d;drawAccount();drawPositions();drawRules();drawOrders()}
async function loadRadar(force=false){try{R=await api('/api/scanner'+(force?'?force=1':''));drawRadar()}catch(e){if(force)alert('Radar scan error: '+e.message)}}
async function armRadarSetup(setupId){try{const d=await api('/api/scanner/arm',{method:'POST',body:JSON.stringify({setupId})});alert(d.message||'Setup armed.');await Promise.all([state(),loadRadar()])}catch(e){alert(e.message)}}
async function exitPosition(id){try{await api('/api/paper/exit',{method:'POST',body:JSON.stringify({id})});await state()}catch(e){alert(e.message)}}
async function cancelRule(id){try{await api('/api/paper/rule/cancel',{method:'POST',body:JSON.stringify({id})});await state()}catch(e){alert(e.message)}}
async function ping(){try{const d=await api('/api/config');M.connected=!!d.configured;if(!M.connected){drawConnection('Backend reached, but Angel One credentials are not configured on the private server.');return}await Promise.allSettled([loadMarket(),state(),loadRadar(true)]);await loadExpiries();drawAll()}catch(e){M.connected=false;drawAll();drawConnection('Backend connection failed: '+e.message)} }
async function loadMarket(){const d=await api('/api/underlyings');M.underlyings=d.data||{};drawUnderlyings()}
async function loadExpiries(){const d=await api('/api/expiries?underlying='+encodeURIComponent(C.selectedU));const old=C.selectedExpiry;$('expiry').innerHTML=(d.expiries||[]).map(x=>`<option value="${x}">${x}</option>`).join('')||'<option value="">No expiries</option>';C.selectedExpiry=(d.expiries||[]).includes(old)?old:(d.expiries||[])[0]||'';$('expiry').value=C.selectedExpiry;saveCfg();if(C.selectedExpiry)await loadChain()}
let chainRequest=0,chainLoading=false,tickRunning=false,tickCount=0;
async function loadChain(background=false){
  background=background===true;
  if(!M.connected||!C.selectedExpiry||(background&&chainLoading))return;
  const root=$('chain'),u=C.selectedU,expiry=C.selectedExpiry,width=$('width').value;
  const request=++chainRequest;
  chainLoading=true;
  const current=()=>request===chainRequest&&u===C.selectedU&&expiry===C.selectedExpiry&&width===$('width').value;
  if(!background)root.innerHTML='<div class="empty"><span class="spinner"></span> Loading Angel One option prices…</div>';
  try{
    const d=await api('/api/options?underlying='+encodeURIComponent(u)+'&expiry='+encodeURIComponent(expiry)+'&width='+encodeURIComponent(width));
    if(!current())return;
    const fresh=d.contracts||[];
    if(background&&root.querySelector('.contract')){
      // Keep the visible strikes and their tap targets fixed until a deliberate reload.
      const quotes=new Map(fresh.map(c=>[String(c.token),c]));
      M.chain=M.chain.map(c=>quotes.get(String(c.token))||c);
      root.querySelectorAll('.contract').forEach(el=>{
        const q=quotes.get(el.dataset.token),price=el.querySelector('.ltp');
        if(price)price.textContent=q?INR(q.ltp):'—';
      });
    }else{M.chain=fresh;drawChain();}
    if(M.selected){
      M.selected=fresh.find(c=>String(c.token)===String(M.selected.token))||null;
      drawSelected();
    }
    if(d.spot)M.underlyings[u]=d.spot;
    drawUnderlyings();
    root.title='';
  }catch(e){
    if(!current())return;
    if(background){root.title='Price refresh failed: '+e.message;}
    else{root.textContent='Unable to load option prices: '+e.message;}
  }finally{if(request===chainRequest)chainLoading=false;}
}
async function tick(){
  if(!M.connected||tickRunning)return;
  tickRunning=true;
  tickCount++;
  try{
    const jobs=[loadMarket(),state(),C.selectedExpiry?loadChain(true):Promise.resolve()];
    if(tickCount%10===0)jobs.push(loadRadar(false));
    await Promise.allSettled(jobs);
  }
  finally{tickRunning=false;}
}
async function selectUnderlying(u){C.selectedU=u;M.selected=null;saveCfg();drawAll();if(M.connected)await loadExpiries()}
$('niftyCard').onclick=()=>selectUnderlying('NIFTY');$('bankCard').onclick=()=>selectUnderlying('BANKNIFTY');
$('expiry').onchange=()=>{C.selectedExpiry=$('expiry').value;saveCfg();loadChain()};$('width').onchange=loadChain;
$('buyTab').onclick=()=>{C.side='BUY';saveCfg();updateOrderButton()};$('sellTab').onclick=()=>{C.side='SELL';saveCfg();updateOrderButton()};
$('orderType').onchange=()=>{$('limitBox').style.display=$('orderType').value==='LIMIT'?'block':'none'};
$('placeOrder').onclick=async()=>{if(!M.selected)return;const qty=num($('qty').value);if(!qty)return alert('Enter quantity.');const body={side:C.side,contract:M.selected,qty,orderType:$('orderType').value,limitPrice:num($('limitPrice').value),sl:num($('sl').value),target:num($('target').value)};try{await api('/api/paper/order',{method:'POST',body:JSON.stringify(body)});await state()}catch(e){alert(e.message)}};
$('runCommand').onclick=async()=>{const text=$('command').value.trim();if(!text)return;try{const d=await api('/api/paper/command',{method:'POST',body:JSON.stringify({command:text,expiry:C.selectedExpiry||null})});$('commandResult').textContent=d.message||'Command accepted.';$('commandResult').className='notice good';await state()}catch(e){$('commandResult').textContent='Command rejected: '+e.message;$('commandResult').className='notice bad'}};
$('toggleAutoTrade').onclick=async()=>{if(!R)return;const next=!(R.config&&R.config.autoTrade);if(next&&!confirm('Enable server-side AUTO PAPER TRADING for TradePilot Dual-Engine setups (1 lot, 1:3 R:R, -₹3,000 daily kill-switch)? Simulated paper trades only.'))return;try{await api('/api/scanner/config',{method:'POST',body:JSON.stringify({autoTrade:next})});await loadRadar(false)}catch(e){alert(e.message)}};
$('refreshRadar').onclick=()=>M.connected?loadRadar(true):ping();
$('backendUrl').value=C.backendUrl||'';$('accessKey').value=C.accessKey||'';
$('saveBackend').onclick=()=>{const v=$('backendUrl').value.trim(),k=$('accessKey').value;if(v&&!/^https:\/\//i.test(v)&&!/^http:\/\/localhost/i.test(v))return alert('Use an HTTPS backend URL. HTTP is allowed only for localhost during development.');C.backendUrl=v;C.accessKey=k;saveCfg();ping()};
$('refreshChain').onclick=()=>M.connected?loadChain():ping();$('resetAccount').onclick=async()=>{if(!confirm('Reset the server-side paper account to ₹1,00,000 and erase paper trades/rules?'))return;try{await api('/api/paper/reset',{method:'POST',body:'{}'});await Promise.all([state(),loadRadar(false)])}catch(e){alert(e.message)}};
$('goRadar').onclick=()=>document.getElementById('radar').scrollIntoView({behavior:'smooth'});$('goPositions').onclick=()=>document.getElementById('positions').scrollIntoView({behavior:'smooth'});$('goConsole').onclick=()=>document.getElementById('command').scrollIntoView({behavior:'smooth',block:'center'});$('goSettings').onclick=()=>document.getElementById('settings').scrollIntoView({behavior:'smooth'});
let installPrompt=null;window.addEventListener('beforeinstallprompt',e=>{e.preventDefault();installPrompt=e;$('installBtn').style.display='block'});$('installBtn').onclick=async()=>{if(!installPrompt)return;installPrompt.prompt();await installPrompt.userChoice;installPrompt=null;$('installBtn').style.display='none'};
if('serviceWorker'in navigator)window.addEventListener('load',()=>navigator.serviceWorker.register('./sw.js').catch(()=>{}));
drawAll();updateOrderButton();if(C.backendUrl)ping();M.timer=setInterval(tick,3000);
