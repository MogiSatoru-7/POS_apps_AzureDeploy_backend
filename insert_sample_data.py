import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Product, Tax, Transactions, TransactionDetails, PurchaseHistory
from dotenv import load_dotenv

# .envファイルの読み込み
load_dotenv()

# 環境変数からデータベース接続情報を取得
DB_USERNAME = os.getenv("DB_USERNAME")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")
DB_ssl_ca = os.getenv("DB_ssl_ca")

# データベース接続URL
DATABASE_URL = (
    f"mysql+pymysql://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    f"?ssl_ca={DB_ssl_ca}&charset=utf8mb4"  # utf8mb4 文字セットを追加
)

# SQLAlchemyエンジンを作成
engine = create_engine(
    DATABASE_URL,
    connect_args={
        "ssl": {
            "ca": DB_ssl_ca
        }
    }
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
db = SessionLocal()

# サンプルデータの挿入
try:
    # Products テーブルにサンプルデータを挿入
    product1 = Product(CODE="0011234567890", NAME="Black Label 350ml", PRICE=210)
    product2 = Product(CODE="0021234567890", NAME="Yebisu 350ml", PRICE=240)
    product3 = Product(CODE="1011234567890", NAME="Black Label 6-pack", PRICE=1200)
    product4 = Product(CODE="1021234567890", NAME="Yebisu 6-pack", PRICE=1400)
    product5 = Product(CODE="2011234567890", NAME="Black Label Case", PRICE=5000)
    product6 = Product(CODE="2021234567890", NAME="Yebisu Case", PRICE=5500)
    db.add_all([product1, product2, product3, product4, product5, product6])

    # Tax テーブルにサンプルデータを挿入
    tax1 = Tax(CODE="01", NAME="General Tax", PERCENT=10.0)
    tax2 = Tax(CODE="02", NAME="Reduced Tax", PERCENT=8.0)
    db.add_all([tax1, tax2])

    # データベースにコミットして保存
    db.commit()
    print("サンプルデータが挿入されました。")

except Exception as e:
    print("エラーが発生しました:", e)
    db.rollback()

finally:
    db.close()

