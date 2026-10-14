from playwright.sync_api import sync_playwright,expect
with sync_playwright() as p:
 b=p.chromium.launch(executable_path='/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',headless=True)
 q=b.new_page(viewport={'width':1900,'height':1400});q.set_default_timeout(5000);count=0
 for theme in ['light','dark']:
  for scene in ['general','appearance','model-detail','agents','plugins-import']:
   q.goto('http://127.0.0.1:8871/docs/functional-design/prototypes/agent-workbench/review.html?page='+scene+'&theme='+theme)
   f=q.frame_locator('#pad')
   expect(f.locator('.application')).to_be_visible()
   if scene=='agents':f.get_by_role('button',name='新建',exact=True).click()
   scope=f.locator('.ant-modal-content') if scene in ['agents','plugins-import'] else f.locator('.application')
   for select in scope.locator('.ant-select').all():
    select.click();q.wait_for_timeout(250)
    popup=f.locator('.ant-select-dropdown:visible')
    expect(popup).to_have_count(1)
    assert popup.evaluate('(e)=>{const r=e.getBoundingClientRect();return r.x>=0&&r.y>=0&&r.right<=innerWidth+1&&r.bottom<=innerHeight+1}'),scene
    select.get_by_role('combobox').press('Escape')
    count+=1
 print('PASS',count,'Pad selects across settings, model, editor and import in both themes')
 b.close()
