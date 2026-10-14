from playwright.sync_api import sync_playwright,expect
with sync_playwright() as p:
 b=p.chromium.launch(executable_path='/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',headless=True)
 q=b.new_page(viewport={'width':1280,'height':1400})
 for theme in ['dark','light']:
  q.goto('http://127.0.0.1:8871/docs/functional-design/prototypes/agent-workbench/review.html?page=agents&theme='+theme)
  phone=q.frame_locator('#phone');pad=q.frame_locator('#pad')
  phone.get_by_role('button',name='新建',exact=True).click()
  q.wait_for_timeout(500)
  for f in [phone,pad]:
   btn=f.get_by_role('button',name='保存',exact=True)
   actual=btn.evaluate('(e)=>getComputedStyle(e).backgroundColor')
   expected='rgb(245, 245, 246)' if theme=='dark' else 'rgb(32, 34, 40)'
   assert actual==expected,(theme,actual,expected)
 print('PASS: primary dialog actions match in both themes and devices')
 b.close()
