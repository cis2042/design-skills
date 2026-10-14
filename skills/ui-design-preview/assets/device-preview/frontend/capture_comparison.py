from pathlib import Path
from playwright.sync_api import sync_playwright,expect
root=Path(__file__).resolve().parent/'evidence/visual-review'
with sync_playwright() as p:
 b=p.chromium.launch(executable_path='/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',headless=True)
 q=b.new_page(viewport={'width':1900,'height':1400})
 for scene,device,w,h,theme in [('chat','pad',768,1024,'dark'),('settings','phone',390,884,'dark'),('general','pad',768,1024,'light'),('discover','pad',768,1024,'dark')]:
  q.goto('http://127.0.0.1:8871/docs/functional-design/prototypes/agent-workbench/review.html?page='+scene+'&theme='+theme)
  expect(q.frame_locator('#'+device).locator('.application')).to_be_visible()
  q.locator('#'+device).evaluate('(e,s)=>{e.style.width=s[0]+"px";e.style.height=s[1]+"px";e.style.transform="none";e.parentElement.style.height=s[1]+"px"}',[w,h])
  q.frame_locator('#'+device).locator('.application').screenshot(path=str(root/('compare-'+scene+'.png')))
 b.close()
