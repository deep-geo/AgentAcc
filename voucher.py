import pandas as pd

# def generate_voucher(vendor, item_desc, amount, date, mapping):
#     summary = f"报销{vendor}{item_desc}费用"
#     return pd.DataFrame([
#         {
#             "日期": date,
#             "摘要": summary,
#             "科目编码": mapping["debit_code"],
#             "科目名称": mapping["debit_name"],
#             "借方金额": amount,
#             "贷方金额": 0.00
#         },
#         {
#             "日期": date,
#             "摘要": summary,
#             "科目编码": mapping["credit_code"],
#             "科目名称": mapping["credit_name"],
#             "借方金额": 0.00,
#             "贷方金额": amount
#         }
#     ])


def generate_voucher(vendor, keyword, amount, date, subject):
    """
    生成会计凭证 DataFrame
    :param vendor: 发票商家名称
    :param keyword: 分类关键词
    :param amount: 金额（含税）
    :param date: 日期（ISO 格式）
    :param subject: MAPPING_RULES[keyword] 对应的借贷科目信息
    :return: pandas.DataFrame
    """
    return pd.DataFrame([{
        "日期": date,
        "摘要": f"{vendor} - {keyword}",
        "借方科目": subject["debit_name"],
        "借方科目编码": subject["debit_code"],
        "贷方科目": subject["credit_name"],
        "贷方科目编码": subject["credit_code"],
        "金额": round(amount, 2)
    }])