from sqlalchemy import Column, DateTime, Float, Integer, String, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_URL = "sqlite:///./database.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


class Alert(Base):
  __tablename__ = "alerts"

  id = Column(Integer, primary_key=True, index=True)
  timestamp = Column(String)
  source = Column(String)
  message = Column(String)
  status = Column(String, default="Unprocessed")  # Unprocessed, Processed


class Incident(Base):
  __tablename__ = "incidents"

  id = Column(Integer, primary_key=True, index=True)
  cluster_id = Column(Integer)
  root_cause = Column(String)
  risk_level = Column(String)  # Low, High
  remediation_status = Column(
      String, default="Pending"
  )  # Pending, Resolved, Escalated


def init_db():
  Base.metadata.create_all(bind=engine)


if __name__ == "__main__":
  init_db()
  print("Database initialized successfully!")