## Comments
1. If table **product_stocks** doesn't exist in database we need 
    another function to create table with SQL query like: 
    **"CREATE TABLE product_stocks
                  (time, product_id, variant_id, stock_id, supply)"**
2. If existing base is not empty and already has records with product_id which values 
    we want to modify, we should write function to update record with SQL query: 
    **"UPDATE product_stocks SET some_column = some_value WHERE product_id = some_id"**.
    Probably product_id is unique so INSERT INTO query may cause problems with saving record 
    with id which already exist in database.