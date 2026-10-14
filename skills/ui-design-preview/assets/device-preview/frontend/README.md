# AgentScope · Ant Design 交互预览

React 18 + Ant Design 5（Pad / 评审工具栏）+ Ant Design Mobile 5（Phone）。开发时为 React 应用，交付为静态 HTML、JS、CSS；HTTP 静态服务器即可运行，不需要 Node 运行服务、CDN 或后端。

## 构建与运行

```sh
npm ci
npm run build
python3 -m http.server 8872 --directory dist
```

打开 `http://127.0.0.1:8872/review.html`。完整产物在 `dist/`。

- `review.html`：390×884 / 768×1024 同步评审。
- `index.html?device=phone`：独立手机预览。
- `index.html?device=pad`：独立 Pad 预览。
- `index.html?device=desktop`：1280×1024 布局预览，未替代 Agent Buddy 桌面实现。
- URL 支持 `page`、`theme`、`sync`、`last`，独立模式支持 `phone` / `pad` 页面与对应主题。

## 结构

- `src/store.js`：共享状态、独立编辑及重新联动。React 直接订阅状态，无 DOM 事件转发桥。
- `src/ui.jsx`：两套组件库的语义适配层，统一中等按钮与输入控件主题。
- `src/app.jsx`：布局、导航、抽屉与设置入口。
- `src/settings.jsx`：设置、目录、编辑和导入。
- `src/models.jsx`：供应商与模型管理，手填及获取流程。
- `src/workspace.jsx`：主界面、对话、工作、发现、任务与账户。
- `src/main.jsx`：评审工具栏及固定视口。Portal 渲染到独立 iframe，样式与浮层容器跟随各设备。

## 联动与边界

页面、主题、普通输入、枚举选择、开关和本地演示保存同步。关闭联动后两端隔离，重新开启采用最近操作端。密钥仅保留在各设备组件内存，不进入共享状态、URL 或存储。文件只共享预览名称，不复制文件内容。

所有数据为演示数据，刷新会重置。聊天为本地示例回复；获取模型提供成功、空列表和失败演示；导入只保存待验证来源草稿；不下载、解压、安装、上传、请求真实模型或启动后台调度。

## 验证

使用已安装 Playwright / Chrome：

```sh
python3 verify_antd.py --url http://127.0.0.1:8872/review.html
```

`evidence/verification.json` 为实际浏览器结果，截图仅作为视觉证据。构建锁定版本见 `package-lock.json`。
