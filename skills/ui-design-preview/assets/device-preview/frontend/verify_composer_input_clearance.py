from playwright.sync_api import sync_playwright,expect
with sync_playwright() as p:
 b=p.chromium.launch(executable_path='/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',headless=True);q=b.new_page(viewport={'width':1900,'height':1400})
 q.goto('http://127.0.0.1:8871/docs/functional-design/prototypes/agent-workbench/review.html?page=chat&theme=light')
 f=q.frame_locator('#pad');expect(f.locator('.composer')).to_be_visible()
 for text in ['', '一\n二\n三\n四\n五']:
  f.get_by_role('textbox',name='描述任务或提出问题').fill(text)
  f.get_by_role('button',name='选择聊天模型',exact=True).click();q.wait_for_timeout(400)
  r=q.frame(name='pad').evaluate('''() => {const panel=document.querySelector('.composer-popover:not(.ant-popover-hidden)').getBoundingClientRect();const input=document.querySelector('.composer textarea').getBoundingClientRect();return [panel.bottom,input.top]}''')
  assert r[0]<=r[1],r
  f.get_by_role('button',name='选择聊天模型',exact=True).click()
 print('PASS: Pad menu stays above empty and five-line input')
 b.close()
