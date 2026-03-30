code = open('world.html').read()
start = code.find('\nfunction drawTile(ctx, tile, px, py, mx, my)')
end = code.find('\n\n// ── 16-BIT PLAYER SPRITE')

NEW = """
function drawTile(ctx, tile, px, py, mx, my) {
  const pal = getRegionPal(tile);
  const T = TILE;
  ctx.fillStyle = pal.base;
  ctx.fillRect(px, py, T, T);
}

function drawTileDetail(ctx, tile, px, py, mx, my) {
  const pal = getRegionPal(tile);
  const af  = animFrame;
  const T   = TILE;
  const s   = (mx*17+my*13)%12;
  const alt = (mx+my)%2;

  if (tile === T.GROUND) {
    ctx.fillStyle = alt ? pal.base : pal.sh;
    ctx.fillRect(px, py, T, T);
    ctx.fillStyle = pal.hi;
    if(s<3){ ctx.beginPath(); ctx.ellipse(px+s*8+6,py+s*6+8,5,3,0,0,Math.PI*2); ctx.fill(); }
    if(s>8){ ctx.beginPath(); ctx.ellipse(px+T-s*2-4,py+T-s*2-6,4,2,0.3,0,Math.PI*2); ctx.fill(); }
    ctx.fillStyle = pal.sh;
    if(s===4||s===7){ ctx.beginPath(); ctx.ellipse(px+T/2+s,py+T/2-s+4,6,3,0.2,0,Math.PI*2); ctx.fill(); }
  }

  else if (tile === T.GRASS) {
    ctx.fillStyle = pal.base; ctx.fillRect(px,py,T,T);
    const sw  = Math.sin(af*0.03+mx*0.8)*2;
    const sw2 = Math.sin(af*0.04+my*0.7)*2;
    ctx.fillStyle = pal.sh;
    ctx.beginPath(); ctx.ellipse(px+10,py+36,10,7,0,0,Math.PI*2); ctx.fill();
    ctx.beginPath(); ctx.ellipse(px+28,py+38,12,7,0,0,Math.PI*2); ctx.fill();
    ctx.beginPath(); ctx.ellipse(px+42,py+34,8,6,0,0,Math.PI*2); ctx.fill();
    ctx.fillStyle = pal.base;
    ctx.beginPath(); ctx.ellipse(px+10+sw,py+28,10,10,0,0,Math.PI*2); ctx.fill();
    ctx.beginPath(); ctx.ellipse(px+28+sw2,py+26,13,11,0,0,Math.PI*2); ctx.fill();
    ctx.beginPath(); ctx.ellipse(px+42+sw,py+24,9,10,0,0,Math.PI*2); ctx.fill();
    ctx.fillStyle = pal.hi;
    ctx.beginPath(); ctx.ellipse(px+9+sw,py+20,8,8,0,0,Math.PI*2); ctx.fill();
    ctx.beginPath(); ctx.ellipse(px+27+sw2,py+17,11,9,0,0,Math.PI*2); ctx.fill();
    ctx.beginPath(); ctx.ellipse(px+41+sw,py+16,7,8,0,0,Math.PI*2); ctx.fill();
    ctx.fillStyle = pal.acc;
    ctx.beginPath(); ctx.ellipse(px+9+sw,py+16,5,5,0,0,Math.PI*2); ctx.fill();
    ctx.beginPath(); ctx.ellipse(px+27+sw2,py+12,7,6,0,0,Math.PI*2); ctx.fill();
    ctx.beginPath(); ctx.ellipse(px+41+sw,py+11,4,5,0,0,Math.PI*2); ctx.fill();
  }

  else if (tile === T.TREE) {
    ctx.fillStyle = pal.base; ctx.fillRect(px,py,T,T);
    ctx.fillStyle='#4a3010';
    ctx.beginPath(); ctx.roundRect(px+18,py+30,12,18,2); ctx.fill();
    ctx.fillStyle='#6a4820';
    ctx.beginPath(); ctx.roundRect(px+20,py+30,7,18,2); ctx.fill();
    ctx.fillStyle='#3a2008';
    ctx.beginPath(); ctx.ellipse(px+24,py+46,14,5,0,0,Math.PI*2); ctx.fill();
    ctx.fillStyle=pal.sh;
    ctx.beginPath(); ctx.ellipse(px+24,py+22,20,16,0,0,Math.PI*2); ctx.fill();
    ctx.beginPath(); ctx.ellipse(px+14,py+18,12,10,0,0,Math.PI*2); ctx.fill();
    ctx.beginPath(); ctx.ellipse(px+35,py+20,11,9,0,0,Math.PI*2); ctx.fill();
    ctx.fillStyle=pal.base;
    ctx.beginPath(); ctx.ellipse(px+24,py+18,18,14,0,0,Math.PI*2); ctx.fill();
    ctx.beginPath(); ctx.ellipse(px+14,py+14,11,9,0,0,Math.PI*2); ctx.fill();
    ctx.beginPath(); ctx.ellipse(px+35,py+16,10,8,0,0,Math.PI*2); ctx.fill();
    ctx.fillStyle=pal.hi;
    ctx.beginPath(); ctx.ellipse(px+24,py+13,13,10,0,0,Math.PI*2); ctx.fill();
    ctx.beginPath(); ctx.ellipse(px+15,py+10,8,7,0,0,Math.PI*2); ctx.fill();
    ctx.beginPath(); ctx.ellipse(px+34,py+11,7,6,0,0,Math.PI*2); ctx.fill();
    ctx.fillStyle=pal.acc;
    ctx.beginPath(); ctx.ellipse(px+23,py+8,8,6,0,0,Math.PI*2); ctx.fill();
    ctx.beginPath(); ctx.ellipse(px+15,py+6,5,4,0,0,Math.PI*2); ctx.fill();
  }

  else if (tile === T.FLOWER) {
    ctx.fillStyle=pal.base; ctx.fillRect(px,py,T,T);
    ctx.fillStyle=pal.hi;
    if(s<4){ ctx.beginPath(); ctx.ellipse(px+s*6+4,py+s*4+4,4,2,0,0,Math.PI*2); ctx.fill(); }
    ctx.fillStyle='#2a8814'; ctx.fillRect(px+8,py+28,2,14); ctx.fillRect(px+24,py+26,2,16); ctx.fillRect(px+38,py+30,2,12);
    const fc=(mx+my)%3===0?'#ffdd00':(mx+my)%3===1?'#ff5577':'#eeeeff';
    const fc2=(mx+my)%3===0?'#ffa000':(mx+my)%3===1?'#ff88aa':'#aaaaff';
    ctx.fillStyle=fc;
    ctx.beginPath(); ctx.ellipse(px+9,py+24,7,6,0,0,Math.PI*2); ctx.fill();
    ctx.beginPath(); ctx.ellipse(px+25,py+21,7,6,0,0,Math.PI*2); ctx.fill();
    ctx.fillStyle=fc2;
    ctx.beginPath(); ctx.ellipse(px+39,py+25,6,5,0,0,Math.PI*2); ctx.fill();
    ctx.fillStyle='#ffffaa';
    ctx.beginPath(); ctx.ellipse(px+9,py+24,2,2,0,0,Math.PI*2); ctx.fill();
    ctx.beginPath(); ctx.ellipse(px+25,py+21,2,2,0,0,Math.PI*2); ctx.fill();
  }

  else if (tile === T.WATER) {
    const w1 = (af*0.8+mx*14)%T;
    const w2 = (af*0.6+my*11+8)%T;
    ctx.fillStyle='#1040a0'; ctx.fillRect(px,py,T,T);
    ctx.fillStyle='#1858c0'; ctx.fillRect(px,py+4,T,T-8);
    ctx.fillStyle='#2070d8'; ctx.fillRect(px,py+8,T,T/2);
    ctx.fillStyle='#3888ee';
    ctx.fillRect(px,py+Math.floor(w1*0.4)+4,T,3);
    ctx.fillRect(px,py+Math.floor(w2*0.35)+16,T,2);
    ctx.fillRect(px,py+Math.floor(w1*0.25)+28,T,2);
    ctx.fillStyle='rgba(255,255,255,0.7)';
    const sx1=(w1+mx*9)%40+3, sx2=(w2+my*7)%36+6;
    ctx.beginPath(); ctx.ellipse(px+sx1,py+14,3,2,0,0,Math.PI*2); ctx.fill();
    ctx.beginPath(); ctx.ellipse(px+sx2,py+30,2,1.5,0,0,Math.PI*2); ctx.fill();
    if((mx*7+my*11)%8===0){
      ctx.fillStyle='#206a28'; ctx.beginPath(); ctx.ellipse(px+12,py+26,9,6,0.3,0,Math.PI*2); ctx.fill();
      ctx.fillStyle='#2a8a34'; ctx.beginPath(); ctx.ellipse(px+12,py+25,7,5,0.3,0,Math.PI*2); ctx.fill();
      ctx.fillStyle='#ff8899'; ctx.beginPath(); ctx.ellipse(px+13,py+23,2,2,0,0,Math.PI*2); ctx.fill();
    }
    if((mx*5+my*9)%10===0){
      ctx.fillStyle='#206a28'; ctx.beginPath(); ctx.ellipse(px+34,py+34,8,5,0.5,0,Math.PI*2); ctx.fill();
      ctx.fillStyle='#2a8a34'; ctx.beginPath(); ctx.ellipse(px+34,py+33,6,4,0.5,0,Math.PI*2); ctx.fill();
    }
    if((af+mx*3+my*7)%40<3){ ctx.fillStyle='#ffffff'; ctx.beginPath(); ctx.ellipse(px+T/3,py+T/4,2,2,0,0,Math.PI*2); ctx.fill(); }
  }

  else if (tile === T.PATH) {
    ctx.fillStyle='#888060'; ctx.fillRect(px,py,T,T);
    const ox = my%2 ? 0 : 11;
    ctx.fillStyle = alt ? '#b0a888':'#a49870';
    ctx.beginPath(); ctx.roundRect(px+2,py+3,20,19,3); ctx.fill();
    ctx.beginPath(); ctx.roundRect(px+25,py+3,20,19,3); ctx.fill();
    ctx.beginPath(); ctx.roundRect(px+2+ox,py+25,20,19,3); ctx.fill();
    ctx.beginPath(); ctx.roundRect(px+25+ox,py+25,20,19,3); ctx.fill();
    ctx.fillStyle='#ccc0a0';
    ctx.fillRect(px+4,py+5,16,4); ctx.fillRect(px+27,py+5,16,4);
    ctx.fillRect(px+4+ox,py+27,16,4); ctx.fillRect(px+27+ox,py+27,16,4);
    ctx.fillStyle='#706850';
    ctx.fillRect(px+2,py+21,20,2); ctx.fillRect(px+25,py+21,20,2);
  }

  else if (tile === T.WALL) {
    ctx.fillStyle='#6a5840'; ctx.fillRect(px,py,T,T);
    const rw=my%2;
    ctx.fillStyle=alt?'#8a7858':'#7a6848';
    ctx.beginPath(); ctx.roundRect(px+(rw?1:T/2+1),py+2,T/2-3,T/2-4,2); ctx.fill();
    ctx.beginPath(); ctx.roundRect(px+(rw?T/2+1:1),py+T/2+2,T/2-3,T/2-4,2); ctx.fill();
    ctx.fillStyle='rgba(176,152,128,0.45)';
    ctx.fillRect(px+(rw?2:T/2+2),py+3,T/2-7,4);
    ctx.fillRect(px+(rw?T/2+2:2),py+T/2+3,T/2-7,4);
    ctx.fillStyle='#403828';
    ctx.fillRect(px,py+T/2-1,T,3);
    ctx.fillRect(px+(rw?T/2-1:0),py,2,T/2);
    ctx.fillRect(px+(rw?0:T/2-1),py+T/2+2,2,T/2);
    if((mx*11+my*7)%6===0){ ctx.fillStyle='#4a6828'; ctx.beginPath(); ctx.ellipse(px+6,py+10,4,2,0,0,Math.PI*2); ctx.fill(); }
    if((mx*9+my*13)%7===0){ ctx.fillStyle='#3a5018'; ctx.beginPath(); ctx.ellipse(px+T-8,py+T/2+6,3,2,0,0,Math.PI*2); ctx.fill(); }
  }

  else if (tile === T.CAVE) {
    ctx.fillStyle='#3a2830'; ctx.fillRect(px,py,T,T);
    ctx.fillStyle='#5a4048'; ctx.beginPath(); ctx.roundRect(px+2,py+2,T-4,T-4,4); ctx.fill();
    ctx.fillStyle='#080008';
    ctx.beginPath(); ctx.arc(px+T/2,py+T/2+2,T/3,Math.PI,0); ctx.lineTo(px+T/2+T/3,py+T-4); ctx.lineTo(px+T/2-T/3,py+T-4); ctx.fill();
    const cg=Math.sin(af*0.04)*0.2+0.3;
    ctx.fillStyle='rgba(120,0,180,'+cg+')';
    ctx.beginPath(); ctx.arc(px+T/2,py+T/2+2,T/4,Math.PI,0); ctx.lineTo(px+T/2+T/4,py+T-4); ctx.lineTo(px+T/2-T/4,py+T-4); ctx.fill();
    ctx.fillStyle='#7a6068';
    ctx.beginPath(); ctx.ellipse(px+6,py+8,5,4,0.3,0,Math.PI*2); ctx.fill();
    ctx.beginPath(); ctx.ellipse(px+T-8,py+10,4,4,0.5,0,Math.PI*2); ctx.fill();
    ctx.fillStyle='#4a3848';
    [[10,4,3,8],[18,4,2,6],[28,4,3,9],[38,4,2,6]].forEach(function(a){
      ctx.beginPath(); ctx.moveTo(px+a[0],py+a[1]); ctx.lineTo(px+a[0]+a[2],py+a[1]); ctx.lineTo(px+a[0]+a[2]/2,py+a[1]+a[3]); ctx.fill();
    });
  }

  else if (tile === T.SHRINE) {
    ctx.fillStyle='#706840'; ctx.fillRect(px,py,T,T);
    ctx.fillStyle='#806030'; ctx.beginPath(); ctx.roundRect(px+4,py+32,T-8,12,3); ctx.fill();
    ctx.fillStyle='#a07840'; ctx.beginPath(); ctx.roundRect(px+7,py+30,T-14,6,2); ctx.fill();
    ctx.fillStyle='#908040'; ctx.beginPath(); ctx.roundRect(px+18,py+8,12,24,2); ctx.fill();
    ctx.fillStyle='#b0a050'; ctx.beginPath(); ctx.roundRect(px+20,py+8,7,24,2); ctx.fill();
    ctx.fillStyle='#c09838';
    ctx.beginPath(); ctx.moveTo(px+8,py+10); ctx.lineTo(px+T-8,py+10); ctx.lineTo(px+T-4,py+16); ctx.lineTo(px+4,py+16); ctx.fill();
    ctx.fillStyle='#e0b840';
    ctx.beginPath(); ctx.moveTo(px+10,py+4); ctx.lineTo(px+T-10,py+4); ctx.lineTo(px+T-6,py+10); ctx.lineTo(px+6,py+10); ctx.fill();
    ctx.fillStyle='#ffd050';
    ctx.beginPath(); ctx.moveTo(px+14,py+1); ctx.lineTo(px+T-14,py+1); ctx.lineTo(px+T-10,py+5); ctx.lineTo(px+10,py+5); ctx.fill();
    const sg=Math.sin(af*0.05)*0.3+0.5;
    ctx.fillStyle='rgba(255,200,50,'+(sg*0.35)+')';
    ctx.beginPath(); ctx.ellipse(px+T/2,py+16,18,20,0,0,Math.PI*2); ctx.fill();
  }

  else if (tile === T.RUIN) {
    ctx.fillStyle='#585850'; ctx.fillRect(px,py,T,T);
    ctx.fillStyle='#706860'; ctx.beginPath(); ctx.roundRect(px+2,py+16,14,T-16,2); ctx.fill();
    ctx.beginPath(); ctx.roundRect(px+T-16,py+8,14,T-10,2); ctx.fill();
    ctx.fillStyle='#606058';
    [[18,34,8,6],[10,40,10,5],[28,38,7,5],[6,28,5,4]].forEach(function(a){
      ctx.beginPath(); ctx.ellipse(px+a[0],py+a[1],a[2]/2,a[3]/2,s*0.3,0,Math.PI*2); ctx.fill();
    });
    ctx.fillStyle='#888878'; ctx.fillRect(px+3,py+17,8,3); ctx.fillRect(px+T-15,py+9,8,3);
    ctx.fillStyle='#3a6020';
    if(s<4){ ctx.beginPath(); ctx.ellipse(px+5,py+22,5,3,0.2,0,Math.PI*2); ctx.fill(); }
    ctx.strokeStyle='#282818'; ctx.lineWidth=1;
    ctx.beginPath(); ctx.moveTo(px+4,py+20); ctx.lineTo(px+6,py+28); ctx.lineTo(px+5,py+34); ctx.stroke();
  }

  else if (tile === T.NEST) {
    ctx.fillStyle=pal.base; ctx.fillRect(px,py,T,T);
    ctx.fillStyle='#6a3e18'; ctx.beginPath(); ctx.ellipse(px+T/2,py+30,18,8,0,0,Math.PI*2); ctx.fill();
    ctx.fillStyle='#7a4e24'; ctx.beginPath(); ctx.ellipse(px+T/2,py+28,16,7,0,0,Math.PI*2); ctx.fill();
    ctx.fillStyle='#4a2808'; ctx.beginPath(); ctx.ellipse(px+T/2,py+26,12,5,0,0,Math.PI*2); ctx.fill();
    const np=Math.sin(af*0.07)*0.4+0.7;
    ctx.fillStyle='rgba(255,190,0,'+(np*0.35)+')'; ctx.beginPath(); ctx.ellipse(px+T/2,py+14,14,16,0,0,Math.PI*2); ctx.fill();
    ctx.fillStyle='#ffe050'; ctx.beginPath(); ctx.ellipse(px+T/2,py+14,10,12,0,0,Math.PI*2); ctx.fill();
    ctx.fillStyle='#fff888'; ctx.beginPath(); ctx.ellipse(px+T/2-2,py+10,4,5,0.3,0,Math.PI*2); ctx.fill();
  }

  else if (tile === T.CHEST) {
    ctx.fillStyle=pal.base; ctx.fillRect(px,py,T,T);
    ctx.fillStyle='#7a5018'; ctx.beginPath(); ctx.roundRect(px+8,py+22,T-16,T-26,3); ctx.fill();
    ctx.fillStyle='#9a6828'; ctx.beginPath(); ctx.roundRect(px+10,py+24,T-20,T-30,2); ctx.fill();
    ctx.fillStyle='#c09030'; ctx.beginPath(); ctx.roundRect(px+8,py+12,T-16,12,3); ctx.fill();
    ctx.fillStyle='#e0b040'; ctx.beginPath(); ctx.roundRect(px+10,py+13,T-20,6,2); ctx.fill();
    ctx.fillStyle='#ffd840'; ctx.beginPath(); ctx.roundRect(px+T/2-5,py+22,10,8,2); ctx.fill();
    ctx.fillStyle='#fff080'; ctx.beginPath(); ctx.ellipse(px+T/2,py+25,3,3,0,0,Math.PI*2); ctx.fill();
    ctx.fillStyle='#d0a030';
    [[8,12],[T-12,12],[8,T-10],[T-12,T-10]].forEach(function(a){ ctx.beginPath(); ctx.ellipse(px+a[0],py+a[1],3,3,0,0,Math.PI*2); ctx.fill(); });
  }

  else if (tile === T.TOWN) {
    ctx.fillStyle='#a09878'; ctx.fillRect(px,py,T,T);
    ctx.fillStyle=alt?'#b8b090':'#a8a080';
    ctx.beginPath(); ctx.roundRect(px+1,py+1,T/2-2,T/2-2,2); ctx.fill();
    ctx.beginPath(); ctx.roundRect(px+T/2+1,py+1,T/2-2,T/2-2,2); ctx.fill();
    ctx.beginPath(); ctx.roundRect(px+1,py+T/2+1,T/2-2,T/2-2,2); ctx.fill();
    ctx.beginPath(); ctx.roundRect(px+T/2+1,py+T/2+1,T/2-2,T/2-2,2); ctx.fill();
    ctx.fillStyle='#d0c8a8';
    ctx.fillRect(px+3,py+3,T/2-6,4); ctx.fillRect(px+T/2+3,py+3,T/2-6,4);
    ctx.fillStyle='#686050'; ctx.fillRect(px,py+T/2-1,T,3); ctx.fillRect(px+T/2-1,py,3,T);
    if(s<4){ ctx.fillStyle='rgba(0,0,0,0.08)'; ctx.beginPath(); ctx.ellipse(px+s*8+6,py+s*6+6,4,3,0,0,Math.PI*2); ctx.fill(); }
  }

  else if (tile === T.SAND) {
    ctx.fillStyle=alt?'#d8c078':'#c8b068'; ctx.fillRect(px,py,T,T);
    const rip=(af*0.012+mx*0.25+my*0.18)%1;
    ctx.strokeStyle='rgba(255,255,200,0.2)'; ctx.lineWidth=2;
    const ry1=py+Math.floor(rip*T*0.5)+4;
    const ry2=py+Math.floor(rip*T*0.5)+16;
    ctx.beginPath(); ctx.moveTo(px,ry1); ctx.quadraticCurveTo(px+T/2,ry1-3,px+T,ry1); ctx.stroke();
    ctx.beginPath(); ctx.moveTo(px,ry2); ctx.quadraticCurveTo(px+T/2,ry2+3,px+T,ry2); ctx.stroke();
    if(s<4){
      ctx.fillStyle='#9a7830'; ctx.beginPath(); ctx.ellipse(px+s*9+5,py+s*7+10,4,3,s*0.3,0,Math.PI*2); ctx.fill();
      ctx.fillStyle='#c09848'; ctx.beginPath(); ctx.ellipse(px+s*9+6,py+s*7+9,2,1.5,s*0.3,0,Math.PI*2); ctx.fill();
    }
  }

  else if (tile === T.BRIDGE) {
    ctx.fillStyle='#6a4820'; ctx.fillRect(px,py,T,T);
    for(let i=0;i<5;i++){
      ctx.fillStyle=i%2?'#8a6030':'#7a5020';
      ctx.beginPath(); ctx.roundRect(px+i*10+1,py+5,9,T-10,1); ctx.fill();
      ctx.fillStyle='rgba(255,255,255,0.08)'; ctx.fillRect(px+i*10+2,py+6,5,3);
    }
    ctx.fillStyle='#c8a040'; ctx.beginPath(); ctx.roundRect(px,py+3,T,3,1); ctx.fill();
    ctx.beginPath(); ctx.roundRect(px,py+T-6,T,3,1); ctx.fill();
    ctx.fillStyle='#a08030'; ctx.fillRect(px,py+5,T,1); ctx.fillRect(px,py+T-4,T,1);
  }

  else if (tile === T.MINIBOSS) {
    const pulse=Math.sin(af*0.08)*0.35+0.55;
    ctx.fillStyle='#200404'; ctx.fillRect(px,py,T,T);
    ctx.fillStyle='rgba(255,40,20,'+(pulse*0.4)+')'; ctx.fillRect(px,py,T,T);
    ctx.strokeStyle='rgba(255,60,0,'+pulse+')'; ctx.lineWidth=2; ctx.strokeRect(px+2,py+2,T-4,T-4);
    ctx.fillStyle='rgba(255,120,0,'+pulse+')';
    ctx.beginPath(); ctx.moveTo(px+T/2,py+6); ctx.lineTo(px+T/2+10,py+28); ctx.lineTo(px+T/2-10,py+28); ctx.fill();
    ctx.beginPath(); ctx.moveTo(px+T/2,py+T-6); ctx.lineTo(px+T/2+10,py+T-28); ctx.lineTo(px+T/2-10,py+T-28); ctx.fill();
  }

  else if (tile === T.BOSS) {
    const pulse=Math.sin(af*0.05)*0.4+0.6;
    ctx.fillStyle='#100008'; ctx.fillRect(px,py,T,T);
    ctx.fillStyle='rgba(200,0,60,'+(pulse*0.5)+')'; ctx.fillRect(px,py,T,T);
    for(let r=3;r<18;r+=4){ ctx.strokeStyle='rgba(255,0,80,'+(pulse*(1-r/20))+')'; ctx.lineWidth=1.5; ctx.strokeRect(px+r,py+r,T-r*2,T-r*2); }
    ctx.fillStyle='rgba(255,20,80,'+pulse+')';
    ctx.beginPath(); ctx.moveTo(px+T/2,py+4); ctx.lineTo(px+T-8,py+20); ctx.lineTo(px+T-4,py+T-6); ctx.lineTo(px+4,py+T-6); ctx.lineTo(px+8,py+20); ctx.fill();
  }

  else if (tile === T.SIGN) {
    ctx.fillStyle=pal.base; ctx.fillRect(px,py,T,T);
    ctx.fillStyle='#6a4820'; ctx.beginPath(); ctx.roundRect(px+T/2-3,py+18,6,T-18,2); ctx.fill();
    ctx.fillStyle='#aa8030'; ctx.beginPath(); ctx.roundRect(px+6,py+5,T-12,16,3); ctx.fill();
    ctx.fillStyle='#ccA040'; ctx.beginPath(); ctx.roundRect(px+8,py+7,T-16,10,2); ctx.fill();
    ctx.fillStyle='#5a3808'; ctx.fillRect(px+10,py+9,T-20,2); ctx.fillRect(px+12,py+13,T-24,2);
    ctx.fillStyle='#888060';
    ctx.beginPath(); ctx.ellipse(px+8,py+8,3,3,0,0,Math.PI*2); ctx.fill();
    ctx.beginPath(); ctx.ellipse(px+T-8,py+8,3,3,0,0,Math.PI*2); ctx.fill();
  }
}
"""

code = code[:start] + NEW + code[end:]
open('world.html','w').write(code)
js = code[code.find('<script>'):code.find('</script>')]
print('Done. Lines:', code.count('\n'), '| Balanced:', js.count('{') == js.count('}'))
