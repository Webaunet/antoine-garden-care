import asyncio
from playwright.async_api import async_playwright
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch()
        for w,h in [(1440,900),(900,1000),(390,844)]:
            pg=await b.new_page(viewport={'width':w,'height':h})
            errs=[]
            pg.on('console',lambda m:errs.append(m.text) if m.type=='error' else None)
            await pg.goto('file:///home/claude/antoine-garden-care/index.html')
            await pg.wait_for_timeout(800)
            sw=await pg.evaluate('document.documentElement.scrollWidth')
            H=await pg.evaluate('document.documentElement.scrollHeight')
            bad=await pg.evaluate("[...document.images].filter(i=>i.loading!='lazy'&&!i.naturalWidth).length")
            print(w,'scrollW',sw,'height/screen',round(H/h,1),'errs',[e for e in errs if 'fonts' not in e][:2])
            await pg.screenshot(path=f'full{w}.png',full_page=True)
        await b.close()
asyncio.run(main())
