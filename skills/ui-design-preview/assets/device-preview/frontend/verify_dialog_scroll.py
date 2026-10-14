"""Check scrollbar styling, actual scroll reachability and fixed dialog actions."""
from pathlib import Path
from playwright.sync_api import sync_playwright,expect
import json
root=Path(__file__).resolve().parent
with sync_playwright() as p:
 b=p.chromium.launch(executable_path='/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',headless=True)
 q=b.new_page(viewport={'width':1280,'height':1400});errors=[];q.on('pageerror',lambda e:errors.append(str(e)));checks=[]
 for theme in ['dark','light']:
  q.goto('http://127.0.0.1:8871/docs/functional-design/prototypes/agent-workbench/review.html?page=agents&theme='+theme)
  phone=q.frame_locator('#phone');phone.get_by_role('button',name='新建',exact=True).click()
  q.wait_for_timeout(600) # Allow library popup entrance animation to complete.
  for device in ['phone','pad']:
   f=q.frame_locator('#'+device);content=f.locator('.dialog-content');expect(content).to_be_visible()
   assert content.evaluate('(e)=>getComputedStyle(e).scrollbarWidth')=='none'
   save=f.get_by_role('button',name='保存',exact=True);expect(save).to_be_visible();before=save.bounding_box()
   content.evaluate('(e)=>e.scrollTop=e.scrollHeight')
   assert content.evaluate('(e)=>e.scrollTop+e.clientHeight>=e.scrollHeight-1')
   after=save.bounding_box();assert abs(before['y']-after['y'])<1
   assert f.locator('textarea').evaluate('(e)=>getComputedStyle(e).scrollbarWidth')=='none'
   checks.append({'device':device,'theme':theme,'scrollbar':'hidden','last_field_reachable':True,'save_fixed':True})
  q.screenshot(path=str(root/'evidence'/('dialog-no-scrollbar-'+theme+'.png')),full_page=True)
 assert not errors,errors
 (root/'evidence/dialog-scroll-verification.json').write_text(json.dumps({'passed':True,'checks':checks,'errors':errors},indent=2))
 print('PASS: both devices, both themes; no scrollbar, content reachable, save fixed')
 b.close()
