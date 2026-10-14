"""Verify the built static React preview through a real browser; no dev server required."""
from pathlib import Path
import argparse,json,re,threading
from http.server import SimpleHTTPRequestHandler,ThreadingHTTPServer
from functools import partial
from playwright.sync_api import sync_playwright,expect
ROOT=Path(__file__).resolve().parent
parser=argparse.ArgumentParser();parser.add_argument('--url');args=parser.parse_args()
server=None
if not args.url:
 server=ThreadingHTTPServer(('127.0.0.1',0),partial(SimpleHTTPRequestHandler,directory=str(ROOT/'dist')))
 threading.Thread(target=server.serve_forever,daemon=True).start()
 args.url=f'http://127.0.0.1:{server.server_port}/review.html'
scenes=['chat','drawer','conversation','work','discover','tasks','me','settings','general','appearance','model','model-providers','model-detail','model-fetch','model-editor','skills-import','agents-import','plugins-import','agents','plugins','mcp','skills','memory','commands','hooks','usage','search','detail']
out=ROOT/'evidence';out.mkdir(exist_ok=True)
with sync_playwright() as p:
 b=p.chromium.launch(executable_path='/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',headless=True)
 page=b.new_page(viewport={'width':1280,'height':1400});page.set_default_timeout(8000);errors=[];missing=[]
 page.on('pageerror',lambda e:errors.append(str(e)));page.on('response',lambda r:missing.append(r.url) if r.status>=400 else None)
 phone=page.frame_locator('#phone');pad=page.frame_locator('#pad')
 def load(scene,theme='dark'):
  page.goto(args.url+'?page='+scene+'&theme='+theme);expect(phone.locator('.application')).to_be_visible();expect(pad.locator('.application')).to_be_visible()
 def text(f,name):return f.get_by_role('textbox',name=name,exact=True)
 def click(f,name):f.get_by_role('button',name=name,exact=True).click()
 for theme in ['light','dark']:
  for scene in scenes:
   load(scene,theme)
   for name,w,h in [('phone',393,852),('pad',768,1024)]:
    f=page.frame(name=name);assert f.evaluate('innerWidth')==w;assert f.evaluate('innerHeight')==h
    assert f.evaluate('document.body.scrollWidth<=innerWidth'),(scene,theme,name,'body overflow')
    assert f.locator('.application').evaluate('(e)=>e.scrollWidth<=e.clientWidth'),(scene,theme,name,'app overflow')
   assert phone.locator('.adm-button').count()>0
   assert pad.locator('.ant-btn').count()>0
   if scene in ['chat','agents','model-detail','drawer','general','plugins-import']:
    page.screenshot(path=str(out/(scene+'-'+theme+'.png')),full_page=True)
 print('56 scene/theme pairs passed',flush=True)
 load('agents');click(phone,'新建');text(phone,'名称').fill('同步研究助手');expect(text(pad,'名称')).to_have_value('同步研究助手')
 text(pad,'系统提示词').fill('整理资料\n保留来源');expect(text(phone,'系统提示词')).to_have_value('整理资料\n保留来源')
 page.screenshot(path=str(out/'editor-sync.png'),full_page=True)
 click(phone,'保存');expect(pad.locator('.content')).to_contain_text('同步研究助手');expect(phone.locator('.content')).to_contain_text('同步研究助手')
 phone.get_by_role('switch',name='启用 同步研究助手').click();expect(pad.get_by_role('switch',name='启用 同步研究助手')).not_to_be_checked()
 click(phone,'新建');page.get_by_role('switch',name='同步两端').click();text(phone,'名称').fill('独立草稿');expect(text(pad,'名称')).to_have_value('');page.get_by_role('switch',name='同步两端').click();expect(text(pad,'名称')).to_have_value('独立草稿')
 click(phone,'取消');click(phone,'新建');click(phone,'保存');expect(phone.get_by_text('请填写名称',exact=True)).to_be_visible();expect(pad.get_by_text('请填写名称',exact=True)).to_be_visible()
 load('model-detail');click(phone,'添加模型');text(phone,'模型 ID').fill('custom-model');click(phone,'确认');expect(pad.locator('.model-rows')).to_contain_text('custom-model');click(phone,'保存配置');expect(pad.get_by_text('连接已保存到演示会话；密钥未持久化',exact=True)).to_be_visible()
 click(pad,'获取模型');phone.get_by_role('dialog',name='获取模型',exact=True).get_by_role('button',name='获取模型',exact=True).click();expect(phone.get_by_text('example-chat',exact=True)).to_be_visible();phone.get_by_role('checkbox',name='example-chat').check();expect(pad.get_by_role('checkbox',name='example-chat')).to_be_checked();click(pad,'添加所选模型');expect(phone.locator('.model-rows')).to_contain_text('example-chat')
 load('plugins-import');text(phone,'来源链接').fill('https://example.com/plugin.zip');expect(text(pad,'来源链接')).to_have_value('https://example.com/plugin.zip');click(phone,'预览导入');text(phone,'导入名称').fill('演示插件');click(pad,'保存导入草稿');expect(phone.locator('.content')).to_contain_text('演示插件')
 load('skills-import');click(phone,'压缩文件');expect(pad.get_by_label('选择 ZIP 压缩文件')).to_be_attached();phone.get_by_label('选择 ZIP 压缩文件').set_input_files({'name':'demo.zip','mimeType':'application/zip','buffer':b'PK\x05\x06'+b'\0'*18});click(phone,'预览导入');expect(pad.get_by_text('demo.zip',exact=True)).to_be_visible()
 load('tasks');click(phone,'创建任务');text(phone,'任务名称').fill('每日简报');click(pad,'创建');expect(phone.locator('.content')).to_contain_text('每日简报')
 load('drawer');
 for f in [phone,pad]:
  for name in ['对话','工作','发现','任务','我的','设置']:expect(f.locator('.drawer').get_by_role('button',name=name,exact=True)).to_be_visible()
 load('chat');text(phone,'描述任务或提出问题').fill('你好');click(phone,'发送');expect(pad.locator('.messages')).to_contain_text('你好');expect(pad.locator('.messages')).to_contain_text('尚未接入模型服务')
 assert not errors,errors;assert not missing,missing
 result={'passed':True,'scene_theme_pairs':56,'devices':['393x852','768x1024'],'checks':['real-library-components','no-horizontal-overflow','text-and-multiline-sync','shared-save','toggle-sync','independent-rejoin','required-validation','manual-model','fetch-model-fixtures','link-import','zip-preview','task-create','drawer-parity','chat-demo'],'page_errors':errors,'missing_resources':missing}
 (out/'verification.json').write_text(json.dumps(result,ensure_ascii=False,indent=2));print(json.dumps(result,ensure_ascii=False));b.close()

if server:server.shutdown();server.server_close()
