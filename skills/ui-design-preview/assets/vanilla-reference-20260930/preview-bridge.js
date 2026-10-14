"use strict";
// 同源评审器：同步视图与普通表单草稿，不广播文件、凭据或提交动作。
let previewApplyingSelection = false;
function previewSelectKey(element) {
  if (element.id) return 'id:' + element.id;
  if (element.dataset.pref) return 'pref:' + element.dataset.pref;
  if (element.name) return 'name:' + element.name;
  if (element.dataset.prefDraft) return 'draft:' + element.dataset.prefDraft;
  if (element.getAttribute('aria-label')) return 'label:' + element.getAttribute('aria-label');
  return null;
}
function readPreviewSelections() {
  return [...document.querySelectorAll('select')]
    .filter(element => previewSelectKey(element) && element.checkVisibility())
    .map(element => ({key: previewSelectKey(element), value: element.value}));
}
function applyPreviewSelections(selections) {
  if (!Array.isArray(selections)) return;
  previewApplyingSelection = true;
  try {
    for (const selection of selections) {
      const element = [...document.querySelectorAll('select')].find(node => previewSelectKey(node) === selection.key);
      if (!element || ![...element.options].some(option => option.value === selection.value) || element.value === selection.value) continue;
      element.value = selection.value;
      // 沿用本地控件的枚举状态处理，不触发保存/导入；桥自身禁止回传。
      element.dispatchEvent(new Event('change', {bubbles: true}));
    }
  } finally { previewApplyingSelection = false; }
}
function previewTextFields() {
  return [...document.querySelectorAll('input, textarea')].filter(element =>
    (element instanceof HTMLTextAreaElement || ['text','search','url','email','tel','number'].includes(element.type)) &&
    !/key|token|secret|password|密钥|密码/i.test([element.id,element.name,element.getAttribute('aria-label')].join(' ')) &&
    previewSelectKey(element) && element.checkVisibility());
}
function applyPreviewTexts(texts) {
  if (!Array.isArray(texts)) return;
  previewApplyingSelection = true;
  try {
    for (const text of texts) {
      const element = previewTextFields().find(node => previewSelectKey(node) === text.key);
      if (!element || typeof text.value !== 'string' || element.value === text.value) continue;
      element.value = text.value;
      element.dispatchEvent(new Event('input', {bubbles:true}));
    }
  } finally { previewApplyingSelection = false; }
}
window.readPreviewView = function () {
  let page = state.page;
  if (state.drawer) page = 'drawer';
  else if (page === 'chat' && state.conversation) page = 'conversation';
  else if (page === 'settings') {
    if (importDraft) page = importDraft.kind + '-import';
    else if (!settingsDetail) page = 'settings';
    else if (state.settingsTab !== 'model') page = state.settingsTab;
    else if (providerPicker) page = 'model-providers';
    else if (modelDialog === 'fetch') page = 'model-fetch';
    else if (modelScreen === 'edit') page = modelConnections.some(c => c.id === modelDraft?.id) ? 'model-detail' : 'model-editor';
    else page = 'model';
  }
  // 未保存决定留在操作端；不能替另一端作出保存/放弃决定。
  if (modelDialog === 'leave') return null;
  return {
    page, theme: state.theme, selections: readPreviewSelections(),
    texts: previewTextFields().map(element => ({key:previewSelectKey(element),value:element.value})),
    importMode: importDraft?.mode === 'archive' ? 'archive' : 'link',
    connection: modelConnections.some(c => c.id === modelDraft?.id) ? modelDraft.id : null,
    provider: modelDraft?.provider || null,
    modelOverlay: modelDialog === 'manual' ? 'manual' : null,
    modelIndex: modelDialog === 'manual' ? modelEditIndex : -1,
    category: state.category, scope: state.scope, taskTab: state.taskTab,
    item: state.selectedItem,
    modal: ['schedule','permission','login-expired','add'].includes(state.modal) ? state.modal : null,
    productModal: ['model','document'].includes(productModal) ? productModal : null,
    configEditor: editorKind ? editorKind.kind : null
  };
};
window.applyPreviewView = function (view) {
  const current = window.readPreviewView();
  if (view.selectionOnly && current?.page === view.page && current.modelOverlay === view.modelOverlay && current.configEditor === view.configEditor && current.modal === view.modal && current.connection === view.connection && current.provider === view.provider && current.productModal === view.productModal && current.importMode === view.importMode && current.theme === view.theme) {
    applyPreviewSelections(view.selections);
    applyPreviewTexts(view.texts);
    return;
  }
  if (Object.values(catalog).flat().some(item => item.id === view.item)) state.selectedItem = view.item;
  // 同一导入弹窗换方式时保留接收端自己的输入；不会复制另一端的链接/文件。
  if (importDraft && current?.page === view.page) {
    captureImport();
    importDraft.mode = view.importMode === 'archive' ? 'archive' : 'link';
    importDraft.step = 'source';
    importDraft.error = '';
  } else {
    window.previewRoute(view.page);
    if (importDraft) importDraft.mode = view.importMode === 'archive' ? 'archive' : 'link';
  }
  if (['model-detail','model-fetch','model-editor'].includes(view.page)) {
    const connection = modelConnections.find(c => c.id === view.connection);
    if (connection) { modelDraft = structuredClone(connection); modelScreen = 'edit'; }
    else if (view.page === 'model-editor' && modelProviders.some(p => p.id === view.provider)) modelPick(view.provider);
    if (view.modelOverlay === 'manual') {
      modelDialog = 'manual';
      modelEditIndex = Number.isInteger(view.modelIndex) && view.modelIndex >= 0 && view.modelIndex < modelDraft.models.length ? view.modelIndex : -1;
    }
  }
  if (Object.hasOwn(categoryNames, view.category)) state.category = view.category;
  if (['discover','installed'].includes(view.scope)) state.scope = view.scope;
  if (['running','schedule','done'].includes(view.taskTab)) state.taskTab = view.taskTab;
  if (settingsItems().some(item => item[0] === view.configEditor)) editorKind = {kind: view.configEditor};
  state.modal = ['schedule','permission','login-expired'].includes(view.modal) || (view.modal === 'add' && findItem()) ? view.modal : null;
  productModal = ['model','document'].includes(view.productModal) ? view.productModal : null;
  state.theme = view.theme === 'dark' ? 'dark' : 'light';
  render();
  applyPreviewSelections(view.selections);
    applyPreviewTexts(view.texts);
};
const previewNavigationActions = new Set([
  'open-item','open-search-item','pad-open','add-item','create-task','close-modal','permission','login-expired','model','view-knowledge','product-close',
  'drawer','new-chat','open-history','search','z-category','z-back','z-import','z-new','z-edit','z-editor-close',
  'imp-mode','imp-close','imp-back','mc-edit','mc-exit','mc-list','mc-add','mc-picker-close','mc-pick',
  'mc-fetch','mc-model-add','mc-model-edit','mc-dialog-close'
]);
// 在应用事件处理器之后注册，读取最终视图。程序化回放不产生点击事件。
document.addEventListener('click', event => {
  const action = event.target.closest('[data-action]')?.dataset.action;
  if (!action || !(previewNavigationActions.has(action) || /^(go-|theme-|category-|scope-|task-)/.test(action))) return;
  queueMicrotask(() => window.onPreviewChange?.(window.readPreviewView()));
});
document.addEventListener('keydown', event => {
  if (event.key === 'Escape') queueMicrotask(() => window.onPreviewChange?.(window.readPreviewView()));
});

// 原生 select 的选中值可同步；不尝试打开另一端的系统弹出菜单。
document.addEventListener('change', event => {
  if (previewApplyingSelection || !(event.target instanceof HTMLSelectElement) || !previewSelectKey(event.target)) return;
  queueMicrotask(() => {
    const view = window.readPreviewView();
    if (view) window.onPreviewChange?.({...view, selectionOnly: true});
  });
});

function notifyPreviewText(event) {
  if (previewApplyingSelection || event.isComposing || !previewTextFields().includes(event.target)) return;
  queueMicrotask(() => {
    const view = window.readPreviewView();
    if (view) window.onPreviewChange?.({...view, selectionOnly:true});
  });
}
document.addEventListener('input', notifyPreviewText);
document.addEventListener('compositionend', notifyPreviewText);
