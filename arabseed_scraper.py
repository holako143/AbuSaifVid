import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, quote
import re
import base64

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
        
        # New selectors for search results
        content_cards = soup.select('div.item__contents')

        for card in content_cards:
            link_tag = card.find('a')
            title_tag = card.find('h3')
            
            if link_tag and title_tag:
                url = link_tag.get('href')
                title = title_tag.text.strip()

                if title and url:
                    if not url.startswith('http'):
                        url = urljoin(BASE_URL, url)
                    results.append({'title': title, 'url': url})

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
        
        # 1. Find the download page link
        download_link_element = soup.find('a', class_='download__btn')
        
        if not download_link_element:
            return []

        download_page_url = download_link_element.get('href')
        if not download_page_url:
            return []
            
        if not download_page_url.startswith('http'):
            download_page_url = urljoin(content_url, download_page_url)

        # 2. Fetch the download page content
        download_html_content = self._fetch_page(download_page_url)
        if not download_html_content:
            return []

        download_soup = BeautifulSoup(download_html_content, 'html.parser')
        
        download_links = []
        
        # 3. Extract links and qualities from the download page
        quality_tabs = download_soup.select('div.tab__inner')

        for tab in quality_tabs:
            quality = tab.get('data-quality', 'غير محدد')
            
            link_items = tab.select('a.download__item')

            for item in link_items:
                server_tag = item.find('h4')
                server = server_tag.text.strip() if server_tag else "غير محدد"
                
                encoded_url = item.get('href')
                
                if encoded_url and '/l/' in encoded_url:
                    try:
                        # Extract the base64 part
                        base64_str = encoded_url.split('/l/')[1]
                        # Decode the URL
                        decoded_url = base64.b64decode(base64_str).decode('utf-8')

                        download_links.append({
                            'quality': quality,
                            'server': server,
                            'link': decoded_url
                        })
                    except (IndexError, base64.binascii.Error, UnicodeDecodeError) as e:
                        print(f"Could not decode URL {encoded_url}: {e}")

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
        
        # New selectors
        content_cards = soup.select('div.slider__single, div.item__contents')
        
        for card in content_cards:
            link_tag = card.find('a')
            title_tag = card.find('h3')
            
            if link_tag and title_tag:
                url = link_tag.get('href')
                title = title_tag.text.strip()

                if title and url:
                    if not url.startswith('http'):
                        url = urljoin(BASE_URL, url)
                    latest_content.append({'title': title, 'url': url})

        # إزالة التكرارات
        unique_content = []
        seen_urls = set()
        for item in latest_content:
            if item['url'] not in seen_urls:
                unique_content.append(item)
                seen_urls.add(item['url'])
                
        return unique_content[:20]
