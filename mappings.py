MAPPING_RULES = {
    # 🍽 餐饮类
    "奶茶": {"debit_code": "660203", "debit_name": "管理费用-业务招待费", "credit_code": "220201", "credit_name": "其他应付款-员工报销"},
    "饮品": {"debit_code": "660203", "debit_name": "管理费用-业务招待费", "credit_code": "220201", "credit_name": "其他应付款-员工报销"},
    "喜茶": {"debit_code": "660203", "debit_name": "管理费用-业务招待费", "credit_code": "220201", "credit_name": "其他应付款-员工报销"},
    "加班餐": {"debit_code": "660203", "debit_name": "管理费用-加班餐费", "credit_code": "220201", "credit_name": "其他应付款-员工报销"},
    "招待餐": {"debit_code": "660203", "debit_name": "管理费用-业务招待费", "credit_code": "220201", "credit_name": "其他应付款-员工报销"},
    "快餐": {"debit_code": "660203", "debit_name": "管理费用-加班餐费", "credit_code": "220201", "credit_name": "其他应付款-员工报销"},

    # 🚗 差旅/交通类
    "打车": {"debit_code": "660206", "debit_name": "管理费用-交通费", "credit_code": "220201", "credit_name": "其他应付款-员工报销"},
    "出租车": {"debit_code": "660206", "debit_name": "管理费用-交通费", "credit_code": "220201", "credit_name": "其他应付款-员工报销"},
    "滴滴": {"debit_code": "660206", "debit_name": "管理费用-交通费", "credit_code": "220201", "credit_name": "其他应付款-员工报销"},
    "顺风车": {"debit_code": "660206", "debit_name": "管理费用-交通费", "credit_code": "220201", "credit_name": "其他应付款-员工报销"},
    "高铁": {"debit_code": "660205", "debit_name": "管理费用-差旅费", "credit_code": "220201", "credit_name": "其他应付款-员工报销"},
    "机票": {"debit_code": "660205", "debit_name": "管理费用-差旅费", "credit_code": "220201", "credit_name": "其他应付款-员工报销"},
    "差旅费": {"debit_code": "660205", "debit_name": "管理费用-差旅费", "credit_code": "220201", "credit_name": "其他应付款-员工报销"},
    "高速费": {"debit_code": "660206", "debit_name": "管理费用-过路费", "credit_code": "220201", "credit_name": "其他应付款-员工报销"},
    "停车费": {"debit_code": "660206", "debit_name": "管理费用-交通费", "credit_code": "220201", "credit_name": "其他应付款-员工报销"},

    # 🏨 住宿类
    "酒店": {"debit_code": "660210", "debit_name": "管理费用-住宿费", "credit_code": "220201", "credit_name": "其他应付款-员工报销"},
    "华住": {"debit_code": "660210", "debit_name": "管理费用-住宿费", "credit_code": "220201", "credit_name": "其他应付款-员工报销"},
    "汉庭": {"debit_code": "660210", "debit_name": "管理费用-住宿费", "credit_code": "220201", "credit_name": "其他应付款-员工报销"},
    "如家": {"debit_code": "660210", "debit_name": "管理费用-住宿费", "credit_code": "220201", "credit_name": "其他应付款-员工报销"},

    # 🔌 水电物业
    "水费": {"debit_code": "660204", "debit_name": "管理费用-水电费", "credit_code": "220201", "credit_name": "其他应付款-员工报销"},
    "电费": {"debit_code": "660204", "debit_name": "管理费用-水电费", "credit_code": "220201", "credit_name": "其他应付款-员工报销"},
    "物业": {"debit_code": "660215", "debit_name": "管理费用-物业费", "credit_code": "220201", "credit_name": "其他应付款-员工报销"},

    # 🧾 服务与办公费
    "服务费": {"debit_code": "660212", "debit_name": "管理费用-服务费", "credit_code": "220201", "credit_name": "其他应付款-员工报销"},
    "手续费": {"debit_code": "660213", "debit_name": "管理费用-手续费", "credit_code": "220201", "credit_name": "其他应付款-员工报销"},
    "会务费": {"debit_code": "660216", "debit_name": "管理费用-会务费", "credit_code": "220201", "credit_name": "其他应付款-员工报销"},
    "办公用品": {"debit_code": "660202", "debit_name": "管理费用-办公用品", "credit_code": "220201", "credit_name": "其他应付款-员工报销"},
    "打印纸": {"debit_code": "660202", "debit_name": "管理费用-办公用品", "credit_code": "220201", "credit_name": "其他应付款-员工报销"},
    "文具": {"debit_code": "660202", "debit_name": "管理费用-办公用品", "credit_code": "220201", "credit_name": "其他应付款-员工报销"},
    "租金": {"debit_code": "660208", "debit_name": "管理费用-房租", "credit_code": "220201", "credit_name": "其他应付款-员工报销"},

    # 🖥 软件与外包
    "软件服务": {"debit_code": "660209", "debit_name": "管理费用-软件服务费", "credit_code": "220201", "credit_name": "其他应付款-员工报销"},
    "系统服务": {"debit_code": "660209", "debit_name": "管理费用-软件服务费", "credit_code": "220201", "credit_name": "其他应付款-员工报销"},
    "平台服务": {"debit_code": "660209", "debit_name": "管理费用-软件服务费", "credit_code": "220201", "credit_name": "其他应付款-员工报销"},
    "外包": {"debit_code": "660214", "debit_name": "管理费用-外包服务费", "credit_code": "100201", "credit_name": "银行存款"},
    "外包服务": {"debit_code": "660214", "debit_name": "管理费用-外包服务费", "credit_code": "100201", "credit_name": "银行存款"},
    "游戏成本": {"debit_code": "540101", "debit_name": "主营业务成本-游戏开发", "credit_code": "220201", "credit_name": "其他应付款-员工报销"},

    # 💼 人工/工资类
    "工资": {"debit_code": "660101", "debit_name": "管理费用-工资", "credit_code": "221101", "credit_name": "应付职工薪酬-工资"},
    "差补": {"debit_code": "660101", "debit_name": "管理费用-工资", "credit_code": "220201", "credit_name": "其他应付款-员工报销"},

    # 💰 押金/保证金
    "押金": {"debit_code": "122105", "debit_name": "其他应收款-押金", "credit_code": "100201", "credit_name": "银行存款"},
    "卡押金": {"debit_code": "122105", "debit_name": "其他应收款-押金", "credit_code": "100201", "credit_name": "银行存款"},

    # 🧾 快递发票
    "快递": {"debit_code": "660207", "debit_name": "管理费用-邮寄快递费", "credit_code": "220201", "credit_name": "其他应付款-员工报销"},
    "顺丰": {"debit_code": "660207", "debit_name": "管理费用-邮寄快递费", "credit_code": "220201", "credit_name": "其他应付款-员工报销"},
    "中通": {"debit_code": "660207", "debit_name": "管理费用-邮寄快递费", "credit_code": "220201", "credit_name": "其他应付款-员工报销"},

    # ⚠️ fallback
    "其他支出": {"debit_code": "660299", "debit_name": "管理费用-其他", "credit_code": "220201", "credit_name": "其他应付款-员工报销"},
}

