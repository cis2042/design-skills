from pathlib import Path
import json
from playwright.sync_api import sync_playwright,expect
root=Path(__file__).resolve().parent
with sync_playwright() as p:
 b=p.chromium.launch(executable_path='/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',headless=True)
 q=b.new_page(viewport={'width':1900,'height':1600});q.set_default_timeout(5000)
 results=[]
 for theme in ['light','dark']:
  q.goto('http://127.0.0.1:8871/docs/functional-design/prototypes/agent-workbench/review.html?page=discover&theme='+theme)
  for device, presets in json.loads((root/'src/device_presets.json').read_text()).items():
   for ident,label,w,h in presets:
    for orientation in ['portrait'] if ident=='nest-hub-max' else ['portrait','landscape']:
     width,height=(w,h) if orientation=='portrait' else (h,w)
     q.locator('#'+device).evaluate('(e,s)=>{e.style.width=s[0]+"px";e.style.height=s[1]+"px";let z=Math.min(1,e.parentElement.clientWidth/s[0]);e.style.transform="scale("+z+")";e.parentElement.style.height=s[1]*z+"px"}',[width,height])
     f=q.frame_locator('#'+device)
     if device=='pad':
      trigger=f.locator('.ant-select').filter(has=f.get_by_role('combobox',name='分类',exact=True));trigger.click()
      popup=f.locator('.ant-select-dropdown:visible');q.wait_for_timeout(300)
      assert popup.evaluate('(e)=>{let r=e.getBoundingClientRect();return r.left>=0 && r.right<=innerWidth+1 && r.top>=0 && r.bottom<=innerHeight+1}')
      popup.locator('.ant-select-item-option').filter(has_text='插件').click()
     else:
      f.get_by_role('button',name='分类',exact=True).click();q.wait_for_timeout(300)
      f.locator('.choice-sheet .adm-selector-item').filter(has_text='插件').click()
     for d in ['phone','pad']:
      expect(q.frame_locator('#'+d).locator('.content')).to_contain_text('编程开发')
      expect(q.frame_locator('#'+d).locator('.content')).not_to_contain_text('研究助理')
     # Reopen and restore to verify repeated use, not only the initial click.
     if device=='pad':
      trigger.click();popup.locator('.ant-select-item-option').filter(has_text='全部').click()
     else:
      f.get_by_role('button',name='分类',exact=True).click();f.locator('.choice-sheet .adm-selector-item').filter(has_text='全部').click()
     results.append([theme,device,label,orientation])
  print(theme,'passed',flush=True)
 (root/'evidence/select-matrix.json').write_text(json.dumps({'passed':len(results),'cases':results},ensure_ascii=False,indent=2))
 print('PASS',len(results),'category popup / filter / sync / reopen cases')
 b.close()
