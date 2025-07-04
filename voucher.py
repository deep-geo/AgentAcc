import pandas as pd

def generate_voucher(vendor, item_desc, amount, date, mapping):
    summary = f"报销{vendor}{item_desc}费用"
    return pd.DataFrame([
        {
            "日期": date,
            "摘要": summary,
            "科目编码": mapping["debit_code"],
            "科目名称": mapping["debit_name"],
            "借方金额": amount,
            "贷方金额": 0.00
        },
        {
            "日期": date,
            "摘要": summary,
            "科目编码": mapping["credit_code"],
            "科目名称": mapping["credit_name"],
            "借方金额": 0.00,
            "贷方金额": amount
        }
    ])