"""Inspect every scene and catalog viewport. Resize the actual iframe, not a screenshot."""
from pathlib import Path
from playwright.sync_api import sync_playwright,expect
import json
root=Path(__file__).resolve().parent
catalog=json.loads((root/'src/device_presets.json').read_text())
scenes=['chat','drawer','conversation','work','discover','tasks','me','settings','general','appearance','model','model-providers','model-detail','model-fetch','model-editor','skills-import','agents-import','plugins-import','agents','plugins','mcp','skills','memory','commands','hooks','usage','search','detail']
measure="""() => {
 const issues=[];
 const check=(e,kind)=>{if(e.clientWidth && e.scrollWidth>e.clientWidth+2)issues.push({kind,el:e.className,extra:e.scrollWidth-e.clientWidth})};
 check(document.body,'body-overflow');
 document.querySelectorAll('.content,.dialog-content,.model-content,.directory-tools,.app-header,.dialog-footer,.ant-modal-content').forEach(e=>check(e,'horizontal-overflow'));
 const modal=document.querySelector('.mobile-dialog section,.ant-modal-content');
 if(modal){
  const r=modal.getBoundingClientRect();
  if(r.top< -1||r.bottom>innerHeight+1)issues.push({kind:'modal-outside',top:r.top,bottom:r.bottom,height:innerHeight});
  const foot=modal.querySelector('.dialog-footer,.ant-modal-footer');
  if(foot){const r=foot.getBoundingClientRect();if(r.bottom>innerHeight+1||r.top<0)issues.push({kind:'footer-outside',top:r.top,bottom:r.bottom});}
 }
 document.querySelectorAll('.directory-tools button,.model-heading button,.app-header button,.dialog-footer button,.ant-modal-footer button').forEach(e=>{
  const r=e.getBoundingClientRect();if(r.height && (r.height<39||r.height>42))issues.push({kind:'button-height',label:e.textContent,height:r.height});
 });
 return issues;
}"""
with sync_playwright() as p:
 b=p.chromium.launch(executable_path='/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',headless=True)
 q=b.new_page(viewport={'width':1600,'height':1800});errors=[];q.on('pageerror',lambda e:errors.append(str(e)));results=[]
 for theme in ['light','dark']:
  for scene in scenes+['editor-'+k for k in ['agents','skills','plugins','mcp','memory','commands','hooks']]:
   page=scene.replace('editor-','')
   q.goto('http://127.0.0.1:8871/docs/functional-design/prototypes/agent-workbench/review.html?page='+page+'&theme='+theme)
   expect(q.frame_locator('#phone').locator('.application')).to_be_visible()
   if scene.startswith('editor-'):q.frame_locator('#phone').get_by_role('button',name='新建',exact=True).click()
   q.wait_for_timeout(350)
   for device,presets in catalog.items():
    for ident,label,w,h in presets:
     for orientation in ['portrait'] if ident=='nest-hub-max' else ['portrait','landscape']:
      width,height=(w,h) if orientation=='portrait' else (h,w)
      q.locator('#'+device).evaluate('(e,s)=>{e.style.width=s[0]+"px";e.style.height=s[1]+"px";const z=Math.min(1,e.parentElement.clientWidth/s[0]);e.style.transform="scale("+z+")";e.parentElement.style.height=s[1]*z+"px"}',[width,height])
      frame=q.frame(name=device);frame.evaluate('()=>document.body.getBoundingClientRect().width')
      q.wait_for_timeout(20)
      issues=frame.evaluate(measure)
      results.append({'theme':theme,'scene':scene,'device':label,'orientation':orientation,'size':[width,height],'issues':issues})
   print(theme,scene,flush=True)
 report={'cases':len(results),'failing':sum(bool(x['issues']) for x in results),'results':results,'errors':errors}
 (root/'evidence/matrix-audit.json').write_text(json.dumps(report,ensure_ascii=False,indent=2))
 print('RESULT',report['cases'],report['failing'],errors)
 b.close()
