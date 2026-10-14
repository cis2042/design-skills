from pathlib import Path
from playwright.sync_api import sync_playwright,expect
with sync_playwright() as p:
 b=p.chromium.launch(executable_path='/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',headless=True)
 q=b.new_page(viewport={'width':1900,'height':1400})
 for theme in ['light','dark']:
  q.goto('http://127.0.0.1:8871/docs/functional-design/prototypes/agent-workbench/review.html?page=general&theme='+theme)
  phone=q.frame_locator('#phone');pad=q.frame_locator('#pad')
  expect(phone.get_by_role('button',name='界面语言',exact=True)).to_be_visible()
  for device in ['phone','pad']:
   dims=q.frame(name=device).evaluate('''() => [...document.querySelectorAll('.general-settings .choice-trigger,.general-settings .ant-select')].map(e=>{const r=e.getBoundingClientRect();const value=e.querySelector('.choice-value,.ant-select-selection-item');return [r.width,r.height,getComputedStyle(value).fontSize]})''')
   assert len(dims)==2 and all(abs(w-180)<1 and abs(h-40)<1 and font=='14px' for w,h,font in dims),(device,dims)
  phone.get_by_role('button',name='界面语言',exact=True).click()
  phone.get_by_text('English',exact=True).click()
  expect(pad.locator('.ant-select-selection-item').first).to_have_text('English')
  phone.get_by_role('button',name='保存',exact=True).first.click()
  for frame in [phone,pad]:
   expect(frame.locator('.notice .ant-alert')).to_be_visible()
   assert frame.locator('.notice .ant-alert-icon').count()==1
  notes=[q.frame(name=device).evaluate("() => {const e=document.querySelector('.notice .ant-alert');const s=getComputedStyle(e);return [e.getBoundingClientRect().height,s.fontSize,s.backgroundColor,s.borderColor,getComputedStyle(e.querySelector('.ant-alert-icon')).color]}") for device in ['phone','pad']]
  assert notes[0]==notes[1],notes
  phone.get_by_role('button',name='关闭提示',exact=True).click()
  for frame in [phone,pad]:expect(frame.locator('.notice')).to_have_count(0)
 print('PASS: compact 180 x 40 selects, 14px values, unified notices and synchronized selection/dismissal in both themes')
 b.close()
