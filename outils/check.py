import asyncio,sys,re,os
from playwright.async_api import async_playwright
BASE=sys.argv[1]; WS=[int(x) for x in sys.argv[2].split(',')]
PAGES=['index.html','prestations.html','a-propos.html','contact.html','mentions-legales.html']
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch()
        for pgn in PAGES:
            for w in WS:
                pg=await b.new_page(viewport={'width':w,'height':900 if w>=768 else 800})
                errs=[]
                pg.on('console',lambda m:errs.append(m.text) if m.type=='error' else None)
                pg.on('requestfailed',lambda r:errs.append('FAIL '+r.url) if 'fonts.g' not in r.url else None)
                await pg.goto(BASE+pgn,wait_until='load'); await pg.wait_for_timeout(400)
                await pg.evaluate("document.querySelectorAll('img[loading=lazy]').forEach(i=>i.loading='eager')"); await pg.wait_for_timeout(500)
                r=await pg.evaluate("""()=>{const d=document.documentElement;const bad=[...document.images].filter(i=>!i.naturalWidth).length;
                 const small=[...document.querySelectorAll('p,li,a,dd,dt,label,span,pre,h3,button')].filter(e=>e.children.length==0&&e.textContent.trim()&&getComputedStyle(e).display!='none'&&parseFloat(getComputedStyle(e).fontSize)<15.9).map(e=>e.tagName+'.'+e.className+':'+getComputedStyle(e).fontSize);
                 const h1=document.querySelectorAll('h1').length;
                 const hd=document.querySelector('.nav').getBoundingClientRect();
                 const lg=document.querySelector('.logo').getBoundingClientRect(),cta=document.querySelector('.nav-cta').getBoundingClientRect(),bg=document.querySelector('.burger').getBoundingClientRect();
                 const over=lg.right>cta.left+1||(getComputedStyle(document.querySelector('.burger')).display!='none'&&cta.right>bg.left+1);
                 const ft=document.querySelector('.site-footer').getBoundingClientRect().height/innerHeight;
                 return {sw:d.scrollWidth,H:d.scrollHeight/innerHeight,bad,small:small.slice(0,3),h1,over,ft:ft}}""")
                flag=[]
                if r['sw']>w: flag.append('H-SCROLL')
                if r['bad']: flag.append('IMGBAD')
                if r['small']: flag.append('SMALL'+str(r['small']))
                if r['h1']!=1: flag.append('H1')
                if r['over']: flag.append('NAV-OVERLAP')
                if r['ft']>0.3: flag.append('FOOTER %.2f'%r['ft'])
                if errs: flag.append(str(errs[:2]))
                print(pgn,w,'%.1f ecrans'%r['H'],'OK' if not flag else flag)
                await pg.screenshot(path=f"/home/claude/work/s_{pgn[:-5]}_{w}.png",full_page=True)
                await pg.close()
        # liens
        pg=await b.new_page(); bad=[]
        for pgn in PAGES:
            await pg.goto(BASE+pgn)
            hrefs=await pg.evaluate("[...document.querySelectorAll('a[href]')].map(a=>a.getAttribute('href'))")
            for h in set(hrefs):
                if h.startswith(('tel:','sms:','http')) or h=='#': continue
                f=h.split('#')[0]
                if f and not os.path.exists('/home/claude/antoine-garden-care/'+f): bad.append((pgn,h))
                if '#' in h:
                    t=h.split('#')[1]; tp=f or pgn
                    if t and 'id="%s"'%t not in open('/home/claude/antoine-garden-care/'+tp).read(): bad.append((pgn,h))
        print('liens morts:',bad)
        await b.close()
asyncio.run(main())
