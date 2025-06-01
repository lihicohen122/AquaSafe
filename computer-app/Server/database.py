from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# הגדרת הנתיב לקובץ SQLite (אפשר לשנות את שם הקובץ אם תרצו)
SQLALCHEMY_DATABASE_URL = "sqlite:///./divers.db"

# יוצרים את engine
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

# יצירת session
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# בסיס משותף לכל המודלים
Base = declarative_base()
