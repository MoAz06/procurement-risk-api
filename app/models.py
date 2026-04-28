from sqlalchemy import Column, Float, Integer, String
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class Invoice(Base):
    __tablename__ = "invoices"

    id = Column(Integer, primary_key=True, index=True)
    invoice_id = Column(Integer, unique=True, index=True)
    supplier = Column(String)
    amount = Column(Float)
    status = Column(String)
    invoice_date = Column(String)