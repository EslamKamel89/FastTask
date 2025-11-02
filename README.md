
# 🚀 FastTask — Full Stack FastAPI Starter Kit

![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white)
![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-D71F00?style=for-the-badge&logo=python&logoColor=white)
![Alembic](https://img.shields.io/badge/Alembic-444444?style=for-the-badge&logo=alembic&logoColor=white)
![MySQL](https://img.shields.io/badge/MySQL-4479A1?style=for-the-badge&logo=mysql&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-4169E1?style=for-the-badge&logo=postgresql&logoColor=white)
![SQLite](https://img.shields.io/badge/SQLite-07405E?style=for-the-badge&logo=sqlite&logoColor=white)
![Jinja2](https://img.shields.io/badge/Jinja2-B41717?style=for-the-badge&logo=jinja&logoColor=white)
![Bootstrap](https://img.shields.io/badge/Bootstrap-7952B3?style=for-the-badge&logo=bootstrap&logoColor=white)
![Pytest](https://img.shields.io/badge/Pytest-0A9EDC?style=for-the-badge&logo=pytest&logoColor=white)
![Uvicorn](https://img.shields.io/badge/Uvicorn-000000?style=for-the-badge&logo=fastapi&logoColor=white)

> 🧑‍💻 Built by a Laravel developer exploring the Python backend world.  
> After **more than 45 days**, it’s finally here — a complete **FastAPI full-stack starter kit** with everything configured for real-world use.

---

## 🌟 Overview

**FastTask** is a production-ready **FastAPI full-stack application** designed as a **starter kit or boilerplate** for future projects.

It includes pre-configured authentication, admin routes, database setup, templating, and testing — so you can **start building immediately** instead of wasting time on setup.

---

## ⚙️ Features

✅ JWT Authentication system (Login, Register, Token Refresh)  
✅ Admin-only routes  
✅ CRUD for Todos (API + HTML templates)  
✅ User management (update password & phone number)  
✅ Multi-database support: **MySQL**, **PostgreSQL**, **SQLite**  
✅ Static files support (CSS, JS, Bootstrap)  
✅ 100% tested with **Pytest**  
✅ Pre-configured **Alembic** migrations  
✅ Clean modular structure — ready for production

---

## 🧩 Tech Stack

| Layer | Tool | Description |
|-------|------|--------------|
| **Backend Framework** | [FastAPI](https://fastapi.tiangolo.com/) | Modern, high-performance Python web framework |
| **ORM** | [SQLAlchemy](https://www.sqlalchemy.org/) | Database ORM for models and queries |
| **Migrations** | [Alembic](https://alembic.sqlalchemy.org/) | Database version control |
| **Auth** | [python-jose](https://github.com/mpdavis/python-jose) + [OAuth2PasswordBearer] | Secure JWT authentication |
| **Hashing** | [Passlib (bcrypt)](https://passlib.readthedocs.io/) | Password encryption |
| **Templating** | [Jinja2](https://jinja.palletsprojects.com/) | Frontend rendering |
| **Testing** | [Pytest](https://docs.pytest.org/) | Unit & integration testing |
| **Databases** | SQLite, MySQL, PostgreSQL | Plug-and-play DB support |
| **Frontend** | [Bootstrap 5](https://getbootstrap.com/) | Responsive UI framework |
| **Web Server** | [Uvicorn](https://www.uvicorn.org/) | ASGI server for FastAPI |

---

## 🏗️ Project Structure

```

FastTask/
│
├── main.py                 # FastAPI entry point
├── database.py             # SQLAlchemy database config
├── models.py               # ORM models and Pydantic schemas
├── security.py             # JWT auth, password hashing
│
├── routers/                # Modular API routes
│   ├── auth.py             # Authentication routes
│   ├── todos.py            # CRUD for todos
│   ├── users.py            # User management
│   └── admin.py            # Admin-only endpoints
│
├── template/               # Jinja2 HTML templates
│   ├── layout.html
│   ├── todo.html
│   ├── login.html
│   ├── register.html
│   └── ...
│
├── static/                 # JS, CSS, images, etc.
├── test/                   # Pytest test suite
│
├── alembic/                # DB migrations
├── alembic.ini
├── requirements.txt
└── README.md

````

---

## ⚡ Getting Started

### 1. Clone the Repository

```bash
git clone https://github.com/EslamKamel89/FastTask.git
cd FastTask
````

### 2. Create a Virtual Environment

```bash
python -m venv venv
source venv/bin/activate   # macOS/Linux
venv\Scripts\activate      # Windows
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Your Database

Edit `database.py` and choose your preferred database:

```python
SELECTED_DB = MYSQL  # or POSTGRESQL or SQLITE
```

Then apply migrations:

```bash
alembic upgrade head
```

### 5. Run the Server

```bash
uvicorn main:app --reload
```

Visit 👉 **[http://127.0.0.1:8000](http://127.0.0.1:8000)**

---

## 🧠 API Endpoints

| Method   | Endpoint       | Description           |
| -------- | -------------- | --------------------- |
| `POST`   | `/auth/`       | Register a new user   |
| `POST`   | `/auth/token`  | Login & get JWT token |
| `GET`    | `/todos/`      | List all user todos   |
| `POST`   | `/todos/`      | Create a new todo     |
| `PUT`    | `/todos/{id}`  | Update a todo         |
| `DELETE` | `/todos/{id}`  | Delete a todo         |
| `GET`    | `/admin/todos` | Admin-only route      |
| `GET`    | `/users/`      | Get current user info |

---

## 🧪 Running Tests

All tests are built using **Pytest**.

```bash
pytest
```

You’ll find test coverage for:

* Auth
* Todos
* Users
* Admin routes
* Basic health checks

---

## 🌍 Deployment

To deploy with **Uvicorn + Gunicorn** (recommended):

```bash
gunicorn -k uvicorn.workers.UvicornWorker main:app
```

---

## 📅 Timeline

🗓️ **Started:** September 15, 2025
✅ **Finished:** November 2, 2025
⏳ **Duration:** More than 45 days
💾 **Commits:** 77 total

---

## 🧑‍💻 Author

**Eslam Kamel**
Full Stack Developer | Laravel → Python Transitioner
🔗 [LinkedIn](https://www.linkedin.com/in/eslamkamel89)
⭐ [GitHub Repo](https://github.com/EslamKamel89/FastTask)

---

## 💬 Final Thoughts

FastTask is built for developers who love structure and hate boilerplate 😅
If you’re a **Laravel dev exploring FastAPI**, this template will feel like home — just with more indentation and fewer semicolons.

**Clone it, extend it, and build something amazing 🚀**


