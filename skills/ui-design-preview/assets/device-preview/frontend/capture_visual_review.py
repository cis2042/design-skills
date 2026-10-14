from pathlib import Path
from playwright.sync_api import sync_playwright,expect
root=Path(__file__).resolve().parent/'evidence/visual-review';root.mkdir(exist_ok=True)
with sync_playwright() as p:
 b=p.chromium.launch(executable_path='/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',headless=True)
 q=b.new_page(viewport={'width':1900,'height':1400})
 for theme in ['light','dark']:
  for scene in ['chat','discover','settings','model-detail','search','general','agents','conversation']:
   q.goto('http://127.0.0.1:8871/docs/functional-design/prototypes/agent-workbench/review.html?page='+scene+'&theme='+theme)
   for device in ['phone','pad']:
    expect(q.frame_locator('#'+device).locator('.application')).to_be_visible()
    q.frame_locator('#'+device).locator('.application').screenshot(path=str(root/(device+'-'+scene+'-'+theme+'.png')))
 print('Captured 32 device screenshots')
 b.close()
