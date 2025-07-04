from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from mappings import MAPPING_RULES
from voucher import generate_voucher
from PIL import Image
import pytesseract
import io
import re
import datetime

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
def health_check():
    return {"message": "📄 Accounting PoC is live!"}
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
            from PIL import Image
            image = Image.open(io.BytesIO(content))

        # OCR识别
        import pytesseract
        text = pytesseract.image_to_string(image, lang="chi_sim+eng")
        print("🧾 OCR识别结果：", text)

        # 匹配关键词
        from mappings import MAPPING_RULES
        matched_key = next((k for k in MAPPING_RULES if k in text), None)
        if not matched_key:
            return {"error": "未识别分类关键词"}

        import re, datetime
        match = re.search(r"(\d+\.\d{2})", text)
        amount = float(match.group(1)) if match else 0.0
        today = datetime.date.today().isoformat()

        from voucher import generate_voucher
        df = generate_voucher("自动识别商家", matched_key, amount, today, MAPPING_RULES[matched_key])
        return {"voucher": df.to_dict(orient="records")}

    except Exception as e:
        return {"error": str(e)}