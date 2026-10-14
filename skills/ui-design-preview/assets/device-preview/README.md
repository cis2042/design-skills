# React + Ant Design 静态交互预览

执行 `python3 serve.py --port 8872`，打开输出的地址。完整静态文件已提供，无需构建或安装依赖即可预览。

源码和锁文件位于 `frontend/`。修改后在该目录执行 `npm ci`、`npm run build`、`python3 verify_antd.py`，验证后 `node publish.mjs` 更新上一级静态入口。

Phone 使用 Ant Design Mobile，Pad 与评审工具栏使用 Ant Design。28 个场景、深浅主题、输入/选择/开关/演示保存同步及独立编辑共用状态。密钥不共享，业务后台未接入；刷新重置演示数据。

源码结构与操作边界见 [frontend/README.md](frontend/README.md)。旧版独立原生 HTML 案例保留在相邻 `vanilla-reference-20260930/`，不与当前 React 入口混用。
