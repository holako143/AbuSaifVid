import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, quote
import re

BASE_URL = "https://a.asd.homes/"

class ArabSeedScraper:
    def __init__(self):
        # محاكاة متصفح لتجنب الحظر
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Accept-Language': 'ar-EG,ar;q=0.9,en-US;q=0.8,en;q=0.7',
            'Referer': BASE_URL
        }

    def _fetch_page(self, url):
        """جلب محتوى الصفحة باستخدام طلب GET"""
        try:
            # إضافة معالجة لإعادة التوجيه (allow_redirects=True)
            response = requests.get(url, headers=self.headers, timeout=15, allow_redirects=True)
            response.raise_for_status()
            return response.text
        except requests.exceptions.RequestException as e:
            print(f"Error fetching {url}: {e}")
            return None

    def search_content(self, query):
        """
        البحث عن محتوى (فيلم/مسلسل) باستخدام كلمة مفتاحية.
        يعود بقائمة من النتائج: [{title, url}]
        """
        # يتم ترميز الاستعلام للغة العربية
        search_url = urljoin(BASE_URL, f"search/{quote(query)}/")
        
        html_content = self._fetch_page(search_url)
        if not html_content:
            return []

        soup = BeautifulSoup(html_content, 'html.parser')
        results = []
        
        # البحث عن الروابط في نتائج البحث
        # سأبحث عن الروابط التي تحتوي على عنوان المحتوى
        content_links = soup.find_all('a', href=lambda href: href and ('movie' in href or 'series' in href))
            
        for link in content_links:
            title = link.text.strip()
            url = link.get('href')
            
            # تنظيف العنوان من التقييمات والجودة
            title = re.sub(r'^\d+\.\d+\s(افلام|مسلسلات)\s(اجنبي|عربي|تركيه|...)\s', '', title).strip()
            title = re.sub(r'\s\(\s\d+\s\)', '', title).strip() # إزالة السنة بين قوسين
            
            if title and url and url.startswith('http'):
                results.append({'title': title, 'url': url})
            elif title and url and url.startswith('/'):
                full_url = urljoin(BASE_URL, url)
                results.append({'title': title, 'url': full_url})

        # إزالة التكرارات
        unique_results = []
        seen_urls = set()
        for item in results:
            if item['url'] not in seen_urls:
                unique_results.append(item)
                seen_urls.add(item['url'])
                
        return unique_results

    def get_download_links(self, content_url):
        """
        جلب روابط التحميل المباشرة والجودات من صفحة المحتوى.
        يعود بقائمة من الروابط: [{quality, server, link}]
        """
        html_content = self._fetch_page(content_url)
        if not html_content:
            return []

        soup = BeautifulSoup(html_content, 'html.parser')
        
        # 1. البحث عن رابط صفحة التحميل (Download Page Link)
        download_link_element = soup.find('a', text=lambda t: t and 'تحميل الان' in t)
        
        if not download_link_element:
            return []

        download_page_url = download_link_element.get('href')
        if not download_page_url:
            return []
            
        if not download_page_url.startswith('http'):
            download_page_url = urljoin(content_url, download_page_url)

        # 2. جلب محتوى صفحة التحميل
        download_html_content = self._fetch_page(download_page_url)
        if not download_html_content:
            return []

        download_soup = BeautifulSoup(download_html_content, 'html.parser')
        
        download_links = []
        
        # 3. استخراج الروابط والجودات من صفحة التحميل
        # البحث عن كل الروابط التي تحتوي على كلمة "التحميل الان"
        all_download_buttons = download_soup.find_all('a', text=lambda t: t and 'التحميل الان' in t)
        
        for button in all_download_buttons:
            link_url = button.get('href')
            
            # البحث عن العنصر الأب لتحديد السيرفر والجودة
            parent_div = button.find_parent('div')
            if parent_div:
                # محاولة استخراج اسم السيرفر
                server_name_tag = parent_div.find('h4')
                server = server_name_tag.text.strip() if server_name_tag else "غير محدد"
                
                # محاولة استخراج الجودة من نص الزر
                quality_match = [q for q in ['1080p', '720p', '480p', '360p', '240p'] if q in button.text]
                quality = quality_match[0] if quality_match else "غير محدد"
                
                if link_url:
                    download_links.append({
                        'quality': quality,
                        'server': server,
                        'link': link_url
                    })

        return download_links

    def get_latest_content(self):
        """
        جلب أحدث المحتوى من الصفحة الرئيسية.
        يعود بقائمة من النتائج: [{title, url}]
        """
        html_content = self._fetch_page(urljoin(BASE_URL, "main0/"))
        if not html_content:
            return []

        soup = BeautifulSoup(html_content, 'html.parser')
        latest_content = []
        
        # Updated selector to find content cards
        content_cards = soup.select('li.box__xs__2 .item__contents a.movie__block')
        
        for card in content_cards:
            title = card.get('title', '').strip()
            url = card.get('href')
            
            # تنظيف العنوان من التقييمات والجودة
            title = re.sub(r'^\d+\.\d+\s(افلام|مسلسلات)\s(اجنبي|عربي|تركيه|...)\s', '', title).strip()
            title = re.sub(r'\s\(\s\d+\s\)', '', title).strip() # إزالة السنة بين قوسين
            
            if title and url and url.startswith('http'):
                latest_content.append({'title': title, 'url': url})
            elif title and url and url.startswith('/'):
                full_url = urljoin(BASE_URL, url)
                latest_content.append({'title': title, 'url': full_url})

        # إزالة التكرارات
        unique_content = []
        seen_urls = set()
        for item in latest_content:
            if item['url'] not in seen_urls:
                unique_content.append(item)
                seen_urls.add(item['url'])
                
        return unique_content[:20] # العودة بأول 20 عنصر كأحدث محتوى
