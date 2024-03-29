DROP DATABASE IF EXISTS Art_museum;
CREATE DATABASE Art_museum;
USE Art_museum;

DROP TABLE IF EXISTS ARTIST;
CREATE TABLE ARTIST
	(AName			VARCHAR(30)		NOT NULL,
	Epoch		 	VARCHAR(30),
	Descriptions	VARCHAR(30),
	MainStyle	 	VARCHAR(30),
   	Country_origin	VARCHAR(30),
	DateBorn		VARCHAR(10),	
   	DateDied		VARCHAR(10),
   	PRIMARY KEY(AName));
	
INSERT INTO ARTIST(AName, Epoch, Descriptions, MainStyle, Country_origin, DateBorn, DateDied)
VALUES ('Leonardo Da Vinci', 'Renaissance', 'Scientist and inventor', 'Renaissance', 'Italy', '1452-04-15', '1519-05-02'),
('Imogen Cunningham', '20th Century', 'Photographer', 'Black and White',  'USA', '1883-04-12', '1976-06-23'),
('Frédéric A. Bartholdi', 'Industrial Revolution', 'Famous French sculptor', 'Classical Statues', 'France', '1834-04-02', '1904-10-04'),
('Lewis Hine', 'Industrial Revolution', 'Captured human nature' ,'Black and White', 'USA', '1874-09-26', '1940-11-03'),
('Johannes Vermeer', 'Dutch Golden Age', 'Dutch artist', 'Oil based paintings', 'Dutch Republic', '1632-10-31', '1675-12-15'),
('Paul Landowski', 'Industrial revolution', 'Famous french sculptor', 'Realistic', 'France', '1875-06-01', '1961-03-31');
INSERT INTO ARTIST(AName, Epoch, Descriptions, MainStyle, Country_origin, DateBorn) VALUES
('Nick Ut', 'Transformation age', 'Captured harsh conditions', 'Black and white', 'Vietnam', '1951-03-29');

DROP TABLE IF EXISTS EXHIBITION;
CREATE TABLE EXHIBITION
	(EName    		VARCHAR(50)		NOT NULL,
	Start_date		VARCHAR(10)			NOT NULL,
	End_date		VARCHAR(10),
	PRIMARY KEY(EName));
    
INSERT INTO EXHIBITION(EName, Start_date, End_date)
VALUES ('YSL aux Musées', '2023-01-29', '2023-05-15'), 
('150 years of Mondrian', '2022-10-29', '2023-02-10');

DROP TABLE IF EXISTS ART_OBJECT;
CREATE TABLE ART_OBJECT 
	(Title			VARCHAR(30)			NOT NULL,
	YearCreated		INT, 			 
	Descript	    VARCHAR(30),		
	Epoch			VARCHAR(30),
	CultureOfOrigin	VARCHAR(30),
	ArtID 			VARCHAR(10)			NOT NULL,
	Artist_Name		VARCHAR(30),
    ExName			VARCHAR(50)		DEFAULT NULL,
	PRIMARY KEY(ArtID),
	CONSTRAINT ANFFK	
		FOREIGN KEY(Artist_Name) REFERENCES ARTIST(AName)
			ON DELETE SET NULL ON UPDATE CASCADE,   -- better design than ON DELETE CASCADE as records for other tables are preserved.
	CONSTRAINT EFFK
		FOREIGN KEY(ExName) REFERENCES EXHIBITION(EName)
			ON DELETE SET NULL ON UPDATE CASCADE);

INSERT INTO ART_OBJECT(Title, YearCreated, Descript, Epoch, CultureOfOrigin, ArtID, Artist_Name, ExName)
VALUES ('Mona Lisa', '1503', 'Very famous', 'Renaissance', 'Italy', 'P-0000', 'Leonardo Da Vinci', 'YSL aux Musées'),
('Magnolia Blossom', '1925', 'Black and white', '20th Century', 'USA', 'O-0001', 'Imogen Cunningham', '150 years of Mondrian');

INSERT INTO ART_OBJECT(Title, YearCreated, Descript, Epoch, CultureOfOrigin, ArtID, Artist_Name) VALUES
('The Terror of War', '1972', 'Photograph depicting war', 'Transformation age', 'USA', 'O-0002', 'Nick Ut'),
('Cotton Mill Girl', '1908', 'Industrial revolution', 'Industrial revolution', 'USA', 'O-0003', 'Lewis Hine'),
('Girl with a Pearl Earring','1665', 'Woman with earring' , 'Dutch Golden Age', 'Dutch Republic', 'P-0001', 'Johannes Vermeer'),
('Statue of Liberty', '1876', 'Well-known statue', 'Industrial Revolution', 'France', 'L-0001', 'Frédéric A. Bartholdi'),
('Christ the Redeemer', '1931', 'Statue of Jesus Christ', 'Roaring 20s', 'Brazil', 'L-0002', 'Paul Landowski');

DROP TABLE IF EXISTS PERMANENT_COLLECTION;
CREATE TABLE PERMANENT_COLLECTION
	(ArtID			CHAR(10),
	DateAcquired	VARCHAR(10)			NOT NULL,
    Status			VARCHAR(20)		NOT NULL,  -- Status: on display, on loan, or stored
    Cost			int				NOT NULL,
    PRIMARY KEY(ArtID),
    CONSTRAINT AOFFK
		FOREIGN KEY(ArtID) REFERENCES ART_OBJECT(ArtID)
			ON DELETE CASCADE		ON UPDATE CASCADE);
            
INSERT INTO PERMANENT_COLLECTION (ArtID, DateAcquired, Status, Cost)
VALUES ('O-0001', '2021-01-01', 'On display', '22000'),
('O-0002', '2021-06-05', 'On display', '50000'),
('O-0003', '2008-05-23', 'On display', '100000'),
('P-0001', '2000-02-01', 'Locked up', '500000');

DROP TABLE IF EXISTS OTHER_COLLECTION;
CREATE TABLE OTHER_COLLECTION
	(OName			VARCHAR(100)			NOT NULL,
    Address	   	 	VARCHAR(60),
    Descrip			VARCHAR(500),
    Otype			VARCHAR(10),
    ContactPhone	VARCHAR(30)			UNIQUE, -- Can't be INT as it is larger than MAX INT
    ContactName		VARCHAR(30)			UNIQUE,
    PRIMARY KEY(OName));

INSERT INTO OTHER_COLLECTION (OName, Address, Descrip, Otype, ContactPhone, ContactName)
VALUES ('Renaissance Collection', '5811 S Ellis Ave, Chicago, IL', 'The Renaissance Society', 
'Museum', '17737028670', 'Pierre Sondeljker'),
('National Park Service', '1849 C Street, Washington, DC', 'Manages parks and monuments', 'Government', '8008778339', 'Charles F. Sams III');

INSERT INTO OTHER_COLLECTION (OName, Address, Descrip, Otype, ContactPhone, ContactName) VALUES
('Brazil MoC', 'Esplanada dos Ministérios BL B, Brasília', 'Regulates historical artifacts', 'Government', '556120242287', 'Felipe Carmona Cantera');


DROP TABLE IF EXISTS BORROWED_COLLECTION;
CREATE TABLE BORROWED_COLLECTION 
	(ArtID				CHAR(10),
	collection_name	   	VARCHAR(40),
	Date_borrowed  		VARCHAR(10)			NOT NULL,
	Date_returned	    VARCHAR(10),
	PRIMARY KEY(ArtID),
	CONSTRAINT BAFFK
		FOREIGN KEY(ArtID) REFERENCES ART_OBJECT(ArtID)
			ON DELETE CASCADE			ON UPDATE CASCADE,
	CONSTRAINT OCFFK
		FOREIGN KEY(collection_name) REFERENCES OTHER_COLLECTION(OName)
			ON DELETE SET NULL			ON UPDATE CASCADE);

