from pathlib import Path
import json
from playwright.sync_api import sync_playwright,expect
root=Path(__file__).resolve().parent
with sync_playwright() as p:
 b=p.chromium.launch(executable_path='/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',headless=True)
 q=b.new_page(viewport={'width':1800,'height':1400});count=0
 for theme in ['light','dark']:
  q.goto('http://127.0.0.1:8871/docs/functional-design/prototypes/agent-workbench/review.html?page=drawer&theme='+theme)
  expect(q.frame_locator('#phone').locator('.drawer')).to_be_visible()
  for device,presets in json.loads((root/'src/device_presets.json').read_text()).items():
   for ident,label,w,h in presets:
    for orientation in ['portrait'] if ident=='nest-hub-max' else ['portrait','landscape']:
     width,height=(w,h) if orientation=='portrait' else (h,w)
     q.locator('#'+device).evaluate('(e,s)=>{e.style.width=s[0]+"px";e.style.height=s[1]+"px"}',[width,height])
     frame=q.frame(name=device)
     positions=[]
     for end in [False,True]:
      positions.append(frame.evaluate('''end=>{const scroll=document.querySelector('.drawer-scroll');scroll.scrollTop=end?scroll.scrollHeight:0;const footer=document.querySelector('.drawer>.rail-bottom');const r=footer.getBoundingClientRect();const btn=footer.querySelector('button').getBoundingClientRect();const s=scroll.getBoundingClientRect();return {top:r.top,bottom:r.bottom,btnBottom:btn.bottom,scrollBottom:s.bottom,height:innerHeight};}''',end))
     for r in positions:
      assert r['bottom']<=height+1 and r['btnBottom']<height and r['top']>=0 and r['scrollBottom']<=r['top']+1,(device,label,orientation,r)
     assert abs(positions[0]['top']-positions[1]['top'])<1
     count+=1
  q.screenshot(path=str(root/('evidence/drawer-fixed-footer-'+theme+'.png')),full_page=True)
  q.frame_locator('#phone').locator('.drawer>.rail-bottom').get_by_role('button',name='设置',exact=True).click()
  expect(q.frame_locator('#pad').locator('.header-context')).to_contain_text('设置')
 print('PASS',count,'drawer footer bounds and scroll isolation; settings navigation sync')
 b.close()
