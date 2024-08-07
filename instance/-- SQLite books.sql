-- SQLite
-- Populate the book table with professional content
INSERT INTO book (name, content, author, section_id, date_issued) VALUES 
('Dune', 'An epic science fiction novel set in a distant future amidst a huge interstellar empire.', 'Frank Herbert', 1, '2024-08-01'),
('Steve Jobs', 'A biography of Steve Jobs, the co-founder of Apple Inc.', 'Walter Isaacson', 2, '2024-08-02'),
('Sapiens: A Brief History of Humankind', 'Exploring the history of humankind from the Stone Age to the present.', 'Yuval Noah Harari', 3, '2024-08-03'),
('Harry Potter and the Sorcerers Stone', 'A young boy discovers he is a wizard and attends a magical school.', 'J.K. Rowling', 4, '2024-08-04'),
('The Innovators', 'How a group of hackers, geniuses, and geeks created the digital revolution.', 'Walter Isaacson', 5, '2024-08-05'),
('The Body: A Guide for Occupants', 'An exploration of the human body, how it works, and how it heals.', 'Bill Bryson', 6, '2024-08-06'),
('How to Win Friends and Influence People', 'A self-help book that provides practical advice on interpersonal skills.', 'Dale Carnegie', 7, '2024-08-07'),
('The Girl with the Dragon Tattoo', 'A mystery novel involving the investigation of a woman disappearance 40 years ago.', 'Stieg Larsson', 8, '2024-08-08'),
('To Kill a Mockingbird', 'A classic novel of a child growing up in the segregated American South.', 'Harper Lee', 9, '2024-08-09'),
('The Art of War', 'An ancient Chinese military treatise on strategy, tactics, and philosophy.', 'Sun Tzu', 10, '2024-08-10');

-- Verify that books have been added
SELECT * FROM book;

