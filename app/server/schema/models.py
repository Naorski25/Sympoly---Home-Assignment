from beanie import Document
from pydantic import BaseModel
from typing import List
from datetime import datetime


class Details(BaseModel):
    created_at: datetime
    status: str
    
    @classmethod
    def parse_details(cls, details_dict: dict) -> 'Details':
        created_at = datetime.strptime(details_dict["CreatedAt"], "%Y%m%d%H%M%S")
        status = details_dict.get("Status")
        status_map = {
            '0': "Draft",
            '1': "Submitted",
            '2': "Approved",
            '3': "Rejected"
        }
        status = status_map.get(status)
        return cls(created_at=created_at, status=status)

class Person(BaseModel):
    full_name: str
    email: str
    @classmethod
    def parse_person(cls, person_dict: dict) -> 'Person':
        return cls(full_name=person_dict["FullName"], email=person_dict["Email"])

class TransactionData(BaseModel):
    date: datetime
    type: str
    amount: float
    currency: str
    
    @classmethod
    def parse_transaction_string(cls, transaction_string: str) -> 'TransactionData':
        date_str = transaction_string[:14]
        date = datetime.strptime(date_str, "%Y%m%d%H%M%S")
        transaction_type = transaction_string[14]
        amount_str = transaction_string[15:-3].replace(',', '.')
        amount = float(amount_str)
        currency = transaction_string[-3:]
        return cls(date=date, type=transaction_type, amount=amount, currency=currency)

class Transaction(BaseModel):
    data: TransactionData
    reference: str
    details: str
    @classmethod
    def parse_transaction(cls, transaction_dict: dict) -> 'Transaction':
        data = TransactionData.parse_transaction_string(transaction_dict["Data"])
        return cls(data=data, reference=transaction_dict["Reference"], details=transaction_dict["Details"])

class InvoiceReport(Document):
    id: str
    details: Details
    reporter: Person
    approvers: List[Person]
    transactions: List[Transaction]

    class settings:
        name = "reports"

