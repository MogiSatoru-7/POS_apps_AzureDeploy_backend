# create_tables.py
import os
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
from models import Base  # models.py の Base をインポート

# .envファイルの読み込み
load_dotenv()

# 環境変数からデータベース接続情報を取得
DB_USERNAME = os.getenv("DB_USERNAME")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")
DB_ssl_ca = os.getenv("DB_ssl_ca")

# データベース接続URL（Azure 用）
DATABASE_URL = (
    f"mysql+pymysql://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    f"?ssl_ca={DB_ssl_ca}&charset=utf8mb4"  # utf8mb4 文字セットを追加
)

# SSL 設定を追加してエンジンを作成
engine = create_engine(
    DATABASE_URL,
    connect_args={
        "ssl": {
            "ca": DB_ssl_ca
        }
    }
)

# データベースの再作成と文字セットの設定
with engine.connect() as connection:
    # データベースをドロップして再作成する（文字セットを含める）
    connection.execute(text(f"DROP DATABASE IF EXISTS {DB_NAME}"))
    connection.execute(text(f"CREATE DATABASE {DB_NAME} CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci"))
    print(f"Database {DB_NAME} created with utf8mb4 character set.")

# エンジンを新しいデータベースに再接続
engine = create_engine(
    DATABASE_URL,
    connect_args={
        "ssl": {
            "ca": DB_ssl_ca
        }
    }
)

# テーブルの再作成
Base.metadata.drop_all(bind=engine)
print(f"Database {DB_NAME} tables dropped.")
Base.metadata.create_all(bind=engine)
print("All tables created successfully.")

#sqlalchemyを使った方のやり方(直接SQL文)
# import os
# from sqlalchemy import create_engine, text
# from dotenv import load_dotenv

# # .envファイルの読み込み
# load_dotenv()

# # 環境変数からデータベース接続情報を取得
# DB_USERNAME = os.getenv("DB_USERNAME")
# DB_PASSWORD = os.getenv("DB_PASSWORD")
# DB_HOST = os.getenv("DB_HOST")
# DB_PORT = os.getenv("DB_PORT")
# DB_NAME = os.getenv("DB_NAME")
# DB_ssl_ca = os.getenv("DB_ssl_ca")

# # データベース接続URL（Azure 用）
# # DATABASE_URLにSSLオプションを追加
# DATABASE_URL = (
#     f"mysql+pymysql://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
#     f"?ssl_ca={DB_ssl_ca}"
# )

# # SSL 設定を追加してエンジンを作成
# engine = create_engine(
#     DATABASE_URL,
#     connect_args={
#         "ssl": {
#             "ca": DB_ssl_ca
#         }
#     }
# )

# # データベースの再作成
# try:
#     with engine.connect() as connection:
#         # データベースが存在する場合は削除
#         connection.execute(text(f"DROP DATABASE IF EXISTS {DB_NAME}"))
#         print(f"Database {DB_NAME} dropped.")

#         # データベースの作成
#         connection.execute(text(f"CREATE DATABASE {DB_NAME}"))
#         print(f"Database {DB_NAME} created.")
# except Exception as e:
#     print("Error creating database:", e)

# # 再作成したデータベースに接続
# engine = create_engine(f"{DATABASE_URL}{DB_NAME}")

# # テーブルの作成
# with engine.connect() as connection:
#     # Productsテーブルの作成
#     connection.execute(text("""
#         CREATE TABLE Products (
#             PRD_ID INT AUTO_INCREMENT PRIMARY KEY,
#             CODE CHAR(13) UNIQUE,
#             NAME VARCHAR(50),
#             PRICE INT
#         )
#     """))
#     print("Table Products created.")

#     # Taxテーブルの作成
#     connection.execute(text("""
#         CREATE TABLE Tax (
#             ID INT AUTO_INCREMENT PRIMARY KEY,
#             CODE CHAR(2) UNIQUE,
#             NAME VARCHAR(20),
#             PERCENT DECIMAL(5, 2)
#         )
#     """))
#     print("Table Tax created.")

#     # Transactionsテーブルの作成
#     connection.execute(text("""
#         CREATE TABLE Transactions (
#             TRD_ID INT AUTO_INCREMENT PRIMARY KEY,
#             DATETIME TIMESTAMP,
#             EMP_CD CHAR(10),
#             STORE_CD CHAR(5),
#             POS_NO CHAR(3),
#             TOTAL_AMT INT,
#             TTL_AMT_EX_TAX INT
#         )
#     """))
#     print("Table Transactions created.")

