from sqlalchemy import Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import relationship

from app.database import Base


class Book(Base):
    __tablename__ = "books"

    book_id = Column(Integer, primary_key=True)
    title = Column(String(200), nullable=False)
    author = Column(String(150), nullable=False)
    isbn = Column(String(20), unique=True, nullable=False)
    category = Column(String(100))
    total_copies = Column(Integer, nullable=False)
    available_copies = Column(Integer, nullable=False)

    loans = relationship("Loan", back_populates="book")


class Member(Base):
    __tablename__ = "members"

    member_id = Column(Integer, primary_key=True)
    name = Column(String(150), nullable=False)
    email = Column(String(150), unique=True, nullable=False)
    phone = Column(String(20))
    joined_date = Column(Date)

    loans = relationship("Loan", back_populates="member")


class Loan(Base):
    __tablename__ = "loans"

    loan_id = Column(Integer, primary_key=True)
    book_id = Column(Integer, ForeignKey("books.book_id"), nullable=False)
    member_id = Column(Integer, ForeignKey("members.member_id"), nullable=False)
    borrow_date = Column(Date, nullable=False)
    due_date = Column(Date, nullable=False)
    return_date = Column(Date)

    book = relationship("Book", back_populates="loans")
    member = relationship("Member", back_populates="loans")