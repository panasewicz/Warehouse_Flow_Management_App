CREATE TABLE product (
    id INT AUTO_INCREMENT PRIMARY KEY,
    Scanner_ID INT,
    Order_Station_Id INT,
    Scanner_Scan_Status INT,
    Barcode_Number INT,
    Error_Comment VARCHAR(255),
    Date_created DATE,
    Time_created TIME
);

CREATE TABLE write_value (
    product_id INT,
    Scanner_ID INT,
    Order_Station_Id INT,
    Scanner_Scan_Status INT,
    Barcode_Number INT,
    Error_Comment VARCHAR(255),
    Date_created DATE,
    Time_created TIME,
    to_write INT,
    FOREIGN KEY (product_id) REFERENCES product(id)
);
