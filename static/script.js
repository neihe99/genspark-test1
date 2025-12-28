// 全局变量
let allBooksData = {};
let currentCategory = 'all';
let categoryChart = null;
let ratingDistributionChart = null;

// 页面加载完成后执行
document.addEventListener('DOMContentLoaded', function() {
    console.log('📚 豆瓣书籍评分可视化系统启动');
    loadAllBooks();
    
    // 绑定刷新按钮
    document.getElementById('refreshBtn').addEventListener('click', function() {
        console.log('🔄 刷新数据');
        loadAllBooks();
    });
});

// 加载所有书籍数据
async function loadAllBooks() {
    showLoading(true);
    hideAllSections();
    
    try {
        const response = await fetch('/api/books');
        if (!response.ok) {
            throw new Error('获取数据失败');
        }
        
        allBooksData = await response.json();
        console.log('✅ 数据加载成功', allBooksData);
        
        // 显示数据
        displayStats();
        displayCharts();
        displayCategories();
        displayBooks('all');
        displayTopBooks();
        
        showLoading(false);
        showAllSections();
        
    } catch (error) {
        console.error('❌ 加载数据失败:', error);
        showLoading(false);
        showError('数据加载失败，请稍后重试');
    }
}

// 显示/隐藏加载状态
function showLoading(show) {
    document.getElementById('loading').style.display = show ? 'block' : 'none';
}

// 隐藏所有内容区域
function hideAllSections() {
    document.getElementById('statsSection').style.display = 'none';
    document.getElementById('chartsSection').style.display = 'none';
    document.getElementById('categoriesSection').style.display = 'none';
    document.getElementById('booksSection').style.display = 'none';
    document.getElementById('topBooksSection').style.display = 'none';
}

// 显示所有内容区域
function showAllSections() {
    document.getElementById('statsSection').style.display = 'block';
    document.getElementById('chartsSection').style.display = 'grid';
    document.getElementById('categoriesSection').style.display = 'block';
    document.getElementById('booksSection').style.display = 'block';
    document.getElementById('topBooksSection').style.display = 'block';
}

// 显示错误信息
function showError(message) {
    const loading = document.getElementById('loading');
    loading.innerHTML = `
        <div class="empty-state">
            <div class="empty-state-icon">❌</div>
            <div class="empty-state-text">${message}</div>
        </div>
    `;
}

// 显示统计数据
function displayStats() {
    let totalBooks = 0;
    let totalRating = 0;
    let highRatedCount = 0;
    
    for (const category in allBooksData) {
        const books = allBooksData[category];
        totalBooks += books.length;
        
        books.forEach(book => {
            totalRating += book.rating;
            if (book.rating >= 8.5) {
                highRatedCount++;
            }
        });
    }
    
    const avgRating = totalBooks > 0 ? (totalRating / totalBooks).toFixed(1) : 0;
    
    document.getElementById('totalCategories').textContent = Object.keys(allBooksData).length;
    document.getElementById('totalBooks').textContent = totalBooks;
    document.getElementById('avgRating').textContent = avgRating;
    document.getElementById('highRatedCount').textContent = highRatedCount;
}

// 显示图表
function displayCharts() {
    displayCategoryChart();
    displayRatingDistributionChart();
}

