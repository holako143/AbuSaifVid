from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List
from arabseed_scraper import ArabSeedScraper

# تهيئة تطبيق FastAPI
app = FastAPI(
    title="ArabSeed Downloader API",
    description="API for scraping latest content and download links from ArabSeed.",
    version="1.0.0"
)

# تهيئة CORS للسماح للواجهة الأمامية بالوصول
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
)

# تهيئة Scraper
scraper = ArabSeedScraper()

# نماذج البيانات (Pydantic Models)
class ContentItem(BaseModel):
    title: str
    url: str
    image_url: str

class DownloadLink(BaseModel):
    quality: str
    server: str
    link: str

# 1. مسار جلب أحدث المحتوى
@app.get("/latest", response_model=List[ContentItem], summary="جلب أحدث الأفلام والمسلسلات")
async def get_latest():
    """
    يجلب قائمة بأحدث الأفلام والمسلسلات المضافة إلى الموقع.
    """
    try:
        latest_content = scraper.get_latest_content()
        return latest_content
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {e}")

# 2. مسار البحث عن محتوى
@app.get("/search", response_model=List[ContentItem], summary="البحث عن فيلم أو مسلسل")
async def search(query: str):
    """
    يبحث عن محتوى (فيلم/مسلسل) باستخدام كلمة مفتاحية.
    """
    if not query:
        raise HTTPException(status_code=400, detail="Query parameter is required.")
    try:
        search_results = scraper.search_content(query)
        return search_results
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {e}")

# 3. مسار جلب روابط التحميل
@app.post("/links", response_model=List[DownloadLink], summary="جلب روابط التحميل والجودات")
async def get_links(item: ContentItem):
    """
    يجلب جميع روابط التحميل المباشرة والجودات المتوفرة لفيلم أو مسلسل محدد.
    """
    if not item.url:
        raise HTTPException(status_code=400, detail="Content URL is required.")
    try:
        download_links = scraper.get_download_links(item.url)
        return download_links
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {e}")

# مسار الصفحة الرئيسية (للتأكد من عمل الـ API)
@app.get("/", summary="حالة الـ API")
async def root():
    return {"message": "ArabSeed Downloader API is running."}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
