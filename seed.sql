-- BOOKS: 20 records

INSERT INTO books
(title, author, isbn, category, total_copies, available_copies)
VALUES
('Python Basics', 'John Smith', 'ISBN001', 'Programming', 5, 5),
('Learning SQL', 'Mark Lee', 'ISBN002', 'Database', 4, 3),
('Clean Code', 'Robert Martin', 'ISBN003', 'Programming', 6, 5),
('The Alchemist', 'Paulo Coelho', 'ISBN004', 'Fiction', 3, 3),
('Data Structures', 'Narasimha Karumanchi', 'ISBN005', 'Programming', 5, 4),
('Database Systems', 'Raghu Ramakrishnan', 'ISBN006', 'Database', 4, 4),
('Atomic Habits', 'James Clear', 'ISBN007', 'Self Help', 5, 5),
('Deep Work', 'Cal Newport', 'ISBN008', 'Productivity', 3, 3),
('Rich Dad Poor Dad', 'Robert Kiyosaki', 'ISBN009', 'Finance', 4, 4),
('The Psychology of Money', 'Morgan Housel', 'ISBN010', 'Finance', 5, 4),
('Java Programming', 'Herbert Schildt', 'ISBN011', 'Programming', 4, 4),
('Effective Python', 'Brett Slatkin', 'ISBN012', 'Programming', 3, 2),
('Computer Networks', 'Andrew Tanenbaum', 'ISBN013', 'Networking', 5, 5),
('Operating Systems', 'Abraham Silberschatz', 'ISBN014', 'Computer Science', 4, 3),
('The Hobbit', 'J.R.R. Tolkien', 'ISBN015', 'Fantasy', 3, 3),
('Harry Potter', 'J.K. Rowling', 'ISBN016', 'Fantasy', 6, 5),
('Think and Grow Rich', 'Napoleon Hill', 'ISBN017', 'Self Help', 4, 4),
('Introduction to Algorithms', 'Thomas Cormen', 'ISBN018', 'Programming', 5, 4),
('Wings of Fire', 'A.P.J. Abdul Kalam', 'ISBN019', 'Biography', 4, 4),
('Artificial Intelligence', 'Stuart Russell', 'ISBN020', 'AI', 3, 3);


-- MEMBERS: 20 records

INSERT INTO members (name, email, phone)
VALUES
('Anu', 'anu@example.com', '9876500001'),
('Rahul', 'rahul@example.com', '9876500002'),
('Maya', 'maya@example.com', '9876500003'),
('Arjun', 'arjun@example.com', '9876500004'),
('Meera', 'meera@example.com', '9876500005'),
('Akhil', 'akhil@example.com', '9876500006'),
('Diya', 'diya@example.com', '9876500007'),
('Nikhil', 'nikhil@example.com', '9876500008'),
('Amal', 'amal@example.com', '9876500009'),
('Sneha', 'sneha@example.com', '9876500010'),
('Vishnu', 'vishnu@example.com', '9876500011'),
('Kavya', 'kavya@example.com', '9876500012'),
('Adithya', 'adithya@example.com', '9876500013'),
('Neha', 'neha@example.com', '9876500014'),
('Riya', 'riya@example.com', '9876500015'),
('Manu', 'manu@example.com', '9876500016'),
('Asha', 'asha@example.com', '9876500017'),
('Kiran', 'kiran@example.com', '9876500018'),
('Devika', 'devika@example.com', '9876500019'),
('Sanjay', 'sanjay@example.com', '9876500020');


-- LOANS: 20 records

INSERT INTO loans
(book_id, member_id, borrow_date, due_date, return_date)
VALUES
(1, 1, CURRENT_DATE - 20, CURRENT_DATE - 6, NULL),
(2, 2, CURRENT_DATE - 10, CURRENT_DATE + 4, NULL),
(3, 3, CURRENT_DATE - 25, CURRENT_DATE - 11, CURRENT_DATE - 12),
(4, 4, CURRENT_DATE - 5, CURRENT_DATE + 9, NULL),
(5, 5, CURRENT_DATE - 18, CURRENT_DATE - 4, NULL),
(6, 6, CURRENT_DATE - 30, CURRENT_DATE - 16, CURRENT_DATE - 18),
(7, 7, CURRENT_DATE - 3, CURRENT_DATE + 11, NULL),
(8, 8, CURRENT_DATE - 15, CURRENT_DATE - 1, NULL),
(9, 9, CURRENT_DATE - 12, CURRENT_DATE + 2, NULL),
(10, 10, CURRENT_DATE - 22, CURRENT_DATE - 8, CURRENT_DATE - 9),
(11, 11, CURRENT_DATE - 8, CURRENT_DATE + 6, NULL),
(12, 12, CURRENT_DATE - 28, CURRENT_DATE - 14, CURRENT_DATE - 15),
(13, 13, CURRENT_DATE - 6, CURRENT_DATE + 8, NULL),
(14, 14, CURRENT_DATE - 19, CURRENT_DATE - 5, NULL),
(15, 15, CURRENT_DATE - 4, CURRENT_DATE + 10, NULL),
(16, 16, CURRENT_DATE - 16, CURRENT_DATE - 2, CURRENT_DATE - 3),
(17, 17, CURRENT_DATE - 9, CURRENT_DATE + 5, NULL),
(18, 18, CURRENT_DATE - 24, CURRENT_DATE - 10, CURRENT_DATE - 11),
(19, 19, CURRENT_DATE - 2, CURRENT_DATE + 12, NULL),
(20, 20, CURRENT_DATE - 14, CURRENT_DATE, NULL);


-- Update sequences after inserting explicit IDs

SELECT setval(pg_get_serial_sequence('books', 'book_id'),
              (SELECT MAX(book_id) FROM books));

SELECT setval(pg_get_serial_sequence('members', 'member_id'),
              (SELECT MAX(member_id) FROM members));

SELECT setval(pg_get_serial_sequence('loans', 'loan_id'),
              (SELECT MAX(loan_id) FROM loans));