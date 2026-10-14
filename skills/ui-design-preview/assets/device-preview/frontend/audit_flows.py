from pathlib import Path
from playwright.sync_api import sync_playwright,expect
import json
root=Path(__file__).resolve().parent
catalog=json.loads((root/'src/device_presets.json').read_text())
results=[]
with sync_playwright() as p:
 b=p.chromium.launch(executable_path='/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',headless=True)
 q=b.new_page(viewport={'width':1600,'height':1800});q.set_default_timeout(8000)
 for device,presets in catalog.items():
  for ident,label,w,h in presets:
   for orient in ['portrait'] if ident=='nest-hub-max' else ['portrait','landscape']:
    width,height=(w,h) if orient=='portrait' else (h,w)
    for scene in ['model-detail','plugins-import','tasks','chat']:
     q.goto('http://127.0.0.1:8871/docs/functional-design/prototypes/agent-workbench/review.html?page='+scene+'&theme=dark')
     f=q.frame_locator('#'+device);peer=q.frame_locator('#'+('pad' if device=='phone' else 'phone'))
     expect(f.locator('.application')).to_be_visible()
     q.locator('#'+device).evaluate('(e,s)=>{e.style.width=s[0]+"px";e.style.height=s[1]+"px";const z=Math.min(1,e.parentElement.clientWidth/s[0]);e.style.transform="scale("+z+")";e.parentElement.style.height=s[1]*z+"px"}',[width,height])
     if scene=='model-detail':
      f.get_by_role('button',name='添加模型',exact=True).click()
      f.get_by_role('textbox',name='模型 ID',exact=True).fill('audit-model')
      f.get_by_role('button',name='确认',exact=True).click()
      expect(peer.locator('.model-rows')).to_contain_text('audit-model')
      f.get_by_role('button',name='删除 audit-model',exact=True).click()
      f.get_by_role('button',name='删除',exact=True).click()
      expect(peer.locator('.model-rows')).not_to_contain_text('audit-model')
     elif scene=='plugins-import':
      f.get_by_role('textbox',name='来源链接',exact=True).fill('https://example.com/plugin.zip')
      f.get_by_role('button',name='预览导入',exact=True).click()
      f.get_by_role('textbox',name='导入名称',exact=True).fill('导入检查')
      f.get_by_role('button',name='保存导入草稿',exact=True).click()
      expect(peer.locator('.content')).to_contain_text('导入检查')
     elif scene=='tasks':
      f.get_by_role('button',name='创建任务',exact=True).click()
      f.get_by_role('textbox',name='任务名称',exact=True).fill('任务检查')
      f.get_by_role('button',name='创建',exact=True).click()
      expect(peer.locator('.content')).to_contain_text('任务检查')
     else:
      f.get_by_role('textbox',name='描述任务或提出问题',exact=True).fill('消息检查')
      f.get_by_role('button',name='发送',exact=True).click()
      expect(peer.locator('.messages')).to_contain_text('消息检查')
     results.append([label,orient,scene])
    print(label,orient,flush=True)
 (root/'evidence/flow-matrix.json').write_text(json.dumps({'passed':True,'cases':len(results),'results':results},ensure_ascii=False,indent=2))
 print('PASS',len(results));b.close()