// 显示分类平均评分图表
function displayCategoryChart() {
    const ctx = document.getElementById('categoryChart');
    
    const categories = [];
    const avgRatings = [];
    const colors = [
        '#667eea', '#764ba2', '#f093fb', '#f5576c',
        '#4facfe', '#00f2fe', '#43e97b', '#38f9d7'
    ];
    
    for (const category in allBooksData) {
        const books = allBooksData[category];
        if (books.length > 0) {
            const avgRating = books.reduce((sum, book) => sum + book.rating, 0) / books.length;
            categories.push(category);
            avgRatings.push(avgRating.toFixed(2));
        }
    }
    
    if (categoryChart) {
        categoryChart.destroy();
    }
    
    categoryChart = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: categories,
            datasets: [{
                label: '平均评分',
                data: avgRatings,
                backgroundColor: colors,
                borderColor: colors,
                borderWidth: 2,
                borderRadius: 8,
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: true,
            plugins: {
                legend: {
                    display: false
                },
                tooltip: {
                    backgroundColor: 'rgba(0, 0, 0, 0.8)',
                    padding: 12,
                    titleFont: {
                        size: 14
                    },
                    bodyFont: {
                        size: 13
                    }
                }
            },
            scales: {
                y: {
                    beginAtZero: true,
                    max: 10,
                    ticks: {
                        font: {
                            size: 12
                        }
                    },
                    grid: {
                        color: 'rgba(0, 0, 0, 0.05)'
                    }
                },
                x: {
                    ticks: {
                        font: {
                            size: 12
                        }
                    },
                    grid: {
                        display: false
                    }
                }
            }
        }
    });
}

