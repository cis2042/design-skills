"""Cross-device semantic parity checks against the published preview."""
from pathlib import Path
from playwright.sync_api import sync_playwright, expect
import json
root=Path(__file__).resolve().parent
scenes=['chat','conversation','work','discover','tasks','me','settings','general','appearance','model-detail','agents','plugins','mcp','skills','memory','commands','hooks','usage','search','detail']
with sync_playwright() as p:
 b=p.chromium.launch(executable_path='/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',headless=True)
 q=b.new_page(viewport={'width':1280,'height':1400});errors=[];q.on('pageerror',lambda e:errors.append(str(e)))
 def load(scene,theme='light'):
  q.goto('http://127.0.0.1:8871/docs/functional-design/prototypes/agent-workbench/review.html?page='+scene+'&theme='+theme)
  for device in ['phone','pad']:expect(q.frame_locator('#'+device).locator('.app-header')).to_be_visible()
 checks=[]
 for theme in ['light','dark']:
  for scene in scenes:
   load(scene,theme)
   headers=[q.frame_locator('#'+d).locator('.app-header') for d in ['phone','pad']]
   actions=[h.locator('button').evaluate_all('(els)=>els.map(e=>e.getAttribute("aria-label"))') for h in headers]
   assert actions[0]==actions[1],(scene,actions)
   assert headers[0].inner_text()==headers[1].inner_text(),scene
   if scene in ['chat','conversation']:
    for h in headers:
     expect(h).to_contain_text('通用 Agent')
     title=h.locator('.header-context strong').bounding_box()
     agent=h.locator('.header-agent').bounding_box()
     assert abs(title['y']+title['height']/2-agent['y']-agent['height']/2)<2, 'Header context must stay on one line'
    expect(q.frame_locator('#pad').locator('.rail').get_by_role('button',name='对话',exact=True)).to_have_attribute('aria-current','page')
    expect(q.frame_locator('#phone').locator('.adm-tab-bar-item-active')).to_contain_text('对话')
   checks.append([scene,theme])
 for scene in ['agents','plugins','skills','mcp','memory','commands','hooks']:
  load(scene)
  phone=q.frame_locator('#phone');pad=q.frame_locator('#pad')
  # Compare available directory actions, then all editor fields and footer operations.
  a=[f.locator('.content button').evaluate_all('(es)=>es.filter(e=>e.getAttribute("role")!=="switch" && e.getAttribute("aria-label")!=="范围").map(e=>e.getAttribute("aria-label")||e.textContent)') for f in [phone,pad]]
  assert a[0]==a[1],(scene,a)
  switches=[f.get_by_role('switch').evaluate_all('(es)=>es.map(e=>[e.getAttribute("aria-label"),e.getAttribute("aria-checked")])') for f in [phone,pad]]
  assert switches[0]==switches[1],(scene,switches)
  for f in [phone,pad]:expect(f.get_by_text('全部范围',exact=True)).to_be_visible()
  phone.get_by_role('button',name='新建',exact=True).click()
  dialogs=[f.get_by_role('dialog') for f in [phone,pad]]
  assert dialogs[0].locator('label').all_text_contents()==dialogs[1].locator('label').all_text_contents(),scene
  for dialog in dialogs:
   expect(dialog.get_by_role('button',name='保存',exact=True)).to_be_visible()
   expect(dialog.get_by_role('button',name='取消',exact=True)).to_be_visible()
 for device in ['phone','pad']:
  load('conversation');f=q.frame_locator('#'+device)
  f.locator('.app-header').get_by_role('button',name='账户',exact=True).click()
  for d in ['phone','pad']:expect(q.frame_locator('#'+d).locator('.app-header')).to_contain_text('我的')
 load('conversation');q.screenshot(path=str(root/'evidence/header-parity-light.png'),full_page=True)
 assert not errors,errors
 (root/'evidence/parity-verification.json').write_text(json.dumps({'passed':True,'header_scene_theme_pairs':checks,'directory_editor_checks':7,'account_navigation':'both directions','errors':errors},ensure_ascii=False,indent=2))
 print('PASS: 40 header scene/theme pairs, 7 directory/editor pairs, account navigation from both devices')
 b.close()
