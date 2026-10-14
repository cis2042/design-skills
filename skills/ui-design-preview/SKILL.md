---
name: ui-design-preview
description: Build runnable local UI previews with synchronized page/theme switching and fixed device viewports. Use for interactive prototype previews, Phone/Pad comparisons, independent side-by-side review, and portable preview delivery.
license: Apache-2.0
---

# UI Design Preview

独立的交互预览与多设备对照技能。页面制作、视觉批准和真实业务验收分别记录。不要把桌面截图缩小后冒充移动布局。

## When to use

用于已有 UI 的交互预览、Phone / Pad / Desktop 布局比较、深浅主题对照、操作同步和可携带静态交付。

## How to use · Workflow

1. 读取已有页面、批准规格、视口和输出位置，保护未提交修改。先备份当前实现，不重复创建产品需求。
2. 整体复制 [完整案例](assets/device-preview/review.html) 所在目录。当前实现使用 React、Ant Design 和 Ant Design Mobile；源码与构建产物都在包内。
3. 在 `frontend/src/data.js` 注册场景，在 `store.js` 管理共享状态；设备采用独立固定逻辑视口，外层只调整展示缩放。布局可不同，功能入口必须一致。
4. 执行 `python3 serve.py --port 8872`，打开输出地址。当前静态产物可直接运行，不依赖 Node 服务器或 CDN。修改源码时在 frontend 执行 npm ci 和 npm run build。
5. 实际操作两端：导航、弹窗、文本、枚举、开关、演示保存；关闭联动独立编辑，重新开启采用最近操作端。敏感凭据和文件内容不共享，不回放真实业务写操作。
6. 在已安装 Playwright / Chrome 的环境运行 `python3 frontend/verify_antd.py --url <当前评审地址>`。核验构建产物，而非只检查开发服务器。新项目更新断言后再验收，不沿用案例通过结果。
7. 验证通过后运行 frontend/publish.mjs 发布静态入口；更新 SHA256SUMS。交付入口、源码、构建产物、场景清单、截图及实际验证边界。

## 操作合同

- 顶部控制统一页面和主题；单端控制在联动开启时传播到另一端。
- 两端共用普通草稿、枚举选择、开关、弹窗及本地演示数据状态。
- 独立模式两端隔离；重新联动以最近操作端为准。
- URL 只记录导航、主题和联动状态，不记录表单、密钥或业务数据。
- 密钥仅保留在各端组件内存；文件仅共享预览名称；真实提交、安装、上传、模型调用不得由评审同步触发。
- 动态应用构建后交付静态 HTML/JS/CSS，浏览器仍能执行交互。静态交付不等于截图或无交互页面。

## Validation checklist

- [ ] 项目外复制目录可独立运行，资源无 404、无外部 CDN 依赖。
- [ ] Phone 390×884、Pad 768×1024 布局分别成立；Desktop 1280×1024 按需求验证。
- [ ] 标准组件和统一主题 token，字号、间距、焦点和滚动不裁切。
- [ ] 两端入口对齐，输入、清空、选择、开关、演示保存与独立/重新联动有效。
- [ ] 深浅主题所有注册场景无脚本异常和横向溢出。
- [ ] 真实后端未接入部分有明确说明，不把模拟成功当作生产验证。

## Troubleshooting

先核对构建、相对资源路径、组件容器和状态来源。端口占用换空闲端口，不杀未知服务。浏览器工具或构建依赖缺失时记录 NOT_VERIFIED，不静默安装全局工具。弹窗必须位于对应设备容器中，不能渲染到评审器外层。新场景以共享状态接入，不恢复 DOM 点击转发。

## Output contract

提供 preview_url、source_directory、静态产物目录、场景/设备/主题清单、备份和 SHA256、实际截图、验证结果及未接入能力。源码存在与构建成功不能替代浏览器验收。

## References

- [运行方法](references/preview-method.md)
- [完整案例说明](assets/device-preview/README.md)
- [React 源码说明](assets/device-preview/frontend/README.md)
- [来源记录](assets/device-preview/SOURCE.md)
- [浏览器验证](assets/device-preview/frontend/verify_antd.py)

## Examples

复制完整目录，运行 serve.py。在子智能体页从 Phone 新建，输入名称，确认 Pad 同步；从 Pad 保存，两端目录显示新增项。关闭联动后独立输入，再开启验证最近端覆盖。模型页测试手填及成功/空/失败获取流程，保留示例数据说明。

## Keywords

React, Ant Design, Ant Design Mobile, UI preview, synchronized preview, static build, 多设备对照, 操作同步, 静态交付
