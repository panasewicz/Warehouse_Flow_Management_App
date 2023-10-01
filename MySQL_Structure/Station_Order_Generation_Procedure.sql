CREATE PROCEDURE InsertProduct (IN p_Scanner_ID INT, IN p_Order_Station_Id INT, IN p_Scanner_Scan_Status INT, IN p_Barcode_Number INT, IN p_Error_Comment VARCHAR(255), IN p_Date_created DATE, IN p_Time_created TIME)
BEGIN
    DECLARE v_order_id INT;
    DECLARE v_product_id INT;
    DECLARE v_min_order_id INT;
    DECLARE v_to_write INT;

    SELECT IFNULL(MAX(order_id), 0) + 1 INTO v_order_id FROM write_value;

    INSERT INTO product (Scanner_ID, Order_Station_Id, Scanner_Scan_Status, Barcode_Number, Error_Comment, Date_created, Time_created)
    VALUES (p_Scanner_ID, p_Order_Station_Id, p_Scanner_Scan_Status, p_Barcode_Number, p_Error_Comment, p_Date_created, p_Time_created);
    
    SELECT LAST_INSERT_ID() INTO v_product_id;

    IF p_Error_Comment = 'null' THEN
        SET v_to_write = FLOOR(1 + RAND() * 3);
    ELSE
        SET v_to_write = 0;
    END IF;

    IF v_order_id > 11 THEN
        SELECT MIN(order_id) INTO v_min_order_id FROM write_value;
        UPDATE write_value SET 
            product_id = v_product_id,
            Scanner_ID = p_Scanner_ID,
            Order_Station_Id = p_Order_Station_Id,
            Scanner_Scan_Status = p_Scanner_Scan_Status,
            Barcode_Number = p_Barcode_Number,
            Error_Comment = p_Error_Comment,
            Date_created = p_Date_created,
            Time_created = p_Time_created,
            to_write = v_to_write,
            order_id = v_order_id
        WHERE order_id = v_min_order_id;
    ELSE
        INSERT INTO write_value (product_id, Scanner_ID, Order_Station_Id, Scanner_Scan_Status, Barcode_Number, Error_Comment, Date_created, Time_created, to_write, order_id) 
        VALUES (v_product_id, p_Scanner_ID, p_Order_Station_Id, p_Scanner_Scan_Status, p_Barcode_Number, p_Error_Comment, p_Date_created, p_Time_created, v_to_write, v_order_id);
    END IF;

END $$