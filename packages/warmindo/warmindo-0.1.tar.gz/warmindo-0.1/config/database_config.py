from flask_sqlalchemy import SQLAlchemy

DATABASE_URI = 'sqlite:///blog.db'  # Ganti dengan URI basis data Anda

db = SQLAlchemy()