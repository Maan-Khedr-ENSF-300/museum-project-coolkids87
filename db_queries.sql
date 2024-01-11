-- SQL Queries

-- Query 1)
-- Retrieves all tables

SELECT * FROM ARTIST;
SELECT * FROM EXHIBITION;
SELECT * FROM ART_OBJECT;
SELECT * FROM OTHER;
SELECT * FROM PAINTING;
SELECT * FROM STATUE;
SELECT * FROM PERMANENT_COLLECTION;
SELECT * FROM OTHER_COLLECTION;
SELECT * FROM BORROWED_COLLECTION;

-- These tables are related in many ways. 
-- OTHER, PAINTING, and STATUE are subclasses of ART_OBJECT connected by the key ArtID.
-- Within ART_OBJECT we have triggers for ExName(exhibition name) and Artist_Name that perform CASCADEs on DELETEs and UPDATEs.
-- PERMANENT_COLLECTION and BORROWED_COLLECTION are also subclasses of ART_OBJECT connected by the key ArtID.
-- BORROWED_COLLECTION is a collection with art objects borrowed from the collections within OTHER_COLLECTION.
-- ART_OBJECT and ARTIST are related through a relationship of creation. The ART_OBJECT is created by an ARTIST(or multiple artists) and the ARTIST creates ART_OBJECTs.
-- ART_OBJECTs are related to EXHIBITION through their respective keys.

-- Query 2)
-- Retrieves artist table

SELECT * FROM ARTIST;

-- Query 3)
-- retrieves and displays titles of objects in order from newest to oldest (DESC)

SELECT Title 
FROM ART_OBJECT
ORDER BY YearCreated DESC;

-- Query 4)
-- Nested retrieval query
-- will output the name's of artists that have created objects that are all created later than all Italian art objects

SELECT Artist_Name
FROM ART_OBJECT
WHERE YearCreated > ALL (SELECT YearCreated
						FROM ART_OBJECT
						WHERE CultureOfOrigin = 'Italy');

-- Query 5)

SELECT Title, AName, Descriptions
FROM ART_OBJECT
JOIN ARTIST ON ARTIST.AName = ART_OBJECT.Artist_Name;


--  Query 6) 
-- Test updates and deletes in the ART_OBJECT table
-- having issues with this query, getting an error code 1452 which has to do with FK constraints. Everything seems ok to me...

UPDATE ART_OBJECT
SET	YearCreated = 1942
WHERE ArtID = 'P-0001';

SELECT * FROM ART_OBJECT;
-- Above, update works functionally if confined to one table whereby the attr. changed is not present in any other table, but doesn't work if changing an FK linked to PK of other table or attr. present in other tables. 
-- CASCADE trigger works for sure for DELETE FROM, but UPDATE there's clearly a child-parent constraint issue between FK/PK of differing tables.
DELETE FROM ART_OBJECT
WHERE Artist_Name = 'Leonardo Da Vinci';

SELECT * FROM ART_OBJECT;
SELECT * FROM ARTIST;

-- Above, I ensured the ON DELETE SET NULL trigger works when deletion of an artist from child table does not affect the deletion of the PK of parent table. So, records in parent table that are linked by a PK/FK constraint from the record deleted in child table will not be affected.

-- Query 7)
-- Test deletion with primary key

DELETE FROM ART_OBJECT	
WHERE ArtID = 'O-0001';

-- Now, we can see that all tuples containing ArtID = 'O-0001' have been removed from the database:

SELECT * FROM ARTIST;
SELECT * FROM EXHIBITION;
SELECT * FROM ART_OBJECT;
SELECT * FROM OTHER;
SELECT * FROM PAINTING;
SELECT * FROM STATUE;
SELECT * FROM PERMANENT_COLLECTION;
SELECT * FROM OTHER_COLLECTION;
SELECT * FROM BORROWED_COLLECTION;