#     # TransactionDetailsテーブルの作成
#     connection.execute(text("""
#         CREATE TABLE TransactionDetails (
#             TRD_ID INT,
#             DTL_ID INT AUTO_INCREMENT PRIMARY KEY,
#             PRD_ID INT,
#             PRD_CODE CHAR(13),
#             PRD_NAME VARCHAR(50),
#             PRD_PRICE INT,
#             TAX_CD CHAR(2),
#             FOREIGN KEY (TRD_ID) REFERENCES Transactions(TRD_ID),
#             FOREIGN KEY (PRD_ID) REFERENCES Products(PRD_ID)
#         )
#     """))
#     print("Table TransactionDetails created.")

#     # PurchaseHistoryテーブルの作成
#     connection.execute(text("""
#         CREATE TABLE PurchaseHistory (
#             id INT AUTO_INCREMENT PRIMARY KEY,
#             product_code CHAR(13),
#             quantity INT,
#             total_price INT,
#             purchased_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
#             FOREIGN KEY (product_code) REFERENCES Products(CODE)
#         )
#     """))
#     print("Table PurchaseHistory created.")

# print("All tables created successfully.")





#mysqlconnector
# import os
# import mysql.connector
# from dotenv import load_dotenv
# from mysql.connector import errorcode

# # .envファイルをロード
# load_dotenv()

# # Azure Database for MySQL の接続情報
# config = {
#     'host': os.getenv('DB_HOST'),
#     'user': os.getenv('DB_USERNAME'),
#     'password': os.getenv('DB_PASSWORD'),
#     'database': os.getenv('DB_NAME'),
#     'client_flags': [mysql.connector.ClientFlag.SSL],
#     'ssl_ca': os.getenv('DB_ssl_ca')
# }

# try:
#     # データベースに接続
#     conn = mysql.connector.connect(**config)
#     print("Connection established")

#     # カーソルを作成
#     cursor = conn.cursor()

#     # Products テーブルの作成
#     cursor.execute("""
#         CREATE TABLE IF NOT EXISTS Products (
#             PRD_ID INT AUTO_INCREMENT PRIMARY KEY,
#             CODE CHAR(13) UNIQUE,
#             NAME VARCHAR(50),
#             PRICE INT
#         )
#     """)
#     print("Table Products created.")

#     # Tax テーブルの作成
#     cursor.execute("""
#         CREATE TABLE IF NOT EXISTS Tax (
#             ID INT AUTO_INCREMENT PRIMARY KEY,
#             CODE CHAR(2) UNIQUE,
#             NAME VARCHAR(20),
#             PERCENT DECIMAL(5, 2)
#         )
#     """)
#     print("Table Tax created.")

#     # Transactions テーブルの作成
#     cursor.execute("""
#         CREATE TABLE IF NOT EXISTS Transactions (
#             TRD_ID INT AUTO_INCREMENT PRIMARY KEY,
#             DATETIME TIMESTAMP,
#             EMP_CD CHAR(10),
#             STORE_CD CHAR(5),
#             POS_NO CHAR(3),
#             TOTAL_AMT INT,
#             TTL_AMT_EX_TAX INT
#         )
#     """)
#     print("Table Transactions created.")

#     # TransactionDetails テーブルの作成
#     cursor.execute("""
#         CREATE TABLE IF NOT EXISTS TransactionDetails (
#             TRD_ID INT,
#             DTL_ID INT AUTO_INCREMENT PRIMARY KEY,
#             PRD_ID INT,
#             PRD_CODE CHAR(13),
#             PRD_NAME VARCHAR(50),
#             PRD_PRICE INT,
#             TAX_CD CHAR(2),
#             FOREIGN KEY (TRD_ID) REFERENCES Transactions(TRD_ID),
#             FOREIGN KEY (PRD_ID) REFERENCES Products(PRD_ID)
#         )
#     """)
#     print("Table TransactionDetails created.")

#     # PurchaseHistory テーブルの作成
#     cursor.execute("""
#         CREATE TABLE IF NOT EXISTS PurchaseHistory (
#             id INT AUTO_INCREMENT PRIMARY KEY,
#             product_code CHAR(13),
#             quantity INT,
#             total_price INT,
#             purchased_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
#             FOREIGN KEY (product_code) REFERENCES Products(CODE)
#         )
#     """)
#     print("Table PurchaseHistory created.")

#     # 接続を閉じる
#     conn.close()
#     print("All tables created successfully.")
# except mysql.connector.Error as err:
#     if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
#         print("User name or password is incorrect")
#     elif err.errno == errorcode.ER_BAD_DB_ERROR:
#         print("Database does not exist")
#     else:
#         print("Error:", err)