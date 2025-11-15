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
        يعود بقائمة من النتائج: [{title, url, image_url}]
        """
        # يتم ترميز الاستعلام للغة العربية
        search_url = urljoin(BASE_URL, f"search/{quote(query)}/")
        
        html_content = self._fetch_page(search_url)
        if not html_content:
            return []

        soup = BeautifulSoup(html_content, 'html.parser')
        results = []
        
        # More specific selector for search result items
        content_items = soup.select('.widget-body .item__contents')
            
        for item in content_items:
            link_element = item.select_one('a.movie__block')
            if not link_element:
                continue

            title = link_element.get('title', '').strip()
            url = link_element.get('href')
            
            image_element = item.select_one('img')
            # Try to get 'data-src' first, then fall back to 'src'
            image_url = ''
            if image_element:
                image_url = image_element.get('data-src', image_element.get('src', ''))
            if not image_url:
                image_url = 'x'

            # تنظيف العنوان من التقييمات والجودة
            title = re.sub(r'^\d+\.\d+\s(افلام|مسلسلات)\s(اجنبي|عربي|تركيه|...)\s', '', title).strip()
            title = re.sub(r'\s\(\s\d+\s\)', '', title).strip() # إزالة السنة بين قوسين
            
            if title and url:
                full_url = url if url.startswith('http') else urljoin(BASE_URL, url)
                results.append({'title': title, 'url': full_url, 'image_url': image_url})

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
        
        # 1. Find the download page link (new, more specific selector)
        download_link_element = soup.select_one('.watch__and__download a.download__btn')
        
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
        
        # 3. Extract links and qualities from the download page (updated logic)
        download_items = download_soup.select('.downloads__list li')

        for item in download_items:
            link_element = item.select_one('a')
            if not link_element:
                continue
            
            link_url = link_element.get('href')

            quality = "غير محدد"
            quality_element = item.select_one('.quality span')
            if quality_element:
                quality = quality_element.text.strip()

            server = "غير محدد"
            server_element = item.select_one('.server span')
            if server_element:
                server = server_element.text.strip()

            if link_url:
                download_links.append({
                    'quality': quality,
                    'server': server,
                    'link': link_url
                })

        return download_links

    def _scrape_content_page(self, page_path):
        """دالة عامة لكشط المحتوى من صفحة معينة."""
        html_content = self._fetch_page(urljoin(BASE_URL, page_path))
        if not html_content:
            return []

        soup = BeautifulSoup(html_content, 'html.parser')
        content_list = []
        
        content_items = soup.select('li.box__xs__2 .item__contents, .widget-body .item__contents')
        
        for item in content_items:
            link_element = item.select_one('a.movie__block')
            if not link_element:
                continue

            title = link_element.get('title', '').strip()
            url = link_element.get('href')

            image_element = item.select_one('img')
            image_url = ''
            if image_element:
                image_url = image_element.get('data-src', image_element.get('src', ''))
            if not image_url:
                image_url = 'x'

            title = re.sub(r'^\d+\.\d+\s(افلام|مسلسلات)\s(اجنبي|عربي|تركيه|...)\s', '', title).strip()
            title = re.sub(r'\s\(\s\d+\s\)', '', title).strip()
            
            if title and url:
                full_url = url if url.startswith('http') else urljoin(BASE_URL, url)
                content_list.append({'title': title, 'url': full_url, 'image_url': image_url})

        unique_content = []
        seen_urls = set()
        for item in content_list:
            if item['url'] not in seen_urls:
                unique_content.append(item)
                seen_urls.add(item['url'])
                
        return unique_content[:20]

    def get_latest_content(self):
        """جلب أحدث المحتوى من الصفحة الرئيسية."""
        return self._scrape_content_page("main0/")

    def get_latest_movies(self):
        """جلب أحدث الأفلام."""
        return self._scrape_content_page("category/افلام-اجنبية/")

    def get_latest_tvshows(self):
        """جلب أحدث المسلسلات."""
        return self._scrape_content_page("category/مسلسلات-اجنبية/")
