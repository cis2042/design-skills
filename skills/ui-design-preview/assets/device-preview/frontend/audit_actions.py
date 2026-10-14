"""Exercise every capability editor at every catalog viewport in both themes."""
from pathlib import Path
from playwright.sync_api import sync_playwright,expect
import json
root=Path(__file__).resolve().parent
catalog=json.loads((root/'src/device_presets.json').read_text())
results=[]
with sync_playwright() as p:
 b=p.chromium.launch(executable_path='/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',headless=True)
 q=b.new_page(viewport={'width':1600,'height':1800});q.set_default_timeout(8000)
 for theme in ['light','dark']:
  for kind in ['agents','skills','plugins','mcp','memory','commands','hooks']:
   q.goto('http://127.0.0.1:8871/docs/functional-design/prototypes/agent-workbench/review.html?page='+kind+'&theme='+theme)
   for device,presets in catalog.items():
    for ident,label,w,h in presets:
     for orientation in ['portrait'] if ident=='nest-hub-max' else ['portrait','landscape']:
      width,height=(w,h) if orientation=='portrait' else (h,w)
      q.locator('#'+device).evaluate('(e,s)=>{e.style.width=s[0]+"px";e.style.height=s[1]+"px";const z=Math.min(1,e.parentElement.clientWidth/s[0]);e.style.transform="scale("+z+")";e.parentElement.style.height=s[1]*z+"px"}',[width,height])
      f=q.frame_locator('#'+device);peer=q.frame_locator('#'+('pad' if device=='phone' else 'phone'))
      f.get_by_role('button',name='新建',exact=True).click()
      name='检查-'+str(len(results))
      f.get_by_role('textbox',name='名称',exact=True).fill(name)
      expect(peer.get_by_role('textbox',name='名称',exact=True)).to_have_value(name)
      f.get_by_role('button',name='保存',exact=True).click()
      switch=f.get_by_role('switch',name='启用 '+name,exact=True)
      switch.click()
      expect(peer.get_by_role('switch',name='启用 '+name,exact=True)).not_to_be_checked()
      results.append([theme,kind,label,orientation])
   print(theme,kind,len(results),flush=True)
 (root/'evidence/action-matrix.json').write_text(json.dumps({'passed':True,'cases':len(results),'checks':['open-editor','input','peer-input','save','toggle','peer-toggle'],'results':results},ensure_ascii=False,indent=2))
 print('PASS',len(results))
 b.close()
