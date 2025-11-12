import customtkinter as ctk
from arabseed_scraper import ArabSeedScraper
import threading
import webbrowser

# إعدادات الواجهة الرسومية
ctk.set_appearance_mode("System")  # Modes: "System" (default), "Dark", "Light"
ctk.set_default_color_theme("blue")  # Themes: "blue" (default), "green", "dark-blue"

class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        # إعدادات النافذة
        self.title("ArabSeed Downloader - جالب الروابط المباشرة")
        self.geometry("1000x700")
        self.scraper = ArabSeedScraper()

        # إعداد تخطيط الشبكة (Grid Layout)
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        # 1. إطار البحث (Search Frame)
        self.search_frame = ctk.CTkFrame(self)
        self.search_frame.grid(row=0, column=0, padx=20, pady=(20, 10), sticky="ew")
        self.search_frame.grid_columnconfigure(0, weight=1)
        self.search_frame.grid_columnconfigure(1, weight=0)

        self.search_entry = ctk.CTkEntry(self.search_frame, placeholder_text="ابحث عن فيلم أو مسلسل...")
        self.search_entry.grid(row=0, column=0, padx=(10, 5), pady=10, sticky="ew")
        self.search_entry.bind("<Return>", lambda event: self.start_search_thread())

        self.search_button = ctk.CTkButton(self.search_frame, text="بحث", command=self.start_search_thread)
        self.search_button.grid(row=0, column=1, padx=(5, 10), pady=10, sticky="e")

        # 2. إطار المحتوى (Content Frame)
        self.content_frame = ctk.CTkFrame(self)
        self.content_frame.grid(row=1, column=0, padx=20, pady=(10, 20), sticky="nsew")
        self.content_frame.grid_columnconfigure(0, weight=1)
        self.content_frame.grid_rowconfigure(1, weight=1)

        # عنوان المحتوى
        self.content_title = ctk.CTkLabel(self.content_frame, text="أحدث الإضافات", font=ctk.CTkFont(size=20, weight="bold"))
        self.content_title.grid(row=0, column=0, padx=10, pady=(10, 5), sticky="w")

        # إطار التمرير للمحتوى (Scrollable Frame)
        self.scrollable_frame = ctk.CTkScrollableFrame(self.content_frame, label_text="")
        self.scrollable_frame.grid(row=1, column=0, padx=10, pady=(0, 10), sticky="nsew")
        self.scrollable_frame.grid_columnconfigure(0, weight=1)

        # 3. شريط الحالة (Status Bar)
        self.status_bar = ctk.CTkLabel(self, text="جاهز. جاري تحميل أحدث الإضافات...", fg_color="transparent")
        self.status_bar.grid(row=2, column=0, padx=20, pady=(0, 10), sticky="ew")

        # بدء تحميل المحتوى الجديد عند تشغيل التطبيق
        self.start_load_latest_thread()

    def start_load_latest_thread(self):
        """بدء عملية جلب أحدث المحتوى في خيط منفصل"""
        self.status_bar.configure(text="جاري جلب أحدث الإضافات...")
        threading.Thread(target=self.load_latest_content, daemon=True).start()

    def load_latest_content(self):
        """جلب أحدث المحتوى وعرضه"""
        try:
            latest_content = self.scraper.get_latest_content()
            self.after(0, lambda: self.display_content(latest_content, "أحدث الإضافات"))
        except Exception as e:
            self.after(0, lambda: self.status_bar.configure(text=f"خطأ في جلب المحتوى: {e}"))

    def start_search_thread(self):
        """بدء عملية البحث في خيط منفصل"""
        query = self.search_entry.get().strip()
        if not query:
            self.status_bar.configure(text="الرجاء إدخال كلمة للبحث.")
            return

        self.status_bar.configure(text=f"جاري البحث عن: {query}...")
        threading.Thread(target=self.perform_search, args=(query,), daemon=True).start()

    def perform_search(self, query):
        """تنفيذ عملية البحث وعرض النتائج"""
        try:
            search_results = self.scraper.search_content(query)
            self.after(0, lambda: self.display_content(search_results, f"نتائج البحث عن: {query}"))
        except Exception as e:
            self.after(0, lambda: self.status_bar.configure(text=f"خطأ في عملية البحث: {e}"))

    def display_content(self, content_list, title):
        """عرض قائمة المحتوى (أحدث الإضافات أو نتائج البحث)"""
        # مسح المحتوى القديم
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()

        self.content_title.configure(text=title)

        if not content_list:
            no_results_label = ctk.CTkLabel(self.scrollable_frame, text="لا توجد نتائج مطابقة.", font=ctk.CTkFont(size=16))
            no_results_label.grid(row=0, column=0, padx=20, pady=20, sticky="w")
            self.status_bar.configure(text="اكتمل. لا توجد نتائج.")
            return

        # عرض المحتوى في بطاقات
        for i, item in enumerate(content_list):
            self.create_content_card(i, item['title'], item['url'])

        self.status_bar.configure(text=f"اكتمل. تم عرض {len(content_list)} نتيجة.")

    def create_content_card(self, row, title, url):
        """إنشاء بطاقة متحركة (Frame) لكل محتوى"""
        card_frame = ctk.CTkFrame(self.scrollable_frame)
        card_frame.grid(row=row, column=0, padx=10, pady=5, sticky="ew")
        card_frame.grid_columnconfigure(0, weight=1)
        card_frame.grid_columnconfigure(1, weight=0)

        # عنوان الفيلم/المسلسل
        title_label = ctk.CTkLabel(card_frame, text=title, font=ctk.CTkFont(size=14, weight="bold"), anchor="w")
        title_label.grid(row=0, column=0, padx=10, pady=10, sticky="w")

        # زر "جلب الروابط"
        link_button = ctk.CTkButton(card_frame, text="جلب الروابط", command=lambda u=url, t=title: self.start_links_thread(u, t))
        link_button.grid(row=0, column=1, padx=10, pady=10, sticky="e")

        # إطار لعرض الروابط (مخفي مبدئياً)
        links_frame = ctk.CTkFrame(card_frame)
        links_frame.grid(row=1, column=0, columnspan=2, padx=10, pady=(0, 10), sticky="ew")
        links_frame.grid_columnconfigure(0, weight=1)
        links_frame.grid_remove() # إخفاء الإطار مبدئياً
        
        card_frame.links_frame = links_frame # حفظ الإطار كخاصية للبطاقة

    def start_links_thread(self, url, title):
        """بدء عملية جلب الروابط في خيط منفصل"""
        # تحديد البطاقة التي تم الضغط عليها
        button = self.focus_get()
        card_frame = button.master
        
        # إظهار إطار الروابط إذا كان مخفياً، وإخفاؤه إذا كان ظاهراً
        if card_frame.links_frame.winfo_ismapped():
            card_frame.links_frame.grid_remove()
            button.configure(text="جلب الروابط")
            return
        
        # مسح المحتوى القديم من إطار الروابط
        for widget in card_frame.links_frame.winfo_children():
            widget.destroy()
            
        # عرض رسالة "جاري التحميل"
        loading_label = ctk.CTkLabel(card_frame.links_frame, text="جاري جلب الروابط والجودات...", font=ctk.CTkFont(size=12, slant="italic"))
        loading_label.grid(row=0, column=0, padx=10, pady=5, sticky="w")
        card_frame.links_frame.grid() # إظهار الإطار
        button.configure(text="إخفاء الروابط")

        # بدء الجلب في خيط منفصل
        threading.Thread(target=self.fetch_and_display_links, args=(url, card_frame.links_frame, title), daemon=True).start()

    def fetch_and_display_links(self, url, links_frame, title):
        """جلب الروابط وعرضها في الإطار المخصص"""
        try:
            download_links = self.scraper.get_download_links(url)
            self.after(0, lambda: self.display_download_links(download_links, links_frame, title))
        except Exception as e:
            self.after(0, lambda: self.display_error_in_links_frame(links_frame, f"خطأ في جلب الروابط: {e}"))

    def display_download_links(self, download_links, links_frame, title):
        """عرض الروابط المجلوبة في الإطار المخصص"""
        # مسح رسالة "جاري التحميل"
        for widget in links_frame.winfo_children():
            widget.destroy()

        if not download_links:
            no_links_label = ctk.CTkLabel(links_frame, text="لم يتم العثور على روابط تحميل لهذا المحتوى.", font=ctk.CTkFont(size=12, slant="italic"))
            no_links_label.grid(row=0, column=0, padx=10, pady=5, sticky="w")
            return

        # عرض الروابط في جدول
        for i, link_item in enumerate(download_links):
            # الجودة والسيرفر
            info_text = f"[{link_item['quality']}] - {link_item['server']}"
            info_label = ctk.CTkLabel(links_frame, text=info_text, font=ctk.CTkFont(size=12), anchor="w")
            info_label.grid(row=i, column=0, padx=10, pady=2, sticky="w")

            # زر "تحميل مباشر"
            download_button = ctk.CTkButton(links_frame, text="تحميل مباشر", width=100, command=lambda u=link_item['link']: self.open_link(u))
            download_button.grid(row=i, column=1, padx=10, pady=2, sticky="e")

    def display_error_in_links_frame(self, links_frame, error_message):
        """عرض رسالة خطأ في إطار الروابط"""
        for widget in links_frame.winfo_children():
            widget.destroy()
        error_label = ctk.CTkLabel(links_frame, text=error_message, text_color="red", font=ctk.CTkFont(size=12, slant="italic"))
        error_label.grid(row=0, column=0, padx=10, pady=5, sticky="w")

    def open_link(self, url):
        """فتح الرابط في المتصفح الافتراضي"""
        webbrowser.open(url)
        self.status_bar.configure(text=f"تم فتح رابط التحميل في المتصفح: {url[:50]}...")

if __name__ == "__main__":
    app = App()
    app.mainloop()
