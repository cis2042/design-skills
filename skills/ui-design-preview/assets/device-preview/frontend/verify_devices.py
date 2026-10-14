from pathlib import Path
from playwright.sync_api import sync_playwright,expect
import json
root=Path(__file__).resolve().parent
with sync_playwright() as p:
 b=p.chromium.launch(executable_path='/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',headless=True)
 q=b.new_page(viewport={'width':1280,'height':1500});q.set_default_timeout(5000);errors=[];q.on('pageerror',lambda e:errors.append(str(e)))
 q.goto('http://127.0.0.1:8871/docs/functional-design/prototypes/agent-workbench/review.html?page=agents')
 phone=q.frame_locator('#phone');pad=q.frame_locator('#pad')
 phone.get_by_role('button',name='新建',exact=True).click()
 phone.get_by_role('textbox',name='名称',exact=True).fill('保留设备切换草稿')
 q.wait_for_timeout(800)
 checks=[]
 for device,presets in json.loads((root/'src/device_presets.json').read_text()).items():
  for index,(ident,label,w,h) in enumerate(presets):
   q.locator('.ant-select').filter(has=q.get_by_role('combobox',name=device+' 设备',exact=True)).click()
   q.wait_for_timeout(500)
   q.locator('.ant-select-dropdown:visible').get_by_text(label+' · '+str(w)+' × '+str(h),exact=True).click()
   for landscape in ([False] if ident=='nest-hub-max' else [False,True]):
    if landscape:q.get_by_role('button',name=device+' 旋转屏幕').click()
    expected=[h,w] if landscape else [w,h]
    q.wait_for_timeout(100)
    frame=q.frame(name=device)
    assert frame.evaluate('[innerWidth,innerHeight]')==expected
    assert frame.evaluate('document.body.scrollWidth<=innerWidth')
    expect(q.frame_locator('#'+device).get_by_role('textbox',name='名称',exact=True)).to_have_value('保留设备切换草稿')
    checks.append([device,label,expected])
   if ident!='nest-hub-max':q.get_by_role('button',name=device+' 旋转屏幕').click()
 pad.get_by_role('textbox',name='名称',exact=True).fill('切换后仍然同步')
 expect(phone.get_by_role('textbox',name='名称',exact=True)).to_have_value('切换后仍然同步')
 phone.get_by_role('button',name='取消',exact=True).click()
 q.screenshot(path=str(root/'evidence/device-presets.png'),full_page=True)
 assert not errors,errors
 (root/'evidence/device-verification.json').write_text(json.dumps({'passed':True,'viewports':checks,'draft_preserved':True,'sync_preserved':True,'errors':errors},ensure_ascii=False,indent=2))
 print('PASS:',len(checks),'viewport/orientation combinations; drafts and synchronization preserved')
 b.close()
