"""Model editor keeps useful density without shrinking standard controls."""
from pathlib import Path
import json
from playwright.sync_api import sync_playwright, expect
root=Path(__file__).resolve().parent
with sync_playwright() as p:
 b=p.chromium.launch(executable_path='/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',headless=True)
 q=b.new_page(viewport={'width':1900,'height':1400})
 results=[]
 for theme in ['light','dark']:
  q.goto('http://127.0.0.1:8871/docs/functional-design/prototypes/agent-workbench/review.html?page=model-detail&theme='+theme)
  expect(q.frame_locator('#pad').locator('.model-workbench')).to_be_visible()
  f=q.frame(name='pad')
  geometry=f.evaluate('''() => {const card=document.querySelector('.model-workbench').getBoundingClientRect();const save=[...document.querySelectorAll('button')].find(x=>x.getAttribute('aria-label')==='保存配置').getBoundingClientRect();return {top:card.top,bottom:save.bottom}}''')
  assert geometry['top']<=160,geometry
  assert geometry['bottom']<=900,geometry
  for device,presets in json.loads((root/'src/device_presets.json').read_text()).items():
   for ident,label,w,h in presets:
    for width,height in ([(w,h)] if ident=='nest-hub-max' else [(w,h),(h,w)]):
     q.locator('#'+device).evaluate('(e,size)=>{e.style.width=size[0]+"px";e.style.height=size[1]+"px"}',[width,height])
     frame=q.frame(name=device)
     frame.evaluate('document.body.getBoundingClientRect()')
     q.wait_for_timeout(30)
     issues=frame.evaluate('''() => {
      const issues=[];
      for(const e of document.querySelectorAll('.content,.model-content,.model-workbench,.model-fields,.model-heading'))if(e.clientWidth&&e.scrollWidth>e.clientWidth+2)issues.push('overflow '+e.className);
      for(const e of document.querySelectorAll('.model-content .ant-input-affix-wrapper,.model-content input.ant-input:not(.ant-input-affix-wrapper input),.model-content .adm-input,.model-content .ant-select,.model-heading button'))if(e.getBoundingClientRect().height<39)issues.push('small control');
      const content=document.querySelector('.content');content.scrollTop=content.scrollHeight;
      const save=[...document.querySelectorAll('button')].find(x=>x.getAttribute('aria-label')==='保存配置');if(!save)issues.push('missing save '+document.querySelector('.content').className);else if(save.getBoundingClientRect().bottom>innerHeight+1)issues.push('save unreachable');
      return issues;
     }''')
     assert not issues,(theme,device,label,width,height,issues)
     results.append([theme,device,label,width,height])
  for device in ['phone','pad']:
   q.locator('#'+device).evaluate('(e)=>{e.style.width=(e.id==="phone"?393:768)+"px";e.style.height=(e.id==="phone"?852:1024)+"px"}')
  phone=q.frame_locator('#phone');pad=q.frame_locator('#pad')
  phone.get_by_role('textbox',name='连接名称',exact=True).fill('紧凑布局测试')
  expect(pad.get_by_role('textbox',name='连接名称',exact=True)).to_have_value('紧凑布局测试')
  phone.get_by_role('button',name='保存配置',exact=True).click()
  expect(pad.locator('.provider.selected')).to_contain_text('紧凑布局测试')
 (root/'evidence/model-density.json').write_text(json.dumps({'cases':len(results),'passed':True,'results':results},ensure_ascii=False,indent=2))
 print('PASS:',len(results),'model viewport/theme cases; synchronized edit and save')
 b.close()
