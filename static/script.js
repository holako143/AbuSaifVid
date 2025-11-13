// تم تحديث هذا الرابط ليتصل بالـ API المؤقت
const API_BASE_URL = '';

const contentList = document.getElementById('content-list');
const statusMessage = document.getElementById('status-message');
const contentTitle = document.getElementById('content-title');
const searchInput = document.getElementById('search-input');

// دالة لجلب البيانات من الـ API
async function fetchData(endpoint, method = 'GET', body = null) {
    const options = {
        method: method,
        headers: {
            'Content-Type': 'application/json',
        },
    };
    if (body) {
        options.body = JSON.stringify(body);
    }

    try {
        const response = await fetch(`${API_BASE_URL}${endpoint}`, options);
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        return await response.json();
    } catch (error) {
        console.error('Fetch error:', error);
        statusMessage.innerHTML = `<p style="color: ${getComputedStyle(document.documentElement).getPropertyValue('--primary-color')}">خطأ في الاتصال بالخادم أو جلب البيانات. تأكد من تشغيل الـ API.</p>`;
        return null;
    }
}

// دالة لعرض رسالة الحالة
function showStatus(message, isLoading = false) {
    contentList.innerHTML = '';
    statusMessage.style.display = 'block';
    if (isLoading) {
        statusMessage.innerHTML = `<div class="loading-spinner"></div><p>${message}</p>`;
    } else {
        statusMessage.innerHTML = `<p>${message}</p>`;
    }
}

// دالة لجلب أحدث المحتوى
async function loadLatestContent() {
    contentTitle.textContent = 'أحدث الإضافات';
    showStatus('جاري تحميل أحدث الإضافات...', true);
    const data = await fetchData('/latest');
    if (data) {
        displayContent(data);
    }
}

// دالة للبحث عن محتوى
async function searchContent() {
    const query = searchInput.value.trim();
    if (!query) {
        showStatus('الرجاء إدخال كلمة للبحث.');
        return;
    }

    contentTitle.textContent = `نتائج البحث عن: "${query}"`;
    showStatus(`جاري البحث عن: ${query}...`, true);
    const data = await fetchData(`/search?query=${encodeURIComponent(query)}`);
    if (data) {
        displayContent(data);
    }
}

// دالة لعرض قائمة المحتوى
function displayContent(content) {
    statusMessage.style.display = 'none';
    contentList.innerHTML = '';

    if (content.length === 0) {
        showStatus('لا توجد نتائج مطابقة.');
        return;
    }

    content.forEach(item => {
        const card = document.createElement('div');
        card.className = 'content-card';
        card.innerHTML = `
            <h3>${item.title}</h3>
            <button onclick="toggleLinks(this, '${item.url}', '${item.title}')">جلب الروابط</button>
            <div class="links-container" style="display: none;"></div>
        `;
        contentList.appendChild(card);
    });
}

// دالة لتبديل عرض الروابط
async function toggleLinks(button, url, title) {
    const linksContainer = button.nextElementSibling;

    if (linksContainer.style.display === 'block') {
        linksContainer.style.display = 'none';
        button.textContent = 'جلب الروابط';
        return;
    }

    // إخفاء جميع الروابط الأخرى
    document.querySelectorAll('.links-container').forEach(container => {
        if (container !== linksContainer) {
            container.style.display = 'none';
            container.previousElementSibling.textContent = 'جلب الروابط';
        }
    });

    button.textContent = 'جاري الجلب...';
    linksContainer.style.display = 'block';
    linksContainer.innerHTML = `<div class="loading-spinner" style="width: 20px; height: 20px;"></div>`;

    const data = await fetchData('/links', 'POST', { title: title, url: url });

    if (data) {
        displayDownloadLinks(linksContainer, data);
        button.textContent = 'إخفاء الروابط';
    } else {
        linksContainer.innerHTML = `<p style="color: ${getComputedStyle(document.documentElement).getPropertyValue('--primary-color')}">فشل جلب الروابط.</p>`;
        button.textContent = 'جلب الروابط';
    }
}

// دالة لعرض روابط التحميل
function displayDownloadLinks(container, links) {
    container.innerHTML = '';
    if (links.length === 0) {
        container.innerHTML = '<p class="link-info">لم يتم العثور على روابط تحميل.</p>';
        return;
    }

    links.forEach(link => {
        const item = document.createElement('div');
        item.className = 'link-item';
        item.innerHTML = `
            <span class="link-info">[${link.quality}] - ${link.server}</span>
            <a href="${link.link}" target="_blank" class="link-button">تحميل مباشر</a>
        `;
        container.appendChild(item);
    });
}

// بدء تحميل المحتوى عند تحميل الصفحة
window.onload = loadLatestContent;
