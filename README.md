# blog-django

A simple blog application built with Django. Users can read blog posts, and admin can create, update, or delete posts.

---

## 🔧 Features

- User-friendly blog home page
- Post detail view
- Admin login
- Add/Edit/Delete blog posts
- Image upload support

---

## 📁 Project Structure

```
blog-djangoproject/
├── blog/               # Blog app
├── myprojecgt/         # Main Django project folder
├── templates/          # HTML templates
├── static/             # Static files (CSS, JS, Images)
├── media/              # Uploaded images
├── manage.py
├── requirements.txt
├── Procfile
└── README.md
```

---

## 🚀 Deployment

### Hosted on [Render.com](https://render.com)

> 🔐 Make sure to set these environment variables in Render:
- `DJANGO_SECRET_KEY`
- `DJANGO_SETTINGS_MODULE = myproject.settings`

---

### 💻 Local Setup

1. **Clone repo**  
   ```bash
   git clone https://github.com/Kishore1245/blog-django.git
   cd blog-django
   ```

2. **Create virtual environment & install packages**  
   ```bash
   python -m env venv
   env\Scripts\activate   # Windows
   pip install -r requirements.txt
   ```

3. **Run migrations & start server**
   ```bash
   python manage.py migrate
   python manage.py runserver
   ```

---

## 📸 Screenshots

(Add your project screenshots here if needed)

---

## ✍️ Author

**Kishore**  
📧 shreekishorekishore.s@gmail.com  
🔗 [GitHub](https://github.com/Kishore1245)

---
