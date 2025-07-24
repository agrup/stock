from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.app.config import get_database_url

DATABASE_URL = get_database_url()

# Engine de SQLAlchemy 2.0
engine = create_engine(
    DATABASE_URL, echo=True, future=True  # Mostrar queries en consola (útil para debug)
)

# SessionLocal es un factory de sesiones para inyección vía Depends
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)


# Para FastAPI
def get_session():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
