#database.py

#sqlalchemyを使用した場合
import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

import mysql.connector
from mysql.connector import Error

# .envファイルの読み込み
load_dotenv()

# 環境変数からデータベース接続情報を取得
DB_USERNAME = os.getenv("DB_USERNAME")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")
DB_ssl_ca = os.getenv("DB_ssl_ca")

# デバッグ用：環境変数の値を出力
print(f"DB_USERNAME: {DB_USERNAME}")
print(f"DB_PASSWORD: {DB_PASSWORD}")
print(f"DB_HOST: {DB_HOST}")
print(f"DB_PORT: {DB_PORT}")
print(f"DB_NAME: {DB_NAME}")
print(f"DB_ssl_ca: {DB_ssl_ca}")


# MySQLデータベースへの接続URL
# データベース接続URL（Azure 用）
# DATABASE_URLにSSLオプションを追加
DATABASE_URL = (
    f"mysql+pymysql://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    f"?ssl_ca={DB_ssl_ca}"
)

print("Database URL:", DATABASE_URL)

# SSL 設定を追加してエンジンを作成
engine = create_engine(
    DATABASE_URL,
    connect_args={
        "ssl": {
            "ca": DB_ssl_ca
        }
    }
)
#???
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# データベース接続のテスト
from sqlalchemy import text

try:
    with engine.connect() as conn:
        result = conn.execute(text("SELECT DATABASE()"))
        print("Connected to:", result.fetchone())
except Exception as e:
    print("Connection failed:", e)

# データベース接続の依存関係
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


#mysql.connector
# import os
# import mysql.connector
# from mysql.connector import Error
# from dotenv import load_dotenv

# # .envファイルの読み込み
# load_dotenv()

# # 環境変数からデータベース接続情報を取得
# config = {
#     'host': os.getenv('DB_HOST'),  # ホスト名
#     'user': os.getenv('DB_USERNAME'),  # ユーザー名
#     'password': os.getenv('DB_PASSWORD'),  # パスワード
#     'database': os.getenv('DB_NAME'),  # データベース名
#     'client_flags': [mysql.connector.ClientFlag.SSL],  # SSL接続を有効にするためのフラグ
#     'ssl_ca': os.getenv('DB_ssl_ca')  # SSL証明書ファイルのパス
# }

# # デバッグ用：環境変数の値を出力
# print("Database Config:")
# print(f"Host: {config['host']}")
# print(f"User: {config['user']}")
# print(f"Database: {config['database']}")
# print(f"SSL CA: {config['ssl_ca']}")

# # データベース接続のテスト
# try:
#     connection = mysql.connector.connect(**config)  # configを使用して接続
#     if connection.is_connected():
#         db_info = connection.get_server_info()
#         print("MySQLサーバーのバージョン: ", db_info)
#         cursor = connection.cursor()
#         cursor.execute("SELECT DATABASE();")
#         record = cursor.fetchone()
#         print("接続中のデータベース: ", record)
# except Error as e:
#     print("MySQL接続エラー: ", e)
# finally:
#     if 'connection' in locals() and connection.is_connected():
#         cursor.close()
#         connection.close()
#         print("MySQL接続は閉じられました")

# # データベース接続の依存関係
# def get_db():
#     try:
#         connection = mysql.connector.connect(**config)  # データベース接続
#         if connection.is_connected():
#             yield connection  # 接続を返す
#     finally:
#         if connection.is_connected():
#             connection.close()  # 接続を閉じる