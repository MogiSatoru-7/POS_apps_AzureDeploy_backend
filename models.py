# models.py
from sqlalchemy import Column, Integer, String, DECIMAL, DateTime, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from database import Base
from datetime import datetime

# Baseクラスを作成
Base = declarative_base()

# 商品情報テーブル
class Product(Base):
    __tablename__ = "Products"

    PRD_ID = Column(Integer, primary_key=True, index=True)
    CODE = Column(String(13), unique=True, index=True)
    NAME = Column(String(50))
    PRICE = Column(Integer)

# Taxテーブルのモデル
class Tax(Base):
    __tablename__ = "Tax"

    ID = Column(Integer, primary_key=True, index=True)
    CODE = Column(String(2), unique=True, index=True)
    NAME = Column(String(20))
    PERCENT = Column(DECIMAL(5, 2))

# 取引テーブル
class Transactions(Base):
    __tablename__ = "Transactions"

    TRD_ID = Column(Integer, primary_key=True, index=True)
    DATETIME = Column(DateTime(timezone=True), server_default=func.now())
    EMP_CD = Column(String(10))
    STORE_CD = Column(String(5))
    POS_NO = Column(String(3))
    TOTAL_AMT = Column(Integer)
    TTL_AMT_EX_TAX = Column(Integer)

# 取引明細テーブル
class TransactionDetails(Base):
    __tablename__ = "TransactionDetails"

    DTL_ID = Column(Integer, primary_key=True, index=True)
    TRD_ID = Column(Integer, ForeignKey("Transactions.TRD_ID"))
    PRD_ID = Column(Integer, ForeignKey("Products.PRD_ID"))
    PRD_CODE = Column(String(13))
    PRD_NAME = Column(String(50))
    PRD_PRICE = Column(Integer)
    TAX_CD = Column(String(10))
    #quantity = Column(Integer)   # 購入数を表すカラムはER図にないため一旦保留

# 購入履歴テーブル
class PurchaseHistory(Base):
    __tablename__ = "PurchaseHistory"

    id = Column(Integer, primary_key=True, index=True)
    product_code = Column(String(13), ForeignKey("Products.CODE"))
    quantity = Column(Integer)
    total_price = Column(Integer)
    purchased_at = Column(DateTime(timezone=True), server_default=func.now())
