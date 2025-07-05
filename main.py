from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from mappings import MAPPING_RULES, FUZZY_KEYWORDS
from voucher import generate_voucher
from PIL import Image
import pytesseract
import io
import re
import datetime
import google.generativeai as genai
from pathlib import Path

app = FastAPI()

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
        model = genai.GenerativeModel("gemini-pro")
        response = model.generate_content(prompt)
        return response.text.strip().replace("\n", "")
    except Exception as e:
        print("❌ Gemini出错：", e)
        return ""
        
def fuzzy_match(keyword: str) -> str:
    for fuzzy, target in FUZZY_KEYWORDS.items():
        if fuzzy in keyword:
            return target
    return None

def extract_keyword_from_filename(filename: str) -> str:
    basename = Path(filename).stem
    for key in MAPPING_RULES.keys():
        if key in basename:
            return key
    return None

def classify_keyword(text: str, filename: str) -> str:
    # Step 1: OCR 匹配
    matched_key = next((k for k in MAPPING_RULES if k in text), None)
    if matched_key:
        print("🔍 OCR命中关键词：", matched_key)
        return matched_key

    # Step 2: Gemini 推理
    gemini_key = call_gemini_category(text)
    if gemini_key in MAPPING_RULES:
        print("🤖 Gemini推荐关键词：", gemini_key)
        return gemini_key

    # Step 3: 文件名提取
    filename_key = extract_keyword_from_filename(filename)
    if filename_key in MAPPING_RULES:
        print("📁 文件名提取关键词：", filename_key)
        return filename_key

    # Step 4: fallback
    print("🚨 未识别关键词，使用默认分类")
    return "其他支出"

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

        # Step 1: 固定关键词匹配
        #matched_key = next((k for k in MAPPING_RULES if k in text), None)
        matched_key = classify_keyword(text, filename)

        # Step 2: Gemini 推理（如无匹配）
        # if not matched_key:
        #     gemini_key = call_gemini_category(text)
        #     print("🤖 Gemini建议关键词：", gemini_key)
        #     if gemini_key in MAPPING_RULES:
        #         matched_key = gemini_key

        # # Step 3: 兜底分类
        # if not matched_key:
        #     matched_key = "其他支出"
        #     MAPPING_RULES["其他支出"] = {
        #         "debit_code": "660299",
        #         "debit_name": "管理费用-其他",
        #         "credit_code": "220201",
        #         "credit_name": "其他应付款-员工报销"
        #     }

        if matched_key == "其他支出" and "其他支出" not in MAPPING_RULES:
            MAPPING_RULES["其他支出"] = {
                "debit_code": "660299",
                "debit_name": "管理费用-其他",
                "credit_code": "220201",
                "credit_name": "其他应付款-员工报销"
            }

        # 提取金额
        match = re.search(r"(\d+\.\d{2})", text)
        amount = float(match.group(1)) if match else 0.0
        today = datetime.date.today().isoformat()

        # 生成凭证
        subject = MAPPING_RULES[matched_key]
        df = generate_voucher("自动识别商家", matched_key, amount, today, subject)
        return {
            "matched_keyword": matched_key,
            "voucher": df.to_dict(orient="records"),
            "amount": amount,
            "ocr_text": text 
        }

    except Exception as e:
        return {"error": str(e)}