INSERT INTO BORROWED_COLLECTION (ArtID, collection_name, Date_borrowed, Date_returned)
VALUES ('P-0000', 'Renaissance Collection', '2022-10-28', '2023-05-20'),
('L-0001', 'National Park Service', '2022-11-01', '2023-05-20'),
('L-0002', 'Brazil MoC', '2022-10-20', '2022-11-20');

DROP TABLE IF EXISTS OTHER;
CREATE TABLE OTHER 
	(ArtID 			CHAR(10),
	Type			VARCHAR(20),
	Style	        VARCHAR(30),
	PRIMARY KEY(ArtID),
	CONSTRAINT OAIFKK
		FOREIGN KEY(ArtID) REFERENCES ART_OBJECT(ArtID)
			ON DELETE CASCADE		ON UPDATE CASCADE);
            
INSERT INTO OTHER (ArtID, Type, Style) 
VALUES ('O-0001', 'Photograph', 'Floral'),
('O-0002', 'Photograph', 'War'),
('O-0003', 'Photograph', 'Social Change');

DROP TABLE IF EXISTS PAINTING;
CREATE TABLE PAINTING 
	(ArtID 			CHAR(10),
	Style			VARCHAR(20),
	Paint_type		VARCHAR(20),
	Drawn_on		VARCHAR(20),
	PRIMARY KEY(ArtID),
    CONSTRAINT PFFK
		FOREIGN KEY(ArtID) REFERENCES ART_OBJECT(ArtID)
			ON DELETE CASCADE	ON UPDATE CASCADE);
    
INSERT INTO PAINTING (ArtID, Style, Paint_type, Drawn_on) 
VALUES ('P-0000', 'Renaissance', 'Portrait', 'Cottonwood'),
('P-0001', 'Dutch Golden Age', 'Portrait', 'Canvas');

DROP TABLE IF EXISTS STATUE;
CREATE TABLE STATUE
	(ArtID 			CHAR(10),
	Height_m		FLOAT,
	Weight_t		FLOAT,			
	Style			VARCHAR(20),
	Material		VARCHAR(50),
	PRIMARY KEY(ArtID),
    CONSTRAINT SAFFK
		FOREIGN KEY(ArtID) REFERENCES ART_OBJECT(ArtID)
			ON DELETE CASCADE		ON UPDATE CASCADE);
 INSERT INTO STATUE (ArtID, Height_m, Weight_t, Style, Material) 
 VALUES ('L-0001', '46.0', '204.1', 'neoclassical', 'Metal'),
 ('L-0002', '28.0', '635.0', 'catholic', 'Cement');

DROP ROLE IF EXISTS dguest@localhost;
DROP ROLE IF EXISTS dadmin@localhost;
DROP ROLE IF EXISTS dinsert@localhost;
CREATE ROLE dguest@localhost;
GRANT SELECT ON ART_MUSEUM. * TO dguest@localhost;
CREATE ROLE dinsert@localhost;
GRANT SELECT, INSERT, DELETE, UPDATE ON ART_MUSEUM. * TO dinsert@localhost;
CREATE ROLE dadmin@localhost;
GRANT ALL PRIVILEGES ON ART_MUSEUM.* TO dadmin@localhost;
DROP USER IF EXISTS guest@localhost;
DROP USER IF EXISTS admin@localhost;
DROP USER IF EXISTS insert_user@localhost;
CREATE USER admin@localhost IDENTIFIED WITH mysql_native_password BY 'password';
CREATE USER guest@localhost IDENTIFIED WITH mysql_native_password BY '';
CREATE USER insert_user@localhost IDENTIFIED WITH mysql_native_password BY 'password';
GRANT dadmin@localhost TO admin@localhost;
GRANT dguest@localhost TO guest@localhost;
GRANT dinsert@localhost TO insert_user@localhost;
SET DEFAULT ROLE ALL TO admin@localhost;
SET DEFAULT ROLE ALL TO guest@localhost;
SET DEFAULT ROLE ALL TO insert_user@localhost;
ALTER USER 'root'@'localhost' identified with mysql_native_password by 'password';
ALTER USER 'guest'@'localhost' identified with mysql_native_password by '';
FLUSH privileges;
