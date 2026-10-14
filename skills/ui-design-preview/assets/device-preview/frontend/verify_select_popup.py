from playwright.sync_api import sync_playwright,expect
with sync_playwright() as p:
 b=p.chromium.launch(executable_path='/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',headless=True)
 q=b.new_page(viewport={'width':1500,'height':1100});q.set_default_timeout(5000)
 for theme in ['light','dark']:
  q.goto('http://127.0.0.1:8871/docs/functional-design/prototypes/agent-workbench/review.html?page=discover&theme='+theme)
  f=q.frame_locator('#pad');select=f.locator('.ant-select').filter(has=f.get_by_role('combobox',name='分类',exact=True))
  select.click();q.wait_for_timeout(400)
  popup=f.locator('.ant-select-dropdown:visible');r=popup.bounding_box();viewport=q.locator('#pad').bounding_box()
  assert r['x']>=viewport['x'] and r['y']>=viewport['y'],'Dropdown outside device'
  popup.locator('.ant-select-item-option').filter(has_text='插件').click()
  expect(select).to_contain_text('插件')
  expect(q.frame_locator('#phone').get_by_role('button',name='分类',exact=True)).to_contain_text('插件')
  expect(f.locator('.content')).not_to_contain_text('研究助理')
  expect(f.locator('.content')).to_contain_text('编程开发')
  select.click();popup.locator('.ant-select-item-option').filter(has_text='全部').click()
  expect(f.locator('.content')).to_contain_text('研究助理')
 print('PASS category popup visible, selection and sync, both themes')
 b.close()
