import React from 'react';
import ReactDOM from 'react-dom';
// 兼容 rc-util 5.44.4 的接口；DOM 类型取自节点所属窗口，支持预览 iframe。
export function isDOM(node) {
  const win = node?.ownerDocument?.defaultView;
  return Boolean(win && (node instanceof win.HTMLElement || node instanceof win.SVGElement));
}
export function getDOM(node) {
  if (isDOM(node?.nativeElement)) return node.nativeElement;
  return isDOM(node) ? node : null;
}
export default function findDOMNode(node) {
  return getDOM(node) || (node instanceof React.Component ? ReactDOM.findDOMNode?.(node) : null);
}
