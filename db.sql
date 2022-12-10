DROP DATABASE Kindergarten;
CREATE DATABASE Kindergarten;
USE Kindergarten;

-- DEBUG
--  SELECT * FROM Kindergarten;
-- select * from Child limit 5,3;


-- -------------

CREATE TABLE Parent
(
ParentID INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
Surname varchar(30),
Name varchar(30),
Patronymic varchar(30),
Phone varchar(13),
Comments varchar(60) DEFAULT NULL
);

CREATE TABLE Family
(
ChildID INT NOT NULL,
ParentID INT NOT NULL,
FOREIGN KEY(ParentID) REFERENCES Parent(ParentID) ON DELETE CASCADE
);

CREATE TABLE Child
(
ChildID INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
GroupID INT NOT NULL,
KindergartenID INT NOT NULL,
Surname varchar(30),
Name varchar(30),
Patronymic varchar(30),
Birthday varchar (10)
);

ALTER TABLE Family
ADD FOREIGN KEY(ChildID) REFERENCES Child(ChildID) ON DELETE CASCADE;

CREATE TABLE Kindergarten
(
KindergartenID INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
NameKindergarten varchar(30),
Address varchar(30),
WorkDaysInWeek INT NOT NULL DEFAULT 7,
ChildrenNumber INT NOT NULL DEFAULT 0,
NominalSum INT NOT NULL
);

ALTER TABLE Kindergarten
ADD CHECK(NominalSum>0 AND ChildrenNumber>=0 AND WorkDaysInWeek>0);

ALTER TABLE Child
ADD FOREIGN KEY(KindergartenID) REFERENCES Kindergarten(KindergartenID) ON DELETE CASCADE;

CREATE TABLE KindergartenGroup
(
GroupID INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
KindergartenID INT NOT NULL,
ChildrenNumber INT NOT NULL DEFAULT 0,
Name varchar(30),
FOREIGN KEY(KindergartenID) REFERENCES Kindergarten(KindergartenID) ON DELETE CASCADE
);

ALTER TABLE KindergartenGroup
ADD CHECK(ChildrenNumber>=0);

ALTER TABLE Child
ADD FOREIGN KEY(GroupID) REFERENCES KindergartenGroup(GroupID) ON DELETE CASCADE;

CREATE TABLE Attendance
(
MonthAndYear varchar(6) NOT NULL,
ChildID INT NOT NULL,
DaysAttended INT NOT NULL DEFAULT 0,
FinalSum INT NOT NULL DEFAULT 0,
isPaid BOOL NOT NULL DEFAULT FALSE,
FOREIGN KEY(ChildID) REFERENCES Child(ChildID) ON DELETE CASCADE
);

CREATE TABLE Month
(
MonthAndYear varchar(6) NOT NULL PRIMARY KEY,
WorkDaysNumber INT NOT NULL DEFAULT 30
);

ALTER TABLE Attendance
ADD FOREIGN KEY(MonthAndYear) REFERENCES Month(MonthAndYear);

ALTER TABLE Parent
ADD CHECK(LENGTH(Phone)=13);

INSERT Kindergarten(NameKindergarten, Address, WorkDaysInWeek, ChildrenNumber, NominalSum)
VALUES
('name1','address1', 24, 2, 1000),
('name2','address2', 25, 1, 1200),
('name3','address3', 26, 3, 1400);
INSERT KindergartenGroup(KindergartenID, ChildrenNumber, Name)
VALUES
(1,1,'group1'),
(1,1,'group2'),
(2,1,'group3'),
(3,2,'group4'),
(3,1,'group5');
INSERT Child(GroupID, KindergartenID, Surname, Name, Patronymic, Birthday)
VALUES
(1, 1, 'Green','John','Joshua','05.11.2015'),
(2, 1, 'Blue','Joshua','Andrew','02.10.2014'),
(3, 2, 'White','Cristiano','Maxym','15.04.2016'),
(4, 3, 'Woods','Max','Volodymyr','08.09.2015'),
(4, 3, 'Reader','Andrew','Yaroslav','20.05.2016'),
(5, 3, 'Surname','Name','Patromymic','16.01.2015');
INSERT Parent(Surname, Name, Patronymic, Phone)
VALUES
('surname1','name1','patronymic1','+380686958887'),
('surname2','name2','patronymic2','+380698454585'),
('surname3','name3','patronymic3','+380657887212'),
('surname4','name4','patronymic4','+380658787875');
INSERT Family(ChildID, ParentID)
VALUES
(1,1),
(2,1),
(3,2),
(4,3),
(5,3),
(6,4);
INSERT Month(MonthAndYear, WorkDaysNumber)
VALUES
('102022',31),
('102021',31),
('112022',30);
INSERT Attendance(MonthAndYear, ChildID, DaysAttended)
VALUES
('102022',1,25),
('112022',1,24),
('102022',2,16),
('102022',3,25),
('102022',4,19),
('112022',4,26),
('102022',5,8),
('102022',6,25);

UPDATE Attendance
JOIN Child on Attendance.ChildID = Child.ChildID
SET isPaid = True
WHERE (SELECT CONVERT((SELECT SUBSTRING(Child.Birthday, 7)), UNSIGNED)) <= 2015;

UPDATE Attendance AS ATT
JOIN Child AS C ON ATT.ChildID = C.ChildID
JOIN Kindergarten AS KID ON C.KindergartenID=KID.KindergartenID
JOIN Month AS M ON ATT.MonthAndYear = M.MonthAndYear
SET FinalSum = KID.NominalSum / M.WorkDaysNumber * ATT.DaysAttended;
