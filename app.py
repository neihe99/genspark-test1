from flask import Flask, render_template, jsonify
from flask_cors import CORS
import requests
from bs4 import BeautifulSoup
import time
import random
import re

app = Flask(__name__)
CORS(app)

# 书籍类别配置
BOOK_CATEGORIES = {
    '小说': 'https://book.douban.com/tag/小说',
    '历史': 'https://book.douban.com/tag/历史',
    '科技': 'https://book.douban.com/tag/科技',
    '经济': 'https://book.douban.com/tag/经济',
    '文学': 'https://book.douban.com/tag/文学',
    '哲学': 'https://book.douban.com/tag/哲学',
    '心理学': 'https://book.douban.com/tag/心理学',
    '编程': 'https://book.douban.com/tag/编程'
}

def get_user_agent():
    """随机获取 User-Agent"""
    user_agents = [
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:121.0) Gecko/20100101 Firefox/121.0',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.1 Safari/605.1.15'
    ]
    return random.choice(user_agents)

def extract_rating(rating_text):
    """从评分文本中提取数字"""
    try:
        match = re.search(r'(\d+\.?\d*)', rating_text)
        if match:
            return float(match.group(1))
    except:
        pass
    return 0.0

def scrape_douban_books(category_url, limit=10):
    """爬取豆瓣书籍数据"""
    books = []
    headers = {
        'User-Agent': get_user_agent(),
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
        'Connection': 'keep-alive',
    }
    
    try:
        response = requests.get(category_url, headers=headers, timeout=10)
        response.encoding = 'utf-8'
        
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'lxml')
            
            # 查找书籍列表
            book_items = soup.select('.subject-item')
            
            for item in book_items[:limit]:
                try:
                    # 提取书名
                    title_tag = item.select_one('.info h2 a')
                    title = title_tag.get('title', '').strip() if title_tag else ''
                    
                    # 提取评分
                    rating_tag = item.select_one('.rating_nums')
                    rating = extract_rating(rating_tag.text.strip()) if rating_tag else 0.0
                    
                    # 提取评价人数
                    rating_count_tag = item.select_one('.pl')
                    rating_count_text = rating_count_tag.text.strip() if rating_count_tag else '0人评价'
                    rating_count = re.search(r'(\d+)', rating_count_text)
                    rating_count = int(rating_count.group(1)) if rating_count else 0
                    
                    # 提取作者和出版社
                    pub_tag = item.select_one('.pub')
                    pub_info = pub_tag.text.strip() if pub_tag else ''
                    
                    # 提取图片
                    img_tag = item.select_one('.pic img')
                    cover = img_tag.get('src', '') if img_tag else ''
                    
                    # 提取链接
                    link = title_tag.get('href', '') if title_tag else ''
                    
                    if title and rating > 0:
                        books.append({
                            'title': title,
                            'rating': rating,
                            'rating_count': rating_count,
                            'info': pub_info,
                            'cover': cover,
                            'link': link
                        })
                except Exception as e:
                    print(f"解析书籍项出错: {str(e)}")
                    continue
            
            # 按评分排序
            books.sort(key=lambda x: (x['rating'], x['rating_count']), reverse=True)
            
    except requests.exceptions.RequestException as e:
        print(f"请求出错: {str(e)}")
    except Exception as e:
        print(f"爬取出错: {str(e)}")
    
    return books

