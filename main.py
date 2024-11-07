#main.py
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models import Product, PurchaseHistory
from crud import get_product_by_code, add_purchase_history, add_transaction, add_transaction_detail
from pydantic import BaseModel
import uvicorn
from schemas import PurchaseRequest
from datetime import datetime


app = FastAPI()

# CORS設定
from fastapi.middleware.cors import CORSMiddleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 商品コードで商品情報を取得するエンドポイント
@app.get("/products/{product_code}")
async def fetch_product_by_code(product_code: str, db: Session = Depends(get_db)):
    product = get_product_by_code(db, product_code)
    if not product:
        #raise HTTPException(status_code=404, detail="商品が見つかりません")
        # 修正点: NULL情報をJSONで返す
        return {"NAME": None, "PRICE": None, "PRD_ID": None, "CODE": None}
    return {
        "NAME": product.NAME,
        "PRICE": product.PRICE,
        "PRD_ID": product.PRD_ID,
        "CODE": product.CODE
    }

@app.get("/products")
def get_products(db: Session = Depends(get_db)):
    products = db.query(Product).all()
    return products

# 購入情報リクエスト用の Pydantic モデル
class PurchaseRequest(BaseModel):
    product_code: str
    quantity: int

# 購入情報を保存するエンドポイント
@app.post("/purchase")
async def purchase_item(request: PurchaseRequest, db: Session = Depends(get_db)):
    try:
        # 商品を検索
        product = db.query(Product).filter(Product.CODE == request.product_code).first()
        if not product:
            raise HTTPException(status_code=404, detail="商品が見つかりません")

        # 合計金額を計算
        total_price = product.PRICE * request.quantity

        # `Transactions` テーブルに追加
        # 修正点: レジ担当者コード、店舗コード、POS機IDの設定を追加
        emp_code = "9999999999"  # デフォルトのレジ担当者コード
        store_code = "30"  # 固定の店舗コード
        pos_no = "90"  # 固定のPOS機ID
        transaction_id = add_transaction(db, total_price, emp_code, store_code, pos_no)

        # `TransactionDetails` テーブルに追加
        add_transaction_detail(db, transaction_id, product, request.quantity)

        # `add_purchase_history` を使って購入履歴を保存
        purchase = add_purchase_history(db, request.product_code, request.quantity, total_price)

        return {
            "transaction_id": transaction_id,
            "product_code": purchase.product_code,
            "quantity": purchase.quantity,
            "total_price": purchase.total_price,
            "purchased_at": purchase.purchased_at
        }

    except HTTPException as http_err:
        # HTTPエラーをログに記録
        print(f"HTTPエラー: {http_err.detail}")
        raise http_err

    except Exception as err:
        # その他のエラーをログに記録
        print(f"予期しないエラーが発生しました: {err}")
        raise HTTPException(status_code=500, detail="サーバー内部でエラーが発生しました。詳細はログを確認してください。")

@app.get("/")
def read_root():
    return {"message": "Hello, World!"}

@app.get("/items/") #動作テスト用（削除可能）
async def get_items():
    return { "items": ["item1", "item2"]}

# 購入履歴を取得するエンドポイント
@app.get("/purchase-history")
async def get_purchase_history(db: Session = Depends(get_db)):
    purchase_history = db.query(PurchaseHistory).all()
    return purchase_history



if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)



#DeployTest
# from fastapi import FastAPI
# app = FastAPI()
# @app.get("/")
# def read_root():
#     return {"Hello": "World"}