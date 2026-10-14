from pathlib import Path
from playwright.sync_api import sync_playwright, expect

root = Path(__file__).resolve().parent
with sync_playwright() as p:
    browser = p.chromium.launch(executable_path='/Applications/Google Chrome.app/Contents/MacOS/Google Chrome', headless=True)
    page = browser.new_page(viewport={'width':1900,'height':1400})
    for theme in ['light','dark']:
        page.goto('http://127.0.0.1:8871/docs/functional-design/prototypes/agent-workbench/review.html?page=settings&theme='+theme)
        phone, pad = page.frame_locator('#phone'), page.frame_locator('#pad')
        expect(pad.locator('.general-settings')).to_be_visible()
        expect(pad.locator('.setting-group')).to_have_count(0)
        expect(pad.locator('.app-header strong')).to_have_text('常规设置')
        expect(pad.locator('.ant-menu-item-selected')).to_have_text('常规')
        expect(phone.locator('.setting-group')).to_have_count(3)
        for width, height in [(768,1024),(1024,768)]:
            page.locator('#pad').evaluate('(e,s)=>{e.style.width=s[0]+"px";e.style.height=s[1]+"px"}',[width,height])
            expect(pad.locator('.general-settings')).to_be_visible()
            assert pad.locator('.content').evaluate('(e)=>e.scrollWidth<=e.clientWidth+1')
        pad.locator('.application').screenshot(path=str(root/'evidence/visual-review'/('pad-settings-landing-'+theme+'.png')))
        pad.get_by_role('menuitem',name='外观',exact=True).click()
        expect(pad.locator('.app-header strong')).to_have_text('外观设置')
        pad.locator('.app-header').get_by_role('button',name='返回工作区',exact=True).click()
        expect(pad.locator('.composer')).to_be_visible()
        pad.get_by_role('button',name='设置',exact=True).click()
        expect(pad.locator('.general-settings')).to_be_visible()
        expect(phone.locator('.setting-group')).to_have_count(3)
        phone.get_by_text('常规',exact=True).click()
        expect(pad.locator('.general-settings')).to_be_visible()
        phone.locator('.app-header').get_by_role('button',name='返回设置',exact=True).click()
        expect(phone.locator('.setting-group')).to_have_count(3)
        expect(pad.locator('.general-settings')).to_be_visible()
    browser.close()
print('PASS: Pad defaults to general settings, no duplicate directory, Phone directory, sidebar/back navigation and both orientations/themes')
