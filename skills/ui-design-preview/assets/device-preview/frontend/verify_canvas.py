from playwright.sync_api import sync_playwright,expect
from pathlib import Path
import json
root=Path(__file__).resolve().parent
with sync_playwright() as p:
 b=p.chromium.launch(executable_path='/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',headless=True)
 q=b.new_page(viewport={'width':1920,'height':1080});q.set_default_timeout(6000)
 q.goto('http://127.0.0.1:8871/docs/functional-design/prototypes/agent-workbench/review.html?page=chat&theme=light')
 expect(q.frame_locator('#phone').locator('.application')).to_be_visible()
 def choose(label,text):
  q.locator('.ant-select').filter(has=q.get_by_role('combobox',name=label,exact=True)).click()
  q.locator('.ant-select-dropdown:visible').get_by_text(text,exact=True).click()
 def scale(d):return q.locator('#'+d).evaluate('(e)=>e.getBoundingClientRect().width/e.clientWidth')
 q.wait_for_timeout(300)
 assert abs(scale('phone')-scale('pad'))<.0001
 canvas=q.locator('.review-canvas').bounding_box()
 inspector=q.locator('.review-inspector').bounding_box()
 assert abs(canvas['width']+inspector['width']-1920)<2
 assert abs(inspector['x']-canvas['width'])<2
 assert inspector['height']==1080
 expect(q.locator('.ruler-x')).to_be_visible()
 expect(q.locator('.ruler-y')).to_be_visible()
 assert q.evaluate('document.documentElement.scrollWidth<=innerWidth')
 q.screenshot(path=str(root/'evidence/browser-workbench.png'),full_page=True)
 assert q.locator('.device-panel.phone').bounding_box()['width']>390
 choose('phone 设备','iPhone SE · 375 × 667');q.get_by_role('button',name='phone 旋转屏幕').click()
 choose('pad 设备','Surface Pro 10 · 960 × 1440');q.get_by_role('button',name='pad 旋转屏幕').click()
 q.set_viewport_size({'width':970,'height':900});q.wait_for_timeout(300)
 assert abs(scale('phone')-scale('pad'))<.0001
 assert scale('phone')>=.745 and scale('pad')>=.745
 assert q.locator('.review-canvas').evaluate('(e)=>e.scrollWidth>e.clientWidth')
 q.screenshot(path=str(root/'evidence/canvas-clear.png'),full_page=True)
 choose('对比方式','仅 Pad');q.wait_for_timeout(200)
 assert q.locator('.device-panel.phone').is_hidden()
 choose('画布缩放','适合窗口');q.wait_for_timeout(200)
 assert q.locator('.review-canvas').evaluate('(e)=>e.scrollWidth<=e.clientWidth+2')
 assert q.frame(name='pad').evaluate('[innerWidth,innerHeight]')==[1440,960]
 choose('对比方式','左右对比');choose('画布缩放','原始尺寸 · 100%');q.wait_for_timeout(200)
 assert abs(scale('phone')-1)<.0001 and abs(scale('pad')-1)<.0001
 q.frame_locator('#phone').get_by_role('textbox',name='描述任务或提出问题',exact=True).fill('画布切换保留输入')
 choose('对比方式','仅 Pad')
 expect(q.frame_locator('#pad').get_by_role('textbox',name='描述任务或提出问题',exact=True)).to_have_value('画布切换保留输入')
 choose('对比方式','左右对比')
 expect(q.frame_locator('#phone').get_by_role('textbox',name='描述任务或提出问题',exact=True)).to_have_value('画布切换保留输入')
 print('PASS: equal scale on both devices; full width, landscape readability, canvas scrolling, single device, 100%, state preservation')
 b.close()
