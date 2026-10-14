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
  phone.locator('input[type=file]').set_input_files(str(root/'evidence/visual-review/pad-composer-panel-0.png'))
  for f in [phone,pad]:expect(f.locator('.composer-context img')).to_be_visible()
  phone.get_by_role('button',name='思考强度',exact=True).click()
  phone.get_by_role('slider').focus();phone.get_by_role('slider').press('End')
  for f in [phone,pad]:expect(f.get_by_role('button',name='思考强度',exact=True)).to_contain_text('最高')
  phone.get_by_role('button',name='关闭选项',exact=True).click()
  pad.get_by_role('button',name='执行权限',exact=True).click()
  pad.get_by_role('button',name='完全访问 减少确认次数。',exact=True).click()
  for f in [phone,pad]:expect(f.locator('.permission-full')).to_be_visible()
  phone.get_by_role('button',name='听写',exact=True).click()
  expect(phone.get_by_role('dialog',name='听写')).to_contain_text('当前预览不录音')
  phone.get_by_role('button',name='关闭选项',exact=True).click()
  phone.get_by_role('textbox',name='描述任务或提出问题').fill('一\n二\n三\n四\n五')
  for device,presets in json.loads((root/'src/device_presets.json').read_text()).items():
   for ident,name,w,h in presets:
    for width,height in ([(w,h)] if ident=='nest-hub-max' else [(w,h),(h,w)]):
     q.locator('#'+device).evaluate('(e,size)=>{e.style.width=size[0]+"px";e.style.height=size[1]+"px"}',[width,height])
     q.wait_for_timeout(30)
     valid=q.frame(name=device).evaluate("() => {const e=document.querySelector('.composer');const r=e.getBoundingClientRect();return {top:r.top,bottom:r.bottom,h:innerHeight,extra:e.scrollWidth-e.clientWidth, parts:[...e.children].map(x=>[x.className,x.getBoundingClientRect().height,getComputedStyle(x).minHeight,getComputedStyle(x).maxHeight,getComputedStyle(x).flexDirection])}}")
     assert valid['top']>=0 and valid['bottom']<=valid['h']+1 and valid['extra']<=1,(theme,device,name,width,height,valid)
  for device in ['phone','pad']:
   q.locator('#'+device).evaluate('(e)=>{e.style.width=(e.id==="phone"?393:768)+"px";e.style.height=(e.id==="phone"?852:1024)+"px"}')
  phone.get_by_role('textbox',name='描述任务或提出问题').fill('参考图说明')
  phone.get_by_role('button',name='发送',exact=True).click()
  expect(pad.locator('.bubble.user')).to_contain_text('pad-composer-panel-0.png')
  for device in ['phone','pad']:q.frame_locator('#'+device).locator('.application').screenshot(path=str(root/'evidence/visual-review'/(device+'-codex-composer-'+theme+'.png')))
 print('PASS: thumbnail preview synchronized, slider keyboard selection synchronized, full-access styling, dictation unavailable state, image reference sent')
 b.close()