def get_mock_books(category, limit=10):
    """获取模拟书籍数据（备用方案）"""
    mock_data = {
        '小说': [
            {'title': '百年孤独', 'rating': 9.3, 'rating_count': 892345, 'info': '[哥伦比亚] 加西亚·马尔克斯 / 范晔 / 南海出版公司', 'cover': '', 'link': ''},
            {'title': '三体', 'rating': 9.2, 'rating_count': 756234, 'info': '刘慈欣 / 重庆出版社', 'cover': '', 'link': ''},
            {'title': '活着', 'rating': 9.1, 'rating_count': 634567, 'info': '余华 / 作家出版社', 'cover': '', 'link': ''},
            {'title': '白夜行', 'rating': 9.0, 'rating_count': 545678, 'info': '[日] 东野圭吾 / 刘姿君 / 南海出版公司', 'cover': '', 'link': ''},
            {'title': '红楼梦', 'rating': 9.6, 'rating_count': 423456, 'info': '曹雪芹 / 人民文学出版社', 'cover': '', 'link': ''},
        ],
        '历史': [
            {'title': '人类简史', 'rating': 9.1, 'rating_count': 567890, 'info': '[以色列] 尤瓦尔·赫拉利 / 林俊宏 / 中信出版社', 'cover': '', 'link': ''},
            {'title': '明朝那些事儿', 'rating': 9.0, 'rating_count': 456789, 'info': '当年明月 / 中国友谊出版公司', 'cover': '', 'link': ''},
            {'title': '万历十五年', 'rating': 8.9, 'rating_count': 345678, 'info': '黄仁宇 / 生活·读书·新知三联书店', 'cover': '', 'link': ''},
            {'title': '全球通史', 'rating': 9.0, 'rating_count': 289456, 'info': '[美] 斯塔夫里阿诺斯 / 吴象婴 / 北京大学出版社', 'cover': '', 'link': ''},
            {'title': '史记', 'rating': 9.5, 'rating_count': 234567, 'info': '司马迁 / 中华书局', 'cover': '', 'link': ''},
        ],
        '科技': [
            {'title': '时间简史', 'rating': 8.8, 'rating_count': 456789, 'info': '[英] 史蒂芬·霍金 / 许明贤 / 湖南科学技术出版社', 'cover': '', 'link': ''},
            {'title': '从一到无穷大', 'rating': 9.1, 'rating_count': 345678, 'info': '[美] 乔治·伽莫夫 / 暴永宁 / 科学出版社', 'cover': '', 'link': ''},
            {'title': '上帝掷骰子吗', 'rating': 8.9, 'rating_count': 234567, 'info': '曹天元 / 北京联合出版公司', 'cover': '', 'link': ''},
            {'title': '失控', 'rating': 8.7, 'rating_count': 189456, 'info': '[美] 凯文·凯利 / 东西文库 / 新星出版社', 'cover': '', 'link': ''},
            {'title': '必然', 'rating': 8.5, 'rating_count': 123456, 'info': '[美] 凯文·凯利 / 周峰 / 电子工业出版社', 'cover': '', 'link': ''},
        ],
        '经济': [
            {'title': '经济学原理', 'rating': 9.0, 'rating_count': 234567, 'info': '[美] 曼昆 / 梁小民 / 北京大学出版社', 'cover': '', 'link': ''},
            {'title': '资本论', 'rating': 9.2, 'rating_count': 189456, 'info': '马克思 / 中共中央编译局 / 人民出版社', 'cover': '', 'link': ''},
            {'title': '国富论', 'rating': 9.0, 'rating_count': 156789, 'info': '[英] 亚当·斯密 / 谢祖钧 / 中央编译出版社', 'cover': '', 'link': ''},
            {'title': '思考，快与慢', 'rating': 8.8, 'rating_count': 234567, 'info': '[美] 丹尼尔·卡尼曼 / 胡晓姣 / 中信出版社', 'cover': '', 'link': ''},
            {'title': '贫穷的本质', 'rating': 8.6, 'rating_count': 123456, 'info': '[美] 阿比吉特·班纳吉 / 景芳 / 中信出版社', 'cover': '', 'link': ''},
        ],
        '文学': [
            {'title': '围城', 'rating': 9.0, 'rating_count': 567890, 'info': '钱钟书 / 人民文学出版社', 'cover': '', 'link': ''},
            {'title': '平凡的世界', 'rating': 9.0, 'rating_count': 456789, 'info': '路遥 / 北京十月文艺出版社', 'cover': '', 'link': ''},
            {'title': '追风筝的人', 'rating': 8.9, 'rating_count': 389456, 'info': '[美] 卡勒德·胡赛尼 / 李继宏 / 上海人民出版社', 'cover': '', 'link': ''},
            {'title': '麦田里的守望者', 'rating': 8.7, 'rating_count': 278901, 'info': '[美] J. D. 塞林格 / 孙仲旭 / 译林出版社', 'cover': '', 'link': ''},
            {'title': '挪威的森林', 'rating': 8.5, 'rating_count': 234567, 'info': '[日] 村上春树 / 林少华 / 上海译文出版社', 'cover': '', 'link': ''},
        ],
        '哲学': [
            {'title': '苏菲的世界', 'rating': 8.9, 'rating_count': 345678, 'info': '[挪威] 乔斯坦·贾德 / 萧宝森 / 作家出版社', 'cover': '', 'link': ''},
            {'title': '沉思录', 'rating': 8.8, 'rating_count': 234567, 'info': '[古罗马] 马可·奥勒留 / 何怀宏 / 中央编译出版社', 'cover': '', 'link': ''},
            {'title': '存在与时间', 'rating': 9.0, 'rating_count': 123456, 'info': '[德] 马丁·海德格尔 / 陈嘉映 / 生活·读书·新知三联书店', 'cover': '', 'link': ''},
            {'title': '理想国', 'rating': 8.7, 'rating_count': 189456, 'info': '[古希腊] 柏拉图 / 郭斌和 / 商务印书馆', 'cover': '', 'link': ''},
            {'title': '查拉图斯特拉如是说', 'rating': 8.9, 'rating_count': 156789, 'info': '[德] 尼采 / 钱春绮 / 生活·读书·新知三联书店', 'cover': '', 'link': ''},
        ],
        '心理学': [
            {'title': '乌合之众', 'rating': 8.6, 'rating_count': 345678, 'info': '[法] 古斯塔夫·勒庞 / 冯克利 / 中央编译出版社', 'cover': '', 'link': ''},
            {'title': '自卑与超越', 'rating': 8.8, 'rating_count': 234567, 'info': '[奥] 阿尔弗雷德·阿德勒 / 曹晚红 / 作家出版社', 'cover': '', 'link': ''},
            {'title': '梦的解析', 'rating': 8.7, 'rating_count': 189456, 'info': '[奥] 弗洛伊德 / 孙名之 / 商务印书馆', 'cover': '', 'link': ''},
            {'title': '影响力', 'rating': 8.9, 'rating_count': 278901, 'info': '[美] 罗伯特·西奥迪尼 / 闾佳 / 万卷出版公司', 'cover': '', 'link': ''},
            {'title': '社会心理学', 'rating': 9.0, 'rating_count': 123456, 'info': '[美] 戴维·迈尔斯 / 侯玉波 / 人民邮电出版社', 'cover': '', 'link': ''},
        ],
        '编程': [
            {'title': '代码大全', 'rating': 9.3, 'rating_count': 123456, 'info': '[美] 史蒂夫·迈克康奈尔 / 金戈 / 电子工业出版社', 'cover': '', 'link': ''},
            {'title': '计算机程序的构造和解释', 'rating': 9.5, 'rating_count': 89456, 'info': '[美] Harold Abelson / 裘宗燕 / 机械工业出版社', 'cover': '', 'link': ''},
            {'title': 'Python编程：从入门到实践', 'rating': 9.1, 'rating_count': 156789, 'info': '[美] 埃里克·马瑟斯 / 袁国忠 / 人民邮电出版社', 'cover': '', 'link': ''},
            {'title': '深度学习', 'rating': 8.8, 'rating_count': 67890, 'info': '[美] Ian Goodfellow / 赵申剑 / 人民邮电出版社', 'cover': '', 'link': ''},
            {'title': 'JavaScript高级程序设计', 'rating': 9.2, 'rating_count': 134567, 'info': '[美] 马特·弗里斯比 / 李松峰 / 人民邮电出版社', 'cover': '', 'link': ''},
        ]
    }
    
    return mock_data.get(category, [])[:limit]

@app.route('/')
def index():
    """主页"""
    return render_template('index.html')

@app.route('/api/books')
def get_books():
    """获取所有分类的书籍数据"""
    all_books = {}
    
    for category, url in BOOK_CATEGORIES.items():
        print(f"正在获取 {category} 类书籍...")
        
        # 尝试爬取真实数据
        books = scrape_douban_books(url, limit=10)
        
        # 如果爬取失败，使用模拟数据
        if not books:
            print(f"{category} 类书籍爬取失败，使用模拟数据")
            books = get_mock_books(category, limit=10)
        
        all_books[category] = books
        
        # 添加延迟，避免请求过快
        time.sleep(random.uniform(0.5, 1.5))
    
    return jsonify(all_books)

@app.route('/api/books/<category>')
def get_books_by_category(category):
    """获取指定分类的书籍数据"""
    if category not in BOOK_CATEGORIES:
        return jsonify({'error': '分类不存在'}), 404
    
    url = BOOK_CATEGORIES[category]
    books = scrape_douban_books(url, limit=10)
    
    # 如果爬取失败，使用模拟数据
    if not books:
        books = get_mock_books(category, limit=10)
    
    return jsonify({category: books})

@app.route('/api/categories')
def get_categories():
    """获取所有分类"""
    return jsonify(list(BOOK_CATEGORIES.keys()))

@app.route('/api/stats')
def get_stats():
    """获取统计数据"""
    all_books = {}
    
    for category, url in BOOK_CATEGORIES.items():
        books = scrape_douban_books(url, limit=10)
        if not books:
            books = get_mock_books(category, limit=10)
        all_books[category] = books
        time.sleep(random.uniform(0.5, 1.5))
    
    # 计算统计数据
    stats = {
        'total_categories': len(all_books),
        'total_books': sum(len(books) for books in all_books.values()),
        'avg_rating_by_category': {},
        'top_rated_books': []
    }
    
    # 计算每个分类的平均评分
    for category, books in all_books.items():
        if books:
            avg_rating = sum(book['rating'] for book in books) / len(books)
            stats['avg_rating_by_category'][category] = round(avg_rating, 2)
    
    # 获取评分最高的书籍
    all_books_flat = []
    for category, books in all_books.items():
        for book in books:
            book_copy = book.copy()
            book_copy['category'] = category
            all_books_flat.append(book_copy)
    
    all_books_flat.sort(key=lambda x: (x['rating'], x['rating_count']), reverse=True)
    stats['top_rated_books'] = all_books_flat[:10]
    
    return jsonify(stats)

if __name__ == '__main__':
    print("🚀 豆瓣书籍评分可视化系统启动中...")
    print("📊 访问地址: http://localhost:5000")
    print("=" * 50)
    app.run(host='0.0.0.0', port=5000, debug=True)
