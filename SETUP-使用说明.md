# Fuxiu OS × Floating Life — GitHub 首页配置说明

仓库：<https://github.com/WuFuxiu/WuFuxiu> ；默认分支 `main`。

## 一次性配置（推荐网页端批量上传）

1. 解压 `fuxiu-os-readme.zip`。如果仓库里有需要保留的文件，先备份。
2. 克隆仓库并复制解压文件到仓库根目录，保留 `assets/`、`scripts/`、`.github/workflows/` 等目录层级；不要把外层 `fuxiu-os-readme/` 目录一起放进仓库。
3. 提交并推送到 `main`。或者用 GitHub 网页 `Add file` → `Upload files` 上传解压后的文件（确保路径无误）。
4. GitHub Repo → `Actions` → 首次允许工作流（若系统提示启用），依次打开这 3 个工作流，点击 `Run workflow`：`Update GitHub Statistics`、`Update Recent Activity`、`Generate Contribution Snake`。如果 `Run workflow` 按钮没出现，请确认三个 workflow 文件已经在默认分支。
5. 等工作流成功后访问 <https://github.com/WuFuxiu>，刷新页面。第一次运行 Snake 会创建 `output` 分支，这是正常现象，不需要设为默认分支。

## Actions 写入权限

工作流使用 GitHub 自动提供的 `GITHUB_TOKEN`，不需要自己创建或上传 PAT。

如果工作流报错 `403 Resource not accessible by integration` 或 `permission denied`，请检查仓库 `Settings → Actions → General → Workflow permissions` 的写入权限；如果你的组织规则锁定该设置，需要由组织管理员处理。工作流已声明 `permissions: contents: write`。

## GitHub 主页识别条件

- 同名仓库 `WuFuxiu/WuFuxiu` 必须为 `Public`。
- 仓库根目录必须有非空 `README.md`。
- 自动深浅色适配使用 HTML `<picture>`。

## 包内文件说明

- `README.md`：主页布局、介绍、技术栈、统计、趋势、近期活动、贪吃蛇、WakaTime 预留、访客徽章。
- `assets/banner-*.svg`：月夜像素横幅，深浅色两套；部分星星带有轻量 SVG 动效（实际显示取决于 GitHub 图片代理和客户端支持）。
- `assets/welcome-*.svg`：终端式个人介绍。
- `assets/footer-*.svg`：座右铭结束横幅。
- `assets/generated/`：第一次成功运行统计工作流前是“SYNCING DATA...”占位卡片，成功后替换成真实公开 GitHub 数据。
- `scripts/update_activity.py`：提取公开的近期 GitHub Events，自动写入 README 的标记范围。会排除本主页仓库的自动更新，避免刷屏。
- `.github/workflows/snake.yml`：每日生成深浅两套贡献贪吃蛇，发布到 `output` 分支。
- `.github/workflows/stats.yml`：每日生成深浅两套 GitHub 统计和语言占比 SVG，提交回 `main`。
- `.github/workflows/update-activity.yml`：每日更新最近 5 条可公开获取的活动，提交回 `main`。

## 改字方法

- 用户名/昵称/座右铭：修改 `README.md` 与 `assets/welcome-dark.svg`、`assets/welcome-light.svg`；大型视觉横幅的英文标题写在 `assets/banner-*.svg` 中。
- 编程语言：在 `README.md` 的 `Tech_Stack.exe` 章节增加实际使用的技术图标；目前只写了你确认的 C++。
- 兴趣与正在学习：编辑 `README.md` 的 `interests.txt` 文本块。
- WakaTime：当前不展示虚构时长；今后接入后再配置相应卡片。
- 更多动画：建议控制数量，避免 README 加载过重。

## 注意

- 图稿内任何示意数字都没有写入真实统计卡片。首次运行成功才会生成真实数据。
- 外部服务（打字机 SVG、访客计数、贡献趋势图、技术图标）的可用性由各服务提供方决定，断开时对应模块可能加载失败。
- 近期活动来自 GitHub 的公开活动 API，可能有时间窗口、事件类型和更新延迟限制，并非完整提交历史。
- GitHub 会缓存图片，更新后偶尔需要刷新或等待缓存失效。
