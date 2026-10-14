from playwright.sync_api import sync_playwright,expect
with sync_playwright() as p:
 b=p.chromium.launch(executable_path='/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',headless=True)
 q=b.new_page(viewport={'width':1500,'height':1200})
 for theme in ['light','dark']:
  q.goto('http://127.0.0.1:8871/docs/functional-design/prototypes/agent-workbench/review.html?page=drawer&theme='+theme)
  for d in ['phone','pad']:
   button=q.frame_locator('#'+d).locator('.drawer .new-chat-button');expect(button).to_be_visible()
   r=button.evaluate('''b=>{const rect=e=>{const r=e.getBoundingClientRect();return {x:r.x+r.width/2,y:r.y+r.height/2,width:r.width,height:r.height}};return {button:rect(b),group:rect(b.querySelector('.new-chat-content')),icon:rect(b.querySelector('.anticon')),text:rect(b.querySelector('.new-chat-content>span:last-child'))}}''')
   assert abs(r['button']['y']-r['group']['y'])<1,r
   assert abs(r['button']['x']-r['group']['x'])<1,r
   assert abs(r['icon']['y']-r['text']['y'])<1,r
   assert r['icon']['width']==14 and r['icon']['height']==14,r
  q.screenshot(path='evidence/new-chat-aligned-'+theme+'.png',full_page=True)
  q.frame_locator('#pad').locator('.drawer .new-chat-button').click()
  expect(q.frame_locator('#phone').locator('.drawer')).not_to_be_visible()
 print('PASS new-chat icon/text centered, 14px icon, both themes and devices; navigation sync')
 b.close()