FUZZY_KEYWORDS = {
    # 🍹 品牌饮品 → 饮品 / 奶茶
    "喜茶": "奶茶",
    "霸王茶姬": "奶茶",
    "瑞幸": "饮品",
    "星巴克": "饮品",
    "沪上阿姨": "奶茶",

    # 🍱 加班餐饮关键词
    "加班餐": "加班餐",
    "团建餐": "加班餐",
    "晚餐": "加班餐",
    "快餐": "加班餐",
    "盒饭": "加班餐",

    # 🚕 出行相关 → 滴滴/打车/交通费
    "滴滴出行": "滴滴",
    "网约车": "滴滴",
    "打的": "打车",
    "顺风车": "顺风车",
    "高德打车": "打车",

    # 🏨 酒店品牌 → 酒店/住宿
    "华住": "酒店",
    "汉庭": "酒店",
    "如家": "酒店",
    "锦江之星": "酒店",
    "全季酒店": "酒店",

    # ✈️ 差旅相关
    "12306": "高铁",
    "机场": "机票",
    "南方航空": "机票",
    "携程": "差旅费",
    "去哪儿": "差旅费",

    # 🧾 软件平台 → 软件服务
    "金蝶": "软件服务",
    "飞书": "软件服务",
    "企业微信": "软件服务",
    "阿里云": "软件服务",
    "腾讯云": "软件服务",
    "ChatGPT": "软件服务",
    "OpenAI": "软件服务",

    # 📦 快递公司 → 快递
    "顺丰": "快递",
    "圆通": "快递",
    "申通": "快递",
    "中通": "快递",
    "韵达": "快递",
    "极兔": "快递",

    # 🖨 办公用品关键词
    "打印纸": "办公用品",
    "A4纸": "办公用品",
    "文具": "办公用品",
    "笔记本": "办公用品",
    "胶水": "办公用品",
    "文件夹": "办公用品",

    # 🎮 游戏与外包相关
    "外包": "外包",
    "外包服务": "外包",
    "游戏项目": "游戏成本",
    "策划": "游戏成本",
    "美术": "游戏成本",
    "程序开发": "游戏成本",

    # 🧾 财务服务
    "BVI注册": "服务费",
    "记账管理": "服务费",
    "公司年审": "服务费",
    "工商代办": "服务费",
}