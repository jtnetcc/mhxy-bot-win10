# mhxy-bot-win10

Win10 单开版梦幻西游端游自动化项目骨架。

## 当前目标
- 端游 PC 端
- 先单开
- 规划并逐步实现：自动打图 / 自动师门 / 自动抓鬼（队长版）
- 支持自动巡线
- 最终打包为 exe

## 当前阶段
- 已完成项目目录初始化
- 已补齐自动打图开发骨架（状态机 / OCR mock / 路线模板 / 模板清单）
- 已接入 Windows 打包与标准安装器工作流

## Windows 打包
- 便携版：GitHub Actions 产出 `mhxy-bot-win10.exe`
- 安装版：GitHub Actions 产出 `mhxy-bot-win10-setup.exe`
- 安装器基于 Inno Setup，支持开始菜单、桌面快捷方式、安装目录

## 目录说明
- `app/`：主程序代码
- `config/`：配置文件
- `assets/`：模板图片、资源文件
- `logs/`：运行日志
- `screenshots/`：异常截图、识别截图
- `docs/`：设计文档、开发计划
- `build/`：打包输出
