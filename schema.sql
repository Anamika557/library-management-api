CREATE TABLE IF NOT EXISTS books (
    book_id SERIAL PRIMARY KEY,
    title VARCHAR(200) NOT NULL,
    author VARCHAR(150) NOT NULL,
    isbn VARCHAR(20) UNIQUE NOT NULL,
    category VARCHAR(100),
    total_copies INT NOT NULL CHECK (total_copies >= 0),
    available_copies INT NOT NULL CHECK (
        available_copies >= 0
        AND available_copies <= total_copies
    )
);


CREATE TABLE IF NOT EXISTS members (
    member_id SERIAL PRIMARY KEY,
    name VARCHAR(150) NOT NULL,
    email VARCHAR(150) UNIQUE NOT NULL,
    phone VARCHAR(20),
    joined_date DATE DEFAULT CURRENT_DATE
);


CREATE TABLE IF NOT EXISTS loans (
    loan_id SERIAL PRIMARY KEY,
    book_id INT NOT NULL REFERENCES books(book_id),
    member_id INT NOT NULL REFERENCES members(member_id),
    borrow_date DATE NOT NULL DEFAULT CURRENT_DATE,
    due_date DATE NOT NULL,
    return_date DATE,
    CHECK (due_date >= borrow_date),
    CHECK (return_date IS NULL OR return_date >= borrow_date)
);


-- Indexes for faster searches
CREATE INDEX IF NOT EXISTS idx_books_title
ON books(title);

CREATE INDEX IF NOT EXISTS idx_loans_member
ON loans(member_id);

CREATE INDEX IF NOT EXISTS idx_loans_book
ON loans(book_id);