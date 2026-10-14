import React,{useEffect,useMemo,useRef,useState,useSyncExternalStore} from 'react';
import {createRoot} from 'react-dom/client';
import {createPortal} from 'react-dom';
import {ConfigProvider,Button,Select,Switch,Space,Typography,theme} from 'antd';
import zhCN from 'antd/locale/zh_CN';
import {ConfigProvider as MobileConfig} from 'antd-mobile';
import {StyleProvider,createCache} from '@ant-design/cssinjs';
import {App} from './app';
import {Host} from './ui';
import {pages,route} from './data';
import {createStore} from './store';
import './style.css';
const store=createStore();
const font='-apple-system,BlinkMacSystemFont,"Segoe UI","PingFang SC","Microsoft YaHei",sans-serif';
const tokens={fontFamily:font,fontSize:14,controlHeight:40,borderRadius:10,colorPrimary:'#527ff5',wireframe:false};
function Frame({id,s,update,widthOverride,heightOverride,expand=false,scaleOverride}){const mobile=id==='phone';const w=widthOverride||(mobile?390:768),h=heightOverride||(mobile?884:1024);const ref=useRef();const box=useRef();const [host,setHost]=useState(null);const [measuredScale,setScale]=useState(1);const scale=scaleOverride??measuredScale;const cache=useMemo(()=>createCache(),[]);
useEffect(()=>{const ro=new ResizeObserver(entries=>setScale(expand?entries[0].contentRect.width/w:Math.min(1,entries[0].contentRect.width/w)));ro.observe(box.current);return()=>ro.disconnect()},[w,expand]);
function ready(){const doc=ref.current.contentDocument;doc.documentElement.lang='zh-CN';doc.body.style.margin='0';document.querySelectorAll('link[rel="stylesheet"],style').forEach(el=>{const copy=el.cloneNode(true);if(copy.tagName==='LINK')copy.href=el.href;doc.head.appendChild(copy)});setHost(doc.body)}
useEffect(()=>{if(host){host.ownerDocument.documentElement.setAttribute('data-prefers-color-scheme',s.theme);host.ownerDocument.documentElement.dataset.theme=s.theme}},[host,s.theme]);
return <div ref={box} className="frame-slot" style={{height:h*scale}}><iframe ref={ref} onLoad={ready} id={id} name={id} title={mobile?'Phone 交互原型':'Pad 交互原型'} srcDoc="<!doctype html><html><head></head><body></body></html>" style={{width:w,height:h,transform:`scale(${scale})`}}/>{host&&createPortal(<StyleProvider cache={cache} container={host.ownerDocument.head}><ConfigProvider locale={zhCN} theme={{algorithm:s.theme==='dark'?theme.darkAlgorithm:theme.defaultAlgorithm,token:{...tokens,colorBgContainer:s.theme==='dark'?'#1d1e21':'#ffffff',colorBgElevated:s.theme==='dark'?'#1d1e21':'#ffffff',colorBorder:s.theme==='dark'?'#34363b':'#e1e4eb',colorText:s.theme==='dark'?'#f5f5f6':'#202228'},components:{Switch:{trackMinWidth:36,trackHeight:22,handleSize:18},Button:{defaultShadow:'none',primaryShadow:'none'},Menu:{itemSelectedBg:s.theme==='dark'?'#303238':'#e9ecf1',itemSelectedColor:s.theme==='dark'?'#ffffff':'#202228'}}}} getPopupContainer={()=>host}><MobileConfig><Host.Provider value={host}><App s={s} mobile={mobile} update={update}/></Host.Provider></MobileConfig></ConfigProvider></StyleProvider>,host)}</div>}
import devicePresets from './device_presets.json';
function Review(){const canvas=useRef(null);const [canvasWidth,setCanvasWidth]=useState(innerWidth);useEffect(()=>{if(!canvas.current)return;const ro=new ResizeObserver(([entry])=>setCanvasWidth(entry.contentRect.width));ro.observe(canvas.current);return()=>ro.disconnect()},[]);const [view,setView]=useState('compare');const [zoom,setZoom]=useState('auto');const [viewports,setViewports]=useState({phone:{preset:'standard',landscape:false},pad:{preset:'standard',landscape:false}});
const viewport=id=>{const v=viewports[id],p=devicePresets[id].find(p=>p[0]===v.preset);return v.landscape&&p[0]!=='nest-hub-max'?[p[3],p[2]]:[p[2],p[3]]};
const shown=view==='compare'?['phone','pad']:[view];
const frameGap=shown.length===2?24:0;
const fitScale=Math.max(.1,(canvasWidth-48-frameGap-shown.length*2)/shown.reduce((sum,id)=>sum+viewport(id)[0],0));
const sharedScale=zoom==='actual'?1:zoom==='auto'?Math.max(.75,Math.min(1,fitScale)):Math.min(1,fitScale);
const canvasStyle={gridTemplateColumns:shown.map(id=>(viewport(id)[0]*sharedScale+2)+'px').join(' '),minWidth:shown.reduce((sum,id)=>sum+viewport(id)[0]*sharedScale+2,0)+frameGap+48,width:'100%'};
const changeViewport=(id,patch)=>setViewports(v=>({...v,[id]:{...v[id],...patch}}));
const all=useSyncExternalStore(store.subscribe,store.getSnapshot);const active=all[all.last];const options=pages.map(([value,label])=>({value,label}));const themes=[{value:'light',label:'浅色'},{value:'dark',label:'深色'}];const standalone=!location.pathname.endsWith('review.html');const requested=new URLSearchParams(location.search).get('device');const device=requested==='phone'?'phone':requested==='pad'||requested==='desktop'?'pad':innerWidth<700?'phone':'pad';const wide=requested==='desktop'||!requested&&innerWidth>=981;const index=pages.findIndex(x=>x[0]===active.page);return <ConfigProvider locale={zhCN} theme={{token:tokens}}>
<div className={standalone?'':'review-shell'}>
<div ref={canvas} className={standalone?'':'review-canvas'}>
{!standalone&&<><div className="ruler-x" aria-label="画布水平标尺" style={{width:Math.max(canvasWidth,canvasStyle.minWidth)}}>{Array.from({length:Math.ceil(Math.max(canvasWidth,canvasStyle.minWidth)/100)},(_,i)=><span key={i} style={{left:24+i*100}}>{i*100}</span>)}</div><div className="ruler-y" aria-label="画布垂直标尺" style={{height:Math.max(1200,...shown.map(id=>viewport(id)[1]*sharedScale+100))}}>{Array.from({length:Math.ceil(Math.max(1200,...shown.map(id=>viewport(id)[1]*sharedScale+100))/100)},(_,i)=><span key={i} style={{top:24+i*100}}>{i*100}</span>)}</div></>}
<div className={'devices '+(standalone?'standalone':'review-devices')} style={standalone?undefined:canvasStyle}>
{(standalone?[device]:['phone','pad']).map(id=><section className={'device-panel '+id} style={standalone?{maxWidth:wide?1280:device==='phone'?390:768}:{display:view==='compare'||view===id?undefined:'none'}} key={id}>
{!standalone&&<div className="device-heading"><strong>{id==='phone'?'Phone':'Pad'}</strong><small>{devicePresets[id].find(p=>p[0]===viewports[id].preset)[1]} · {viewport(id).join(' × ')} · {Math.round(sharedScale*100)}%</small></div>}
<Frame scaleOverride={standalone?undefined:sharedScale} expand={!standalone} widthOverride={standalone?(wide?1280:undefined):viewport(id)[0]} heightOverride={standalone?undefined:viewport(id)[1]} id={id} s={all[id]} update={fn=>store.update(id,fn)}/>
</section>)}</div></div>
{!standalone&&<aside className="review-inspector" aria-label="预览设置">
<header><img src="./assets/agentscope-logo.svg" alt=""/><div><strong>AgentScope</strong><small>响应式设计预览</small></div></header>
<section><h3>页面与联动</h3><Select aria-label="统一页面" value={active.page} options={options} onChange={p=>store.both(s=>route(s,p))}/>
<div className="inspector-pager"><Button disabled={index===0} onClick={()=>store.both(s=>route(s,pages[index-1][0]))}>上一页</Button><span>{index+1} / {pages.length}</span><Button disabled={index===pages.length-1} onClick={()=>store.both(s=>route(s,pages[index+1][0]))}>下一页</Button></div>
<div className="inspector-row"><span>同步两端操作</span><Switch aria-label="同步两端" checked={all.sync} onChange={store.sync}/></div>
<Select aria-label="统一主题" value={active.theme} options={themes} onChange={v=>store.both(s=>({...s,theme:v}))}/></section>
<section><h3>画布</h3><Select aria-label="对比方式" value={view} options={[{value:'compare',label:'左右对比'},{value:'phone',label:'仅 Phone'},{value:'pad',label:'仅 Pad'}]} onChange={setView}/>
<Select aria-label="画布缩放" value={zoom} options={[{value:'auto',label:'清晰优先 · 最低 75%'},{value:'fit',label:'适合窗口'},{value:'actual',label:'原始尺寸 · 100%'}]} onChange={setZoom}/>
<p>两端统一 {Math.round(sharedScale*100)}% · 标尺单位为画布 px</p></section>
{['phone','pad'].map(id=><section key={id}><h3>{id==='phone'?'Phone':'Pad'}</h3>
<Select aria-label={id+' 设备'} value={viewports[id].preset} options={devicePresets[id].map(([value,label,w,h])=>({value,label:label+' · '+w+' × '+h}))} onChange={preset=>changeViewport(id,{preset})}/>
<div className="inspector-row"><span>{viewport(id).join(' × ')} CSS px</span><Button disabled={viewports[id].preset==='nest-hub-max'} aria-label={id+' 旋转屏幕'} onClick={()=>changeViewport(id,{landscape:!viewports[id].landscape})}>{viewports[id].preset==='nest-hub-max'?'固定横屏':viewports[id].landscape?'横屏 ↻':'竖屏 ↻'}</Button></div>
<Select aria-label={(id==='phone'?'Phone':'Pad')+' 页面'} value={all[id].page} options={options} onChange={p=>store.update(id,s=>route(s,p))}/>
<Select aria-label={(id==='phone'?'Phone':'Pad')+' 主题'} value={all[id].theme} options={themes} onChange={v=>store.update(id,s=>({...s,theme:v}))}/>
</section>)}
<footer>交互原型 · 示例数据<br/>业务服务尚未接入</footer>
</aside>}
</div></ConfigProvider>}

createRoot(document.getElementById('root')).render(<Review/>);

import "./polish.css";
import "./codex_reference.css";
