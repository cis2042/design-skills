from pathlib import Path
import json
from playwright.sync_api import sync_playwright,expect
root=Path(__file__).resolve().parent
with sync_playwright() as p:
 b=p.chromium.launch(executable_path='/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',headless=True)
 q=b.new_page(viewport={'width':1900,'height':1400});errors=[];q.on('pageerror',lambda e:errors.append(str(e)))
 for theme in ['light','dark']:
  q.goto('http://127.0.0.1:8871/docs/functional-design/prototypes/agent-workbench/review.html?page=chat&theme='+theme)
  phone=q.frame_locator('#phone');pad=q.frame_locator('#pad')
  expect(phone.get_by_role('textbox',name='描述任务或提出问题')).to_be_visible()
  phone.get_by_role('button',name='执行权限',exact=True).click()
  phone.get_by_role('button',name='计划模式 编辑前先给出计划。',exact=True).click()
  for f in [phone,pad]:expect(f.get_by_role('button',name='执行权限',exact=True)).to_contain_text('计划模式')
  pad.get_by_role('button',name='选择聊天模型',exact=True).click()
  pad.get_by_role('button',name='glm-5.3',exact=True).click()
  expect(phone.get_by_role('button',name='选择聊天模型',exact=True)).to_contain_text('glm-5.3')
  phone.get_by_role('button',name='思考强度',exact=True).click()
  phone.get_by_role('button',name='最高',exact=True).click()
  expect(pad.get_by_role('button',name='思考强度',exact=True)).to_contain_text('最高')
  phone.get_by_role('button',name='添加附件',exact=True).click()
  phone.get_by_role('button',name='示例工作流 资料整理 → 证据核对 → 报告草稿',exact=True).click()
  for f in [phone,pad]:expect(f.locator('.composer-context')).to_contain_text('示例工作流')
  phone.locator('input[type=file]').set_input_files({'name':'notes.txt','mimeType':'text/plain','buffer':b'demo'})
  expect(pad.locator('.composer-context')).to_contain_text('notes.txt')
  pad.get_by_role('button',name='移除 notes.txt',exact=True).click()
  expect(phone.locator('.composer-context')).not_to_contain_text('notes.txt')
  phone.get_by_role('textbox',name='描述任务或提出问题').fill('整理资料\n保留分行')
  expect(pad.get_by_role('textbox',name='描述任务或提出问题')).to_have_value('整理资料\n保留分行')
  phone.get_by_role('button',name='上下文用量',exact=True).click()
  expect(phone.get_by_role('dialog',name='上下文用量')).to_contain_text('本地估算')
  phone.get_by_role('button',name='关闭选项',exact=True).click()
  phone.get_by_role('button',name='发送',exact=True).click()
  expect(pad.locator('.bubble.user')).to_contain_text('整理资料')
  expect(phone.get_by_role('textbox',name='描述任务或提出问题')).to_have_value('')
  for device,sets in json.loads((root/'src/device_presets.json').read_text()).items():
   for ident,label,w,h in sets:
    for width,height in ([(w,h)] if ident=='nest-hub-max' else [(w,h),(h,w)]):
     q.locator('#'+device).evaluate('(e,s)=>{e.style.width=s[0]+"px";e.style.height=s[1]+"px"}',[width,height])
     q.frame(name=device).evaluate('document.body.getBoundingClientRect()');q.wait_for_timeout(30)
     issue=q.frame(name=device).evaluate('''() => {const e=document.querySelector('.composer');const r=e.getBoundingClientRect();return {overflow:e.scrollWidth-e.clientWidth,outside:r.bottom>innerHeight+1||r.top<0}}''')
     assert issue['overflow']<=2 and not issue['outside'],(device,label,width,height,issue)
  for device in ['phone','pad']:
   q.locator('#'+device).evaluate('(e)=>{e.style.width=(e.id==="phone"?393:768)+"px";e.style.height=(e.id==="phone"?852:1024)+"px"}')
   q.frame_locator('#'+device).locator('.application').screenshot(path=str(root/'evidence/visual-review'/(device+'-composer-'+theme+'.png')))
 assert not errors,errors
 print('PASS: permissions, provider models, effort, workflow, attachment add/remove, multiline sync, usage, send; 58 viewport/theme combinations')
 b.close()
