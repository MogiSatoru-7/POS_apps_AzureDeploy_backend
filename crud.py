# crud.py
from sqlalchemy.orm import Session
from models import Product, PurchaseHistory, Transactions, TransactionDetails
from datetime import datetime

def get_product_by_code(db: Session, code: str):
    return db.query(Product).filter(Product.CODE == code).first()

#購入履歴：purchasehistoryテーブルにデータを追加（指定のER図にはない）
def add_purchase_history(db: Session, product_code: str, quantity: int, total_price: int):
    purchase = PurchaseHistory(
        product_code=product_code,
        quantity=quantity,
        total_price=total_price
    )
    db.add(purchase)
    db.commit()
    db.refresh(purchase)
    return purchase

# Transactions テーブルにデータを追加
def add_transaction(db: Session, total_amount: float, emp_code: str, store_code: str, pos_no: str):
    transaction = Transactions(
        DATETIME=datetime.now(),
        EMP_CD=emp_code,
        STORE_CD=store_code,
        POS_NO=pos_no,
        TOTAL_AMT=total_amount,
        TTL_AMT_EX_TAX=total_amount / 1.1  # 消費税を含まない金額（10%税として仮定）
    )
    db.add(transaction)
    db.commit()
    db.refresh(transaction)
    return transaction.TRD_ID  # 取引IDを返す

# TransactionDetails テーブルにデータを追加
def add_transaction_detail(db: Session, transaction_id: int, product: Product, quantity: int):
    detail = TransactionDetails(
        TRD_ID=transaction_id,
        PRD_ID=product.PRD_ID,
        PRD_CODE=product.CODE,
        PRD_NAME=product.NAME,
        PRD_PRICE=product.PRICE,
        TAX_CD='10',  # 仮の税コードを使用。適宜変更してください。
        #quantity=quantity #本来は量は必要だがER図で指定がないため一旦保留
    )
    db.add(detail)
    db.commit()