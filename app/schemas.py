from pydantic import BaseModel, ConfigDict
from datetime import date
from typing import Optional


# Book schemas
class BookCreate(BaseModel):
    title: str
    author: str
    isbn: str
    category: Optional[str] = None
    total_copies: int


class BookResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    book_id: int
    title: str
    author: str
    isbn: str
    category: Optional[str]
    total_copies: int
    available_copies: int


# Member schemas
class MemberCreate(BaseModel):
    name: str
    email: str
    phone: Optional[str] = None


class MemberResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    member_id: int
    name: str
    email: str
    phone: Optional[str]
    joined_date: Optional[date]


# Borrow request schema
class BorrowRequest(BaseModel):
    book_id: int
    member_id: int


# Loan response schema
class LoanResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    loan_id: int
    book_id: int
    member_id: int
    borrow_date: date
    due_date: date
    return_date: Optional[date]