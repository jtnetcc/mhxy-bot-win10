import copy
import json
from pathlib import Path

from app.core.pathing import CONFIG_DIR

OVERRIDE_PATH = CONFIG_DIR / 'task_blueprints.override.json'

DEFAULT_TASK_BLUEPRINTS = {
    'dig_treasure': {
        'label': '自动打图',
        'category': 'treasure',
        'steps': [
            {
                'type': '窗口',
                'name': '绑定游戏窗口',
                'desc': '查找标题包含“梦幻西游”的主窗口',
                'settings': [
                    {'label': '窗口标题关键词', 'value': '梦幻西游'},
                    {'label': '匹配模式', 'value': 'contains'},
                    {'label': '单开限制', 'value': 'true'},
                ],
            },
            {
                'type': '图像',
                'name': '识别主界面元素',
                'desc': '识别背包 / 地图 / 任务栏 / 挂机按钮',
                'settings': [
                    {'label': '模板分组', 'value': 'dig-ui.example'},
                    {'label': '最低相似度', 'value': '0.90'},
                    {'label': '失败重试', 'value': '3 次'},
                ],
            },
            {
                'type': 'OCR',
                'name': '读取藏宝图任务',
                'desc': 'OCR 提取藏宝图目标场景文本',
                'settings': [
                    {'label': 'OCR区域', 'value': '[0,0,300,120]'},
                    {'label': '语言', 'value': 'zh-CN'},
                    {'label': '示例文本', 'value': '去长安城郊外挖宝'},
                ],
            },
            {
                'type': '流程',
                'name': '解析目标场景',
                'desc': '从 OCR 文本提取地图名并归一化',
                'settings': [
                    {'label': '解析策略', 'value': '别名归一化'},
                    {'label': '别名样本', 'value': '长安郊外 / 郊外'},
                    {'label': '回退逻辑', 'value': '模板识别目标地图'},
                ],
            },
            {
                'type': '路线',
                'name': '规划巡线路径',
                'desc': '根据配置模板装载 waypoint 列表',
                'settings': [
                    {'label': '路线模板', 'value': 'default'},
                    {'label': '目标场景', 'value': '长安城郊外'},
                    {'label': 'waypoint 数量', 'value': '3'},
                ],
            },
            {
                'type': '鼠标',
                'name': '移动至目标点',
                'desc': '按场景路径模拟移动到挖图点附近',
                'settings': [
                    {'label': '移动模式', 'value': '逐点移动'},
                    {'label': '到达阈值', 'value': '18'},
                    {'label': '卡住重试', 'value': '3 次'},
                ],
            },
            {
                'type': '动作',
                'name': '执行挖图动作',
                'desc': '点击藏宝图并触发挖图流程',
                'settings': [
                    {'label': '动作入口', 'value': '背包 → 藏宝图'},
                    {'label': '执行方式', 'value': '单击 + 等待反馈'},
                    {'label': '超时', 'value': '8 秒'},
                ],
            },
            {
                'type': '判断',
                'name': '奖励/战斗分流',
                'desc': '识别是否进入战斗或直接领奖',
                'settings': [
                    {'label': '分流条件', 'value': '战斗结束图标 / 奖励弹窗'},
                    {'label': '优先级', 'value': '战斗 > 奖励'},
                    {'label': '回链策略', 'value': '处理后回到循环'},
                ],
            },
            {
                'type': '循环',
                'name': '回到下一轮',
                'desc': '准备执行下一次打图循环',
                'settings': [
                    {'label': '最大轮数', 'value': '20'},
                    {'label': '间隔', 'value': '500ms'},
                    {'label': '终止条件', 'value': '背包满 / 手动停止'},
                ],
            },
        ],
    },
    'master_task': {
        'label': '自动师门',
        'category': 'master',
        'steps': [
            {
                'type': '窗口',
                'name': '绑定游戏窗口',
                'desc': '校验当前单开客户端窗口',
                'settings': [
                    {'label': '窗口标题关键词', 'value': '梦幻西游'},
                    {'label': '任务模式', 'value': '师门'},
                    {'label': '窗口校验', 'value': '主界面可见'},
                ],
            },
            {
                'type': '图像',
                'name': '识别师门入口',
                'desc': '识别师门 NPC / 任务栏 / 包裹按钮',
                'settings': [
                    {'label': '模板分组', 'value': 'master-ui'},
                    {'label': '最低相似度', 'value': '0.88'},
                    {'label': '检测区域', 'value': '主界面左侧 + 顶部'},
                ],
            },
            {
                'type': '动作',
                'name': '领取师门任务',
                'desc': '模拟与 NPC 交互并领取师门',
                'settings': [
                    {'label': 'NPC 交互', 'value': '对话点击'},
                    {'label': '领取策略', 'value': '默认选项优先'},
                    {'label': '失败重试', 'value': '2 次'},
                ],
            },
            {
                'type': 'OCR',
                'name': '读取任务文本',
                'desc': '提取师门任务描述与目标 NPC/物品',
                'settings': [
                    {'label': 'OCR区域', 'value': '任务栏文本区域'},
                    {'label': '目标抽取', 'value': 'NPC / 场景 / 物品'},
                    {'label': '示例文本', 'value': '去长寿村找NPC送信'},
                ],
            },
            {
                'type': '分流',
                'name': '任务类型分流',
                'desc': '区分送信 / 巡逻 / 购买 / 上交等子任务',
                'settings': [
                    {'label': '分流类型', 'value': '送信/巡逻/购买/上交'},
                    {'label': '默认策略', 'value': '送信优先'},
                    {'label': '未知任务', 'value': '记日志并暂停'},
                ],
            },
            {
                'type': '路线',
                'name': '规划 NPC 路线',
                'desc': '根据目标 NPC/场景规划移动路线',
                'settings': [
                    {'label': '路线模板', 'value': 'master-default'},
                    {'label': '目标场景', 'value': '长寿村'},
                    {'label': '换图方式', 'value': '地图跳转 + waypoint'},
                ],
            },
            {
                'type': '动作',
                'name': '执行任务交付',
                'desc': '完成送信/购买/提交动作',
                'settings': [
                    {'label': '交付方式', 'value': '对话 / 包裹提交'},
                    {'label': '超时', 'value': '10 秒'},
                    {'label': '结果检查', 'value': '任务栏变化'},
                ],
            },
            {
                'type': '判断',
                'name': '领取下一轮',
                'desc': '检查是否继续下一轮师门任务',
                'settings': [
                    {'label': '最大轮数', 'value': '20'},
                    {'label': '回师门', 'value': '任务完成后立即返回'},
                    {'label': '暂停条件', 'value': '任务类型未知'},
                ],
            },
        ],
    },
    'ghost_hunt_leader': {
        'label': '自动抓鬼（队长）',
        'category': 'ghost',
        'steps': [
            {
                'type': '窗口',
                'name': '绑定游戏窗口',
                'desc': '校验队长号窗口与战斗场景',
                'settings': [
                    {'label': '窗口标题关键词', 'value': '梦幻西游'},
                    {'label': '角色定位', 'value': '队长'},
                    {'label': '场景校验', 'value': '队伍界面可见'},
                ],
            },
            {
                'type': '图像',
                'name': '识别队伍状态',
                'desc': '识别队伍人数 / 自动状态 / 任务面板',
                'settings': [
                    {'label': '队伍人数阈值', 'value': '5/5'},
                    {'label': '自动状态', 'value': '跟随开启'},
                    {'label': '检测频率', 'value': '每轮 1 次'},
                ],
            },
            {
                'type': '动作',
                'name': '领取抓鬼任务',
                'desc': '与钟馗交互领取抓鬼',
                'settings': [
                    {'label': 'NPC', 'value': '钟馗'},
                    {'label': '交互方式', 'value': '默认对话路径'},
                    {'label': '失败重试', 'value': '2 次'},
                ],
            },
            {
                'type': 'OCR',
                'name': '读取目标场景',
                'desc': '提取当前轮抓鬼目标地图',
                'settings': [
                    {'label': 'OCR区域', 'value': '任务栏文本区域'},
                    {'label': '示例目标', 'value': '北俱芦洲'},
                    {'label': '别名归一', 'value': '启用'},
                ],
            },
            {
                'type': '路线',
                'name': '规划前往路线',
                'desc': '通过驿站/场景切换到目标点',
                'settings': [
                    {'label': '路线模板', 'value': 'ghost-default'},
                    {'label': '驿站策略', 'value': '优先最近驿站'},
                    {'label': '目标点', 'value': '鬼点附近'},
                ],
            },
            {
                'type': '动作',
                'name': '触发战斗',
                'desc': '靠近鬼点并进入战斗',
                'settings': [
                    {'label': '接敌方式', 'value': '接近 + 点击'},
                    {'label': '等待时长', 'value': '6 秒'},
                    {'label': '失败处理', 'value': '重新寻路'},
                ],
            },
            {
                'type': '判断',
                'name': '等待战斗结束',
                'desc': '识别战斗结束并恢复队长流程',
                'settings': [
                    {'label': '结束标识', 'value': '战斗结束按钮'},
                    {'label': '检测频率', 'value': '2 秒'},
                    {'label': '超时', 'value': '180 秒'},
                ],
            },
            {
                'type': '循环',
                'name': '继续下一轮抓鬼',
                'desc': '战斗结束后回链重新领取/追踪',
                'settings': [
                    {'label': '最大轮数', 'value': '20'},
                    {'label': '队伍校验', 'value': '每轮复检'},
                    {'label': '终止条件', 'value': '掉队 / 手动停止'},
                ],
            },
        ],
    },
}

_CACHE = None


def _deepcopy(data):
    return copy.deepcopy(data)


def load_task_blueprints():
    global _CACHE
    if _CACHE is not None:
        return _deepcopy(_CACHE)
    if OVERRIDE_PATH.exists():
        try:
            _CACHE = json.loads(OVERRIDE_PATH.read_text(encoding='utf-8'))
            return _deepcopy(_CACHE)
        except Exception:
            pass
    _CACHE = _deepcopy(DEFAULT_TASK_BLUEPRINTS)
    return _deepcopy(_CACHE)


def get_task_blueprints():
    return load_task_blueprints()


def get_task_blueprint(key: str):
    return load_task_blueprints()[key]


def save_task_blueprints(data: dict):
    global _CACHE
    OVERRIDE_PATH.parent.mkdir(parents=True, exist_ok=True)
    OVERRIDE_PATH.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding='utf-8')
    _CACHE = _deepcopy(data)
    return _deepcopy(_CACHE)


def make_default_step(step_type='动作'):
    return {
        'type': step_type,
        'name': f'新{step_type}步骤',
        'desc': '请补充这个步骤的说明',
        'settings': [
            {'label': '参数1', 'value': '待配置'},
            {'label': '参数2', 'value': '待配置'},
        ],
    }
