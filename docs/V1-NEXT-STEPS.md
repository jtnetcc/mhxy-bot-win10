# V1 Next Steps

## 目标
把当前“自动打图预演版”推进到“真实接入前最后一层骨架”。

## 已完成
- 项目目录
- Web 原型界面
- 自动打图任务底座
- mock 窗口绑定 / mock UI识别 / mock 巡线 / mock 日志链路
- GitHub 远程仓库与 Windows 打包 workflow

## 下一步（无需游戏环境）
1. 补齐配置结构 ✅
2. 补齐路线模板格式 ✅
3. 补齐模板资源清单格式 ✅
4. 补齐 OCR 服务接口 ✅（当前为 mock + 目标地图解析）
5. 补齐打图状态机 ✅
6. 给 launcher 接任务注册器 ✅
7. 规范日志与 screenshots 输出目录 ✅（配置项已预留）

## 本轮新增落地
- `dig_treasure` 已从纯 mock 日志升级为**状态机驱动的预演流程**
- 路线改为从 `config/routes/dig/default.yaml` 装载，不再写死在代码里
- 模板清单改为从 `config/templates/dig-ui.example.yaml` 装载
- OCR 服务增加了 `extract_dig_target()`，可从任务文本里解析目标地图
- launcher 的 `/api/status` 与 `start-dig` 已接入新的路线/模板/状态机调试信息

## 下一批最该做
1. 接入真实截图接口（Win32/adb 方案二选一，当前项目更偏 Win32）
2. 把模板识别从 mock 替换为 OpenCV 匹配
3. 增加地图坐标 OCR 与“当前场景识别”
4. 增加异常分支：背包已满 / 战斗中 / 未到目标场景 / 挖图失败重试
5. 为真实接入准备模板截图采集脚本
6. 给安装版补应用图标、版本信息、卸载说明

## 打包现状
- 已新增 Inno Setup 安装脚本：`build/mhxy-bot-win10.iss`
- GitHub Actions 现可同时产出：
  - 便携版 `mhxy-bot-win10.exe`
  - 安装版 `mhxy-bot-win10-setup.exe`

## 进入真实接入前需要准备
- Win10 游戏客户端环境
- 固定分辨率
- 主界面 / 背包 / 地图 / 任务栏截图
- 打图目标场景截图
- 挖图动作截图
- 战斗结束截图
