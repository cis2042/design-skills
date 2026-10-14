from playwright.sync_api import sync_playwright,expect
with sync_playwright() as p:
 b=p.chromium.launch(executable_path='/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',headless=True)
 q=b.new_page(viewport={'width':1800,'height':1500});q.set_default_timeout(5000)
 def styles(btn):
  return btn.evaluate('(e)=>{const s=getComputedStyle(e);return [s.color,s.backgroundColor,s.borderColor,s.outlineStyle,s.outlineWidth]}')
 count=0
 for theme in ['light','dark']:
  q.goto('http://127.0.0.1:8871/docs/functional-design/prototypes/agent-workbench/review.html?page=drawer&theme='+theme)
  for name in ['发现','对话','示例工作区','新产品市场调研分析','搜索','设置','新建对话']:
   values=[]
   for device in ['phone','pad']:
    btn=q.frame_locator('#'+device).locator('.drawer').get_by_role('button',name=name,exact=True)
    btn.hover();q.wait_for_timeout(200);hover=styles(btn)
    q.mouse.down();q.wait_for_timeout(200);active=styles(btn)
    q.mouse.move(1780,1480);q.mouse.up()
    q.keyboard.press('Tab');btn.focus();q.wait_for_timeout(200);focus=styles(btn)
    assert focus[3]=='solid' and focus[4]=='2px',focus
    btn.evaluate('(e)=>e.blur()')
    values.append([hover,active,focus])
   assert values[0]==values[1],(theme,name,values)
   count+=1
 print('PASS',count,'drawer button/theme cases: hover, pressed, focus match')
 b.close()
