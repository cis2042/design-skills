from pathlib import Path
from playwright.sync_api import sync_playwright,expect
import json
root=Path(__file__).resolve().parent
with sync_playwright() as p:
 b=p.chromium.launch(executable_path='/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',headless=True)
 q=b.new_page(viewport={'width':1280,'height':1400});checks=[]
 def load(scene,theme):
  q.goto('http://127.0.0.1:8871/docs/functional-design/prototypes/agent-workbench/review.html?page='+scene+'&theme='+theme)
  expect(q.frame_locator('#phone').locator('.app-header')).to_be_visible()
 for theme in ['dark','light']:
  load('settings',theme)
  for device in ['phone','pad']:
   f=q.frame_locator('#'+device)
   for row in f.locator('.setting-group .entity-row').all():
    assert row.evaluate('(e)=>e.getBoundingClientRect().height')<=56,'Settings rows too tall'
   for button in f.locator('.app-header button').all():
    size=button.evaluate('(e)=>[e.offsetWidth,e.offsetHeight]')
    assert size==[40,40],(device,size)
   checks.append(device+' settings geometry '+theme)
  q.screenshot(path=str(root/'evidence'/('settings-stable-'+theme+'.png')),full_page=True)
  load('general',theme)
  for device in ['phone','pad']:
   f=q.frame_locator('#'+device);input=f.get_by_role('textbox',name='HTTP 代理',exact=True)
   before=input.bounding_box();input.focus();input.fill('http://localhost:7890')
   after=input.bounding_box()
   assert before==after,(device,before,after)
  load('agents',theme)
  phone=q.frame_locator('#phone');pad=q.frame_locator('#pad')
  before=[f.locator('.app-header').bounding_box() for f in [phone,pad]]
  phone.get_by_role('button',name='新建',exact=True).click()
  phone.get_by_role('button',name='取消',exact=True).click()
  q.wait_for_timeout(400)
  after=[f.locator('.app-header').bounding_box() for f in [phone,pad]]
  assert before==after
  checks.append('focus, input, modal closure stable '+theme)
 assert checks
 (root/'evidence/layout-stability.json').write_text(json.dumps({'passed':True,'checks':checks},ensure_ascii=False,indent=2))
 print('PASS',checks)
 b.close()
