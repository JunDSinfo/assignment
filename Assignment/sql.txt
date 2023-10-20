-- Create table for cats
CREATE TABLE Cats (
   id INT PRIMARY KEY,
   name VARCHAR(50),
   age INT,
   favoriteFood VARCHAR(50)
);

-- Create table for dogs
CREATE TABLE Dogs (
   id INT PRIMARY KEY,
   name VARCHAR(50),
   age INT,
   favoriteFood VARCHAR(50),
   breed VARCHAR(50)
);

-- Sample insert statements for cats
INSERT INTO Cats (id, name, age, favoriteFood)
VALUES (1, 'Kitty', 5, 'Tuna');

INSERT INTO Cats (id, name, age, favoriteFood)
VALUES (2, 'Garfield', 8, 'Lasagna');

-- Sample insert statements for dogs
INSERT INTO Dogs (id, name, age, favoriteFood, breed)
VALUES (1, 'Buddy', 6, 'Bones', 'Labrador');

INSERT INTO Dogs (id, name, age, favoriteFood, breed)
VALUES (2, 'Max', 4, 'Steak', 'German Shepherd');

SELECT *FROM Dogs;
SELECT *FROM Cats;