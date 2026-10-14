// rc-util 5 的全局 Element 判断不支持 iframe portal；按元素所属文档判断。
// 保留库原有的 HTML、SVG 与固定定位元素可见性语义。
export default function isVisible(element) {
  const ElementType = element?.ownerDocument?.defaultView?.Element;
  if (!ElementType || !(element instanceof ElementType)) return false;
  if (element.offsetParent) return true;
  if (element.getBBox) {
    const {width, height} = element.getBBox();
    if (width || height) return true;
  }
  const {width, height} = element.getBoundingClientRect();
  return Boolean(width || height);
}
