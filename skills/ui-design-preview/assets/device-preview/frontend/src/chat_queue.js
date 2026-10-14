// Local demonstration state machine. This does not dispatch a model request.
export const demoReply='已收到。本原型展示对话流程，尚未接入模型服务。';
export function startMessage(state,item){return {...state,page:'conversation',chatRun:{id:crypto.randomUUID()},messages:[...state.messages,{role:'user',...item}]};}
export function submitMessage(state,item){const next={...state,composerPanel:null,chatContext:[],form:{...state.form,message:''}};return state.chatRun||(state.chatQueue||[]).length?{...next,chatQueue:[...(state.chatQueue||[]),{...item,id:crypto.randomUUID()}]}:startMessage(next,item);}
export function finishMessage(state,id){if(state.chatRun?.id!==id)return state;let next={...state,chatRun:null,messages:[...state.messages,{role:'assistant',text:demoReply}]};if(!state.queuePaused&&state.chatQueue?.length){const [item,...rest]=state.chatQueue;next=startMessage({...next,chatQueue:rest},item);}return next;}
export function runQueuedMessage(state,id){const item=state.chatQueue?.find(x=>x.id===id);if(!item)return state;return startMessage({...state,chatQueue:state.chatQueue.filter(x=>x.id!==id),queueEdit:null},item);}
