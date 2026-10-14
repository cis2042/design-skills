from playwright.sync_api import sync_playwright,expect
with sync_playwright() as p:
 b=p.chromium.launch(executable_path='/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',headless=True)
 q=b.new_page(viewport={'width':1280,'height':1400})
 q.goto('http://127.0.0.1:8871/docs/functional-design/prototypes/agent-workbench/review.html?page=model-detail')
 f=q.frame_locator('#phone');peer=q.frame_locator('#pad')
 f.get_by_role('switch',name='启用 glm-4.7',exact=True).click()
 f.get_by_role('button',name='编辑 glm-4.7',exact=True).click()
 f.get_by_role('textbox',name='模型 ID',exact=True).fill('renamed-model')
 f.get_by_role('button',name='确认',exact=True).click()
 for frame in [f,peer]:expect(frame.get_by_role('switch',name='启用 renamed-model',exact=True)).not_to_be_checked()
 print('PASS: renaming a disabled model preserves state on both devices')
 b.close()
