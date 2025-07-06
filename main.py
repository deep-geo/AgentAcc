from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from mappings import MAPPING_RULES, FUZZY_KEYWORDS
from voucher import generate_voucher
from PIL import Image
import pytesseract
import io
import re
import os
import datetime
import google.generativeai as genai
from pathlib import Path

app = FastAPI()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def hello():
    return {"message": "OCR backend running"}

@app.get("/health")
def health_check():
    return {"message": "📄 Accounting PoC is live!"}

# Gemini 分类函数
def call_gemini_category(text: str) -> str:
    prompt = f"""
你是一个会计助理。请根据以下中文发票内容，判断应归属的会计科目，仅返回一个最匹配的关键词。
---
{text}
---
常见关键词包括：奶茶、饮品、出租车、滴滴、打车、差旅、办公用品、软件、快递、住宿、水电等。
"""
    try:
        model = genai.GenerativeModel("gemini-1.5-pro")
        response = model.generate_content(prompt)
        return response.text.strip().replace("\n", "")
    except Exception as e:
        print("❌ Gemini出错：", e)
        return ""

def fuzzy_match(text: str) -> str:
    for fuzzy in sorted(FUZZY_KEYWORDS, key=lambda k: -len(k)):
        if fuzzy in text:
            return FUZZY_KEYWORDS[fuzzy]
    return None


def parse_filename(filename: str) -> dict:
    basename = Path(filename).stem
    keyword = None
    amount = None
    date = None

    # ✅ 优先匹配最长关键词，避免“服务费”覆盖“外包服务”
    for key in sorted(MAPPING_RULES, key=lambda k: -len(k)):
        if key in basename:
            keyword = key
            break

    # ✅ 模糊匹配 fallback
    if not keyword:
        fuzzy_key = fuzzy_match(basename)
        if fuzzy_key and fuzzy_key in MAPPING_RULES:
            keyword = fuzzy_key

    match_amount = re.search(r"(\d+\.\d{2})", basename)
    if match_amount:
        amount = float(match_amount.group(1))

    match_date = re.search(r"(\d{4}-\d{2}-\d{2})", basename)
    if match_date:
        date = match_date.group(1)

    return {
        "keyword": keyword,
        "amount": amount,
        "date": date
    }

def classify_keyword(text: str, filename: str) -> str:
    # Step 1: 文件名匹配（精确）
    parsed = parse_filename(filename)
    filename_key = parsed.get("keyword")
    if filename_key in MAPPING_RULES:
        print("📁 文件名关键词：", filename_key)
        return filename_key

    # Step 1b: 文件名模糊匹配
    mapped = fuzzy_match(filename_key or "")
    if mapped and mapped in MAPPING_RULES:
        print("📁 文件名模糊匹配：", filename_key, "→", mapped)
        return mapped

    # Step 2: OCR 精确匹配
    for key in MAPPING_RULES:
        if key in text:
            print("🔍 OCR命中关键词：", key)
            return key

    # Step 2b: OCR 模糊匹配
    mapped = fuzzy_match(text)
    if mapped and mapped in MAPPING_RULES:
        print("🌀 OCR模糊匹配：→", mapped)
        return mapped

    # Step 3: Gemini 推理
    gemini_key = call_gemini_category(text)
    if gemini_key in MAPPING_RULES:
        print("🤖 Gemini推荐关键词：", gemini_key)
        return gemini_key

    # Step 3b: Gemini 模糊匹配
    mapped = fuzzy_match(gemini_key or "")
    if mapped and mapped in MAPPING_RULES:
        print("🤖 Gemini模糊匹配：", gemini_key, "→", mapped)
        return mapped

    # Step 4: fallback
    print("🚨 fallback 到其他支出")
    return "其他支出"

def extract_vendor_name(text: str) -> str:
    """
    提取销售方公司名称：匹配所有“名称:xxx”字段，排除“项目名称”、“规格型号”等噪音信息，取最后一个可能的公司名。
    """
    # 提取所有 名称: xxx
    candidates = re.findall(r"名称[:：]?\s*([^\n]{4,30})", text)
    
    # 排除常见非公司名称字段（如“项目名称”、“单价”、“单位”等）
    filtered = [
        c.strip() for c in candidates
        if not any(excl in c for excl in ["项目名称", "规格", "单价", "单位", "数量", "税额", "价税"])
    ]

    if filtered:
        chosen = filtered[-1]
        print("🏢 可疑公司名称候选：", filtered)
        print("✅ 选择最后一个公司名（销售方）：", chosen)
        return chosen
    
    return "自动识别商家"


@app.post("/api/generate-voucher")
async def generate_voucher_api(file: UploadFile = File(...)):
    try:
        filename = file.filename.lower()
        content_type = file.content_type
        content = await file.read()

        # 判断是否是 PDF
        is_pdf = filename.endswith(".pdf") or content_type == "application/pdf"
        if is_pdf:
            from pdf2image import convert_from_bytes
            images = convert_from_bytes(content)
            image = images[0]  # 默认取第一页
        else:
            image = Image.open(io.BytesIO(content))

        # OCR识别
        text = pytesseract.image_to_string(image, lang="chi_sim+eng")
        print("🧾 OCR识别结果：", text)

        matched_key = classify_keyword(text, filename)

        if matched_key == "其他支出" and "其他支出" not in MAPPING_RULES:
            MAPPING_RULES["其他支出"] = {
                "debit_code": "660299",
                "debit_name": "管理费用-其他",
                "credit_code": "220201",
                "credit_name": "其他应付款-员工报销"
            }

        # 提取金额
        # 使用文件名优先提取 amount 和 date
        parsed = parse_filename(filename)

        # 金额优先来自文件名，其次 OCR
        match = re.search(r"(\d+\.\d{2})", text)
        amount = parsed.get("amount") or (float(match.group(1)) if match else 0.0)

        # 日期优先来自文件名，其次今天
        today = parsed.get("date") or datetime.date.today().isoformat()

        # 生成凭证
        subject = MAPPING_RULES[matched_key]
        vendor = extract_vendor_name(text)
        df = generate_voucher(vendor, matched_key, amount, today, subject)
        return {
            "matched_keyword": matched_key,
            "voucher": df.to_dict(orient="records"),
            "amount": f"{amount:.2f}",
            "ocr_text": text 
        }

    except Exception as e:
        return {"error": str(e)}