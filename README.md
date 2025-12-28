# 豆瓣书籍评分可视化系统

一个实时获取豆瓣书籍评分并可视化展示各类高分书籍的网页应用。

## 功能特性

- 🔍 实时爬取豆瓣书籍数据
- 📊 多类别书籍分类展示（小说、历史、科技、经济、文学等）
- 📈 交互式图表可视化展示
- 🎯 高分书籍筛选与排序
- 🎨 现代化响应式设计

## 技术栈

- 后端：Python Flask
- 前端：HTML5, CSS3, JavaScript
- 数据可视化：Chart.js
- 数据爬取：BeautifulSoup4, Requests

## 安装运行

### 1. 安装依赖

```bash
pip install -r requirements.txt
```

### 2. 启动应用

```bash
python app.py
```

### 3. 访问应用

打开浏览器访问：`http://localhost:5000`

## 项目结构

```
.
├── app.py              # Flask 后端服务器
├── requirements.txt    # Python 依赖
├── static/            # 静态资源
│   ├── style.css      # 样式文件
│   └── script.js      # 前端 JavaScript
└── templates/         # HTML 模板
    └── index.html     # 主页面
```

## 使用说明

1. 页面加载时自动获取各类书籍数据
2. 查看不同类别的高分书籍排行
3. 通过图表查看评分分布
4. 点击刷新按钮获取最新数据

## 注意事项

- 数据来源于豆瓣网站，请合理使用
- 建议添加请求间隔，避免频繁访问
- 仅供学习和研究使用
