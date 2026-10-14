from playwright.sync_api import sync_playwright,expect
with sync_playwright() as p:
 b=p.chromium.launch(executable_path='/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',headless=True)
 q=b.new_page(viewport={'width':1700,'height':1400});q.set_default_timeout(5000)
 for theme in ['light','dark']:
  q.goto('http://127.0.0.1:8871/docs/functional-design/prototypes/agent-workbench/review.html?page=drawer&theme='+theme)
  rows=[]
  for device in ['phone','pad']:
   f=q.frame_locator('#'+device);expect(f.locator('.drawer')).to_be_visible()
   rows.append(f.locator('.drawer').evaluate('''d=>Array.from(d.querySelectorAll('button')).filter(b=>b.getAttribute('aria-label')!=='新建对话').map(b=>{const r=b.getBoundingClientRect();const icon=b.querySelector('.anticon');const t=document.createTreeWalker(b,NodeFilter.SHOW_TEXT);let n;while(n=t.nextNode()){if(n.textContent.trim())break;}const range=document.createRange();range.selectNodeContents(n);const tr=range.getBoundingClientRect();return {label:b.textContent.trim(),text:tr.left-r.left,icon:icon?icon.getBoundingClientRect().left-r.left:null,size:icon?parseFloat(getComputedStyle(icon).fontSize):null};})'''))
  for a,c in zip(*rows):
   assert a['label']==c['label']
   assert abs(a['text']-c['text'])<2,(theme,a,c)
   if a['icon'] is not None:
    assert abs(a['icon']-c['icon'])<2 and a['icon']<20,(theme,a,c)
    assert a['size']==c['size'],(theme,a,c)
  colors=[q.frame_locator('#'+d).locator('.drawer [aria-current=page]').evaluate('(e)=>[getComputedStyle(e).backgroundColor,getComputedStyle(e).color]') for d in ['phone','pad']]
  assert colors[0]==colors[1],colors
  q.screenshot(path='evidence/drawer-aligned-'+theme+'.png',full_page=True)
  q.frame_locator('#pad').locator('.drawer').get_by_role('button',name='发现',exact=True).click()
  expect(q.frame_locator('#phone').locator('.header-context')).to_contain_text('发现')
 print('PASS drawer left alignment, icon size, labels and navigation sync in both themes')
 b.close()
