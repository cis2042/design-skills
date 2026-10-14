from pathlib import Path
import json
from playwright.sync_api import sync_playwright,expect
root=Path(__file__).resolve().parent
labels=['添加附件','执行权限','选择聊天模型','思考强度','上下文用量','听写']
results=[]
with sync_playwright() as p:
 b=p.chromium.launch(executable_path='/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',headless=True)
 q=b.new_page(viewport={'width':1900,'height':1400})
 for theme in ['light','dark']:
  q.goto('http://127.0.0.1:8871/docs/functional-design/prototypes/agent-workbench/review.html?page=chat&theme='+theme)
  expect(q.frame_locator('#pad').locator('.composer')).to_be_visible()
  for device in ['phone','pad']:q.frame(name=device).add_style_tag(content='.adm-popup-body{transition:none!important}.ant-popover{animation:none!important}')
  for device,presets in json.loads((root/'src/device_presets.json').read_text()).items():
   for ident,name,w,h in presets:
    for width,height in ([(w,h)] if ident=='nest-hub-max' else [(w,h),(h,w)]):
     q.locator('#'+device).evaluate('(e,s)=>{e.style.width=s[0]+"px";e.style.height=s[1]+"px"}',[width,height])
     frame=q.frame(name=device)
     for label in labels:
      frame.evaluate('(label)=>document.querySelector(".composer button[aria-label=\\\""+label+"\\\"]").click()',label)
      frame.wait_for_function("() => {const e=document.querySelector('.composer-sheet')||[...document.querySelectorAll('.composer-popover')].find(x=>getComputedStyle(x).display!=='none'&&!x.classList.contains('ant-popover-hidden'));return e&&e.getBoundingClientRect().bottom<=innerHeight+1}",timeout=3000)
      issues=frame.evaluate('''() => {const e=document.querySelector('.composer-sheet')||[...document.querySelectorAll('.composer-popover')].find(x=>getComputedStyle(x).display!=='none'&&!x.classList.contains('ant-popover-hidden'));if(!e)return ['missing panel'];const r=e.getBoundingClientRect();return r.left< -1||r.right>innerWidth+1||r.top< -1||r.bottom>innerHeight+1?[r.x,r.y,r.width,r.height,innerWidth,innerHeight]:[]}''')
      assert not issues,(theme,device,name,width,height,label,issues)
      if device=='phone':frame.evaluate("document.querySelector('button[aria-label=\"关闭选项\"]').click()")
      else:frame.evaluate('(label)=>document.querySelector(".composer button[aria-label=\\\""+label+"\\\"]").click()',label)
      q.wait_for_timeout(30)
      results.append([theme,device,name,width,height,label])
 (root/'evidence/composer-panel-audit.json').write_text(json.dumps({'cases':len(results),'passed':True},indent=2))
 print('PASS:',len(results),'composer panel bounds checks')
 b.close()