// 显示评分分布图表
function displayRatingDistributionChart() {
    const ctx = document.getElementById('ratingDistributionChart');
    
    // 统计评分分布
    const ratingRanges = {
        '9.0-10.0': 0,
        '8.5-8.9': 0,
        '8.0-8.4': 0,
        '7.5-7.9': 0,
        '7.0-7.4': 0,
        '< 7.0': 0
    };
    
    for (const category in allBooksData) {
        allBooksData[category].forEach(book => {
            const rating = book.rating;
            if (rating >= 9.0) ratingRanges['9.0-10.0']++;
            else if (rating >= 8.5) ratingRanges['8.5-8.9']++;
            else if (rating >= 8.0) ratingRanges['8.0-8.4']++;
            else if (rating >= 7.5) ratingRanges['7.5-7.9']++;
            else if (rating >= 7.0) ratingRanges['7.0-7.4']++;
            else ratingRanges['< 7.0']++;
        });
    }
    
    if (ratingDistributionChart) {
        ratingDistributionChart.destroy();
    }
    
    ratingDistributionChart = new Chart(ctx, {
        type: 'doughnut',
        data: {
            labels: Object.keys(ratingRanges),
            datasets: [{
                data: Object.values(ratingRanges),
                backgroundColor: [
                    '#f39c12',
                    '#e74c3c',
                    '#9b59b6',
                    '#3498db',
                    '#1abc9c',
                    '#95a5a6'
                ],
                borderWidth: 2,
                borderColor: '#fff'
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: true,
            plugins: {
                legend: {
                    position: 'right',
                    labels: {
                        font: {
                            size: 13
                        },
                        padding: 15
                    }
                },
                tooltip: {
                    backgroundColor: 'rgba(0, 0, 0, 0.8)',
                    padding: 12,
                    titleFont: {
                        size: 14
                    },
                    bodyFont: {
                        size: 13
                    }
                }
            }
        }
    });
}

// 显示分类标签
function displayCategories() {
    const container = document.getElementById('categoryTabs');
    container.innerHTML = '';
    
    // 添加"全部"标签
    const allTab = document.createElement('div');
    allTab.className = 'category-tab active';
    allTab.textContent = '全部';
    allTab.onclick = () => selectCategory('all', allTab);
    container.appendChild(allTab);
    
    // 添加各分类标签
    for (const category in allBooksData) {
        const tab = document.createElement('div');
        tab.className = 'category-tab';
        tab.textContent = `${category} (${allBooksData[category].length})`;
        tab.onclick = () => selectCategory(category, tab);
        container.appendChild(tab);
    }
}

// 选择分类
function selectCategory(category, element) {
    currentCategory = category;
    
    // 更新激活状态
    document.querySelectorAll('.category-tab').forEach(tab => {
        tab.classList.remove('active');
    });
    element.classList.add('active');
    
    // 显示对应书籍
    displayBooks(category);
}

// 显示书籍列表
function displayBooks(category) {
    const container = document.getElementById('booksList');
    const titleElement = document.getElementById('currentCategory');
    
    let books = [];
    
    if (category === 'all') {
        titleElement.textContent = '所有书籍';
        for (const cat in allBooksData) {
            books = books.concat(allBooksData[cat].map(book => ({
                ...book,
                category: cat
            })));
        }
    } else {
        titleElement.textContent = `${category} 类书籍`;
        books = allBooksData[category].map(book => ({
            ...book,
            category: category
        }));
    }
    
    // 按评分排序
    books.sort((a, b) => {
        if (b.rating !== a.rating) {
            return b.rating - a.rating;
        }
        return b.rating_count - a.rating_count;
    });
    
    container.innerHTML = '';
    
    if (books.length === 0) {
        container.innerHTML = `
            <div class="empty-state">
                <div class="empty-state-icon">📚</div>
                <div class="empty-state-text">暂无书籍数据</div>
            </div>
        `;
        return;
    }
    
    books.forEach(book => {
        const bookCard = createBookCard(book);
        container.appendChild(bookCard);
    });
}

// 创建书籍卡片
function createBookCard(book) {
    const card = document.createElement('div');
    card.className = 'book-card';
    
    const stars = '⭐'.repeat(Math.round(book.rating / 2));
    const coverHtml = book.cover 
        ? `<img src="${book.cover}" alt="${book.title}" class="book-cover">`
        : `<div class="book-cover-placeholder">📖</div>`;
    
    const linkHtml = book.link 
        ? `<a href="${book.link}" target="_blank" class="book-link">查看详情 →</a>`
        : '';
    
    const categoryTag = book.category 
        ? `<span style="display: inline-block; padding: 4px 10px; background: #667eea; color: white; border-radius: 10px; font-size: 0.85em; margin-bottom: 8px;">${book.category}</span>`
        : '';
    
    card.innerHTML = `
        <div class="book-header">
            ${coverHtml}
            <div class="book-basic-info">
                ${categoryTag}
                <div class="book-title">${book.title}</div>
                <div class="book-rating">
                    <span class="rating-score">${book.rating}</span>
                    <span class="rating-stars">${stars}</span>
                </div>
                <div class="rating-count">${book.rating_count.toLocaleString()} 人评价</div>
            </div>
        </div>
        <div class="book-info">${book.info}</div>
        ${linkHtml}
    `;
    
    return card;
}

// 显示 Top 10 书籍
function displayTopBooks() {
    const container = document.getElementById('topBooksList');
    
    let allBooks = [];
    for (const category in allBooksData) {
        allBooks = allBooks.concat(allBooksData[category].map(book => ({
            ...book,
            category: category
        })));
    }
    
    // 按评分和评价人数排序
    allBooks.sort((a, b) => {
        if (b.rating !== a.rating) {
            return b.rating - a.rating;
        }
        return b.rating_count - a.rating_count;
    });
    
    const top10 = allBooks.slice(0, 10);
    
    container.innerHTML = '';
    
    top10.forEach((book, index) => {
        const item = document.createElement('div');
        item.className = 'top-book-item';
        
        let rankClass = '';
        if (index === 0) rankClass = 'gold';
        else if (index === 1) rankClass = 'silver';
        else if (index === 2) rankClass = 'bronze';
        
        const stars = '⭐'.repeat(Math.round(book.rating / 2));
        
        item.innerHTML = `
            <div class="top-rank ${rankClass}">#${index + 1}</div>
            <div class="top-book-info">
                <div class="top-book-title">${book.title}</div>
                <span class="top-book-category">${book.category}</span>
                <div class="top-book-meta">${book.info}</div>
            </div>
            <div class="top-book-rating">
                <div class="top-rating-score">${book.rating}</div>
                <div class="rating-stars">${stars}</div>
                <div class="top-rating-count">${book.rating_count.toLocaleString()} 评价</div>
            </div>
        `;
        
        container.appendChild(item);
    });
}

// 工具函数：格式化数字
function formatNumber(num) {
    if (num >= 10000) {
        return (num / 10000).toFixed(1) + '万';
    }
    return num.toLocaleString();
}

console.log('✅ 脚本加载完成');
