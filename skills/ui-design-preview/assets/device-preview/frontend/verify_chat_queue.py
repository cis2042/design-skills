from pathlib import Path
import json
from playwright.sync_api import sync_playwright,expect
root=Path(__file__).resolve().parent
with sync_playwright() as p:
 b=p.chromium.launch(executable_path='/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',headless=True)
 q=b.new_page(viewport={'width':1900,'height':1400})
 for theme in ['light','dark']:
  q.goto('http://127.0.0.1:8871/docs/functional-design/prototypes/agent-workbench/review.html?page=chat&theme='+theme)
  phone=q.frame_locator('#phone');pad=q.frame_locator('#pad')
  expect(phone.locator('.composer')).to_be_visible()
  box=phone.get_by_role('textbox',name='描述任务或提出问题')
  box.fill('第一条消息');phone.get_by_role('button',name='发送',exact=True).click()
  phone.get_by_role('button',name='暂停自动发送',exact=True).click()
  box.fill('等待消息 A');phone.get_by_role('button',name='发送',exact=True).click()
  box.fill('等待消息 B');phone.get_by_role('button',name='发送',exact=True).click()
  for f in [phone,pad]:expect(f.locator('.queue-row')).to_have_count(2)
  pad.get_by_role('button',name='上移等待消息 2',exact=True).click()
  expect(phone.locator('.queue-text').first).to_have_text('等待消息 B')
  phone.get_by_role('button',name='编辑等待消息 1',exact=True).click()
  phone.get_by_role('textbox',name='编辑等待消息',exact=True).fill('本地的任何改动都还原掉')
  expect(pad.get_by_role('textbox',name='编辑等待消息',exact=True)).to_have_value('本地的任何改动都还原掉')
  phone.get_by_role('button',name='保存',exact=True).click()
  pad.get_by_role('button',name='删除等待消息 2',exact=True).click()
  for f in [phone,pad]:expect(f.locator('.queue-row')).to_have_count(1)
  phone.locator('input[type=file]').set_input_files(str(root/'evidence/visual-review/pad-composer-panel-0.png'))
  expect(phone.locator('.composer-context img')).to_have_count(1)
  box.fill('一\n二\n三\n四\n五')
  for device,presets in json.loads((root/'src/device_presets.json').read_text()).items():
   for ident,name,w,h in presets:
    for width,height in ([(w,h)] if ident=='nest-hub-max' else [(w,h),(h,w)]):
     q.locator('#'+device).evaluate('(e,size)=>{e.style.width=size[0]+"px";e.style.height=size[1]+"px"}',[width,height]);q.wait_for_timeout(30)
     r=q.frame(name=device).evaluate("() => {const e=document.querySelector('.composer');const r=e.getBoundingClientRect();return [r.top,r.bottom,innerHeight,e.scrollWidth-e.clientWidth]}")
     assert r[0]>=0 and r[1]<=r[2]+1 and r[3]<=1,(theme,device,name,width,height,r)
  box.fill('的')
  for device in ['phone','pad']:
   q.locator('#'+device).evaluate('(e)=>{e.style.width=(e.id==="phone"?393:768)+"px";e.style.height=(e.id==="phone"?852:1024)+"px"}')
   q.frame_locator('#'+device).locator('.composer').screenshot(path=str(root/'evidence/visual-review'/(device+'-chat-queue-'+theme+'.png')))
  pad.get_by_role('button',name='立即发送等待消息 1',exact=True).click()
  expect(phone.locator('.messages')).to_contain_text('本地的任何改动都还原掉')
  expect(phone.get_by_role('textbox',name='描述任务或提出问题')).to_have_value('的')
  phone.get_by_role('button',name='停止响应',exact=True).click()
  expect(pad.locator('.queue-status')).to_have_count(0)
  q.wait_for_timeout(2700)
  expect(pad.locator('.messages')).to_contain_text('已停止本次演示响应。')
 print('PASS: queue/edit/reorder/delete/immediate/stop sync, draft preserved, 58 queue layouts')
 b.close()
