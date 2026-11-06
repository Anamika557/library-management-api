from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import text
from datetime import date, timedelta

from app.database import engine, get_db
from app.models import Book, Member, Loan
from app.schemas import (
    BookCreate,
    BookResponse,
    MemberCreate,
    MemberResponse,
    BorrowRequest,
    LoanResponse
)

app = FastAPI(
    title="Library Management API",
    description="REST API for managing books, members and loans",
    version="1.0.0"
)


@app.get("/")
def home():
    return {"message": "Library Management API is running!"}


# ==================== BOOKS CRUD ====================

@app.post("/books", response_model=BookResponse, status_code=201)
def create_book(book: BookCreate, db: Session = Depends(get_db)):
    if db.query(Book).filter(Book.isbn == book.isbn).first():
        raise HTTPException(status_code=400, detail="ISBN already exists")

    new_book = Book(
        title=book.title,
        author=book.author,
        isbn=book.isbn,
        category=book.category,
        total_copies=book.total_copies,
        available_copies=book.total_copies
    )

    db.add(new_book)
    db.commit()
    db.refresh(new_book)
    return new_book


@app.get("/books", response_model=list[BookResponse])
def get_books(db: Session = Depends(get_db)):
    return db.query(Book).all()


@app.get("/books/{book_id}", response_model=BookResponse)
def get_book(book_id: int, db: Session = Depends(get_db)):
    book = db.query(Book).filter(Book.book_id == book_id).first()

    if not book:
        raise HTTPException(status_code=404, detail="Book not found")

    return book


@app.put("/books/{book_id}", response_model=BookResponse)
def update_book(book_id: int, book_data: BookCreate, db: Session = Depends(get_db)):
    book = db.query(Book).filter(Book.book_id == book_id).first()

    if not book:
        raise HTTPException(status_code=404, detail="Book not found")

    if book_data.isbn != book.isbn:
        existing = db.query(Book).filter(Book.isbn == book_data.isbn).first()
        if existing:
            raise HTTPException(status_code=400, detail="ISBN already exists")

    borrowed_copies = book.total_copies - book.available_copies

    if book_data.total_copies < borrowed_copies:
        raise HTTPException(
            status_code=400,
            detail="Total copies cannot be less than borrowed copies"
        )

    book.title = book_data.title
    book.author = book_data.author
    book.isbn = book_data.isbn
    book.category = book_data.category
    book.total_copies = book_data.total_copies
    book.available_copies = book_data.total_copies - borrowed_copies

    db.commit()
    db.refresh(book)
    return book


@app.delete("/books/{book_id}")
def delete_book(book_id: int, db: Session = Depends(get_db)):
    book = db.query(Book).filter(Book.book_id == book_id).first()

    if not book:
        raise HTTPException(status_code=404, detail="Book not found")

    if book.loans:
        raise HTTPException(
            status_code=400,
            detail="Cannot delete a book with loan records"
        )

    db.delete(book)
    db.commit()
    return {"message": "Book deleted successfully"}


# ==================== MEMBERS CRUD ====================

@app.post("/members", response_model=MemberResponse, status_code=201)
def create_member(member: MemberCreate, db: Session = Depends(get_db)):
    if db.query(Member).filter(Member.email == member.email).first():
        raise HTTPException(status_code=400, detail="Email already exists")

    new_member = Member(
        name=member.name,
        email=member.email,
        phone=member.phone
    )

    db.add(new_member)
    db.commit()
    db.refresh(new_member)
    return new_member


@app.get("/members", response_model=list[MemberResponse])
def get_members(db: Session = Depends(get_db)):
    return db.query(Member).all()


@app.get("/members/{member_id}", response_model=MemberResponse)
def get_member(member_id: int, db: Session = Depends(get_db)):
    member = db.query(Member).filter(Member.member_id == member_id).first()

    if not member:
        raise HTTPException(status_code=404, detail="Member not found")

    return member


@app.put("/members/{member_id}", response_model=MemberResponse)
def update_member(member_id: int, member_data: MemberCreate, db: Session = Depends(get_db)):
    member = db.query(Member).filter(Member.member_id == member_id).first()

    if not member:
        raise HTTPException(status_code=404, detail="Member not found")

    if member_data.email != member.email:
        existing = db.query(Member).filter(Member.email == member_data.email).first()
        if existing:
            raise HTTPException(status_code=400, detail="Email already exists")

    member.name = member_data.name
    member.email = member_data.email
    member.phone = member_data.phone

    db.commit()
    db.refresh(member)
    return member


@app.delete("/members/{member_id}")
def delete_member(member_id: int, db: Session = Depends(get_db)):
    member = db.query(Member).filter(Member.member_id == member_id).first()

    if not member:
        raise HTTPException(status_code=404, detail="Member not found")

    if member.loans:
        raise HTTPException(
            status_code=400,
            detail="Cannot delete a member with loan records"
        )

    db.delete(member)
    db.commit()
    return {"message": "Member deleted successfully"}


# ==================== BORROW BOOK ====================

@app.post("/loans/borrow", response_model=LoanResponse, status_code=201)
def borrow_book(request: BorrowRequest, db: Session = Depends(get_db)):

    try:
        book = db.query(Book).filter(
            Book.book_id == request.book_id
        ).with_for_update().first()

        if not book:
            raise HTTPException(status_code=404, detail="Book not found")

        member = db.query(Member).filter(
            Member.member_id == request.member_id
        ).first()

        if not member:
            raise HTTPException(status_code=404, detail="Member not found")

        if book.available_copies <= 0:
            raise HTTPException(
                status_code=400,
                detail="No copies available"
            )

        loan = Loan(
            book_id=book.book_id,
            member_id=member.member_id,
            borrow_date=date.today(),
            due_date=date.today() + timedelta(days=14),
            return_date=None
        )

        book.available_copies -= 1

        db.add(loan)
        db.commit()
        db.refresh(loan)

        return loan

    except Exception:
        db.rollback()
        raise


# ==================== RETURN BOOK ====================

@app.post("/loans/return/{loan_id}")
def return_book(loan_id: int, db: Session = Depends(get_db)):

    try:
        loan = db.query(Loan).filter(
            Loan.loan_id == loan_id
        ).with_for_update().first()

        if not loan:
            raise HTTPException(status_code=404, detail="Loan not found")

        if loan.return_date is not None:
            raise HTTPException(
                status_code=400,
                detail="Book has already been returned"
            )

        book = db.query(Book).filter(
            Book.book_id == loan.book_id
        ).with_for_update().first()

        if not book:
            raise HTTPException(status_code=404, detail="Book not found")

        loan.return_date = date.today()
        book.available_copies += 1

        db.commit()

        return {
            "message": "Book returned successfully",
            "loan_id": loan.loan_id,
            "book_id": book.book_id,
            "available_copies": book.available_copies
        }

    except Exception:
        db.rollback()
        raise
# ==================== SQL REPORT APIs ====================

# 1. Most borrowed books
@app.get("/reports/most-borrowed-books")
def most_borrowed_books(db: Session = Depends(get_db)):

    result = db.execute(text("""
        SELECT b.book_id, b.title, b.author,
               COUNT(l.loan_id) AS borrow_count
        FROM books b
        JOIN loans l ON b.book_id = l.book_id
        GROUP BY b.book_id, b.title, b.author
        ORDER BY borrow_count DESC
    """))

    return [dict(row._mapping) for row in result]


# 2. Most active members
@app.get("/reports/most-active-members")
def most_active_members(db: Session = Depends(get_db)):

    result = db.execute(text("""
        SELECT m.member_id, m.name, m.email,
               COUNT(l.loan_id) AS total_borrowed
        FROM members m
        JOIN loans l ON m.member_id = l.member_id
        GROUP BY m.member_id, m.name, m.email
        ORDER BY total_borrowed DESC
    """))

    return [dict(row._mapping) for row in result]


# 3. Currently borrowed books
@app.get("/reports/currently-borrowed-books")
def currently_borrowed_books(db: Session = Depends(get_db)):

    result = db.execute(text("""
        SELECT l.loan_id, b.title, m.name AS member_name,
               l.borrow_date, l.due_date
        FROM loans l
        JOIN books b ON l.book_id = b.book_id
        JOIN members m ON l.member_id = m.member_id
        WHERE l.return_date IS NULL
        ORDER BY l.due_date
    """))

    return [dict(row._mapping) for row in result]


# 4. Overdue loans
@app.get("/reports/overdue-loans")
def overdue_loans(db: Session = Depends(get_db)):

    result = db.execute(text("""
        SELECT l.loan_id, b.title, m.name AS member_name,
               l.borrow_date, l.due_date
        FROM loans l
        JOIN books b ON l.book_id = b.book_id
        JOIN members m ON l.member_id = m.member_id
        WHERE l.return_date IS NULL
          AND l.due_date < CURRENT_DATE
        ORDER BY l.due_date
    """))

    return [dict(row._mapping) for row in result]


# 5. Loan statistics
@app.get("/reports/loan-statistics")
def loan_statistics(db: Session = Depends(get_db)):

    result = db.execute(text("""
        SELECT
            COUNT(*) AS total_loans,
            COUNT(*) FILTER (
                WHERE return_date IS NULL
            ) AS active_loans,
            COUNT(*) FILTER (
                WHERE return_date IS NOT NULL
            ) AS returned_loans,
            COUNT(*) FILTER (
                WHERE return_date IS NULL
                  AND due_date < CURRENT_DATE
            ) AS overdue_loans
        FROM loans
    """))

    return dict(result.fetchone()._mapping)