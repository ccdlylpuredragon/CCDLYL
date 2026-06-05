# CCDLYL 用户管理系统

一个基于 Flask 的 Web 应用，提供用户注册、文件上传和数据库管理功能。

## 功能

- **用户注册** - 注册新用户（用户名、邮箱、密码）
- **文件上传** - 上传文件并关联到已注册用户
- **数据库管理** - 查看、管理所有用户和文件记录

## 技术栈

- Python / Flask
- SQLite + Flask-SQLAlchemy
- Bootstrap 5 前端框架

## 快速开始

```bash
# 安装依赖
pip install -r requirements.txt

# 启动应用
python app.py
```

访问 http://localhost:5000 即可使用。

## 支持的文件类型

txt, pdf, png, jpg, jpeg, gif, doc, docx, xls, xlsx, csv, zip

最大文件大小：16 MB
