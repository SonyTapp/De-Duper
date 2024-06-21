CREATE TABLE unique_images(
    Image_ID INT PRIMARY KEY IDENTITY(1,1) NOT NULL,
    Image_Path NVARCHAR(200) NOT NULL
)
CREATE TABLE duplicate_images(
    Image_ID INT PRIMARY KEY IDENTITY(1,1) NOT NULL,
    Image_Path NVARCHAR(200) NOT NULL
)
SELECT * FROM duplicate_images;
SELECT * FROM unique_images;

DROP TABLE duplicate_images;
DROP TABLE unique_images;
