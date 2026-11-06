# Library Management REST API

## Project Description
A RESTful Library Management API developed using FastAPI and PostgreSQL. It manages books, members, and loan transactions, and provides reports to track library activities.

## Technologies Used
- Python
- FastAPI
- PostgreSQL
- SQLAlchemy
- Psycopg 3
- Pydantic
- Uvicorn

## Features

### Book Management
- Create books
- View all books
- View a book by ID
- Update book details
- Delete books

### Member Management
- Register members
- View all members
- View a member by ID
- Update member details
- Delete members

### Loan Management
- Borrow books
- Return books
- Track book availability
- Manage loan transactions

### Reports
- Most borrowed books
- Most active members
- Currently borrowed books
- Overdue loans
- Loan statistics

## Project Structure

```text
library-management-api P2/
│
├── app/
│   ├── __init__.py
│   ├── database.py
│   ├── models.py
│   ├── schemas.py
│   └── main.py
│
├── schema.sql
├── seed.sql
├── requirements.txt
└── README.md
```

## Setup Instructions

### 1. Clone the Repository

```bash
git clone <your-repository-url>
cd library-management-api
```

### 2. Create a Virtual Environment

```bash
python -m venv venv
```

### 3. Activate the Virtual Environment

Windows:

```bash
.\venv\Scripts\Activate.ps1
```

### 4. Install Dependencies

```bash
pip install -r requirements.txt
```

### 5. Create the Database

Create a PostgreSQL database named:

```text
library_management_db
```

### 6. Execute SQL Files

Run `schema.sql` first, followed by `seed.sql`, using PostgreSQL Query Tool.

### 7. Configure Database Connection

Update the PostgreSQL connection details in `app/database.py` with your local database credentials.

### 8. Run the Application

```bash
uvicorn app.main:app --reload
```

## API Documentation

Once the application is running, open:

- Swagger UI: http://127.0.0.1:8000/docs
- ReDoc: http://127.0.0.1:8000/redoc

## Database

The database contains three tables:

- `books`
- `members`
- `loans`

The project includes primary keys, foreign keys, constraints, and indexes.

Seed data includes 20 books, 20 members, and 20 loans.