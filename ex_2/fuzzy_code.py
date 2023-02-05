import datetime
from json import load
from sqlite3 import connect, OperationalError
from requests import request


def fetch_product_data(item_id):
    """
    Fetches data from server.
    :param item_id: single item id
    :return: product info as bytes object
    """
    try:
        product_id = str(item_id)
        url = "https://dummy.server/products/example?id="
        response = request(
                    "GET", url + product_id
                )
        return response.content

    except ConnectionError as err:
        print("Connection error:", err)


def write_retrieved_data(retrieved_data):
    """
    Writes retrieved data as text file.
    :param retrieved_data: product info
    :return: text file with data written in binary mode
    """
    with open("tmp.txt", "wb") as txt_file:
        txt_file.write(retrieved_data)
        txt_file.flush()
        print("data downloaded from server " + str(len(retrieved_data)))
    return txt_file


def load_written_data(saved_file):
    """
    Converts object to json.
    :param saved_file: text file
    :return: json object as a dictionary
    """
    try:
        with open(f"{saved_file.name}", "r") as txt_file:
            loaded_file = load(txt_file)
        return loaded_file

    except FileNotFoundError as err:
        print("File doesn't exist:", err)


def save_to_db(supplied_item):
    """
    Saves product info to database.
    :param supplied_item: info about supplied product
    """
    try:
        DB_NAME = "database.sqlite"
        conn = connect(DB_NAME)
        cursor = conn.cursor()
        query = """INSERT INTO product_stocks
                            (time, product_id, variant_id, stock_id, supply)
                            VALUES 
                            (?,?,?,?,?)"""

        cursor.execute(query, supplied_item)
        conn.commit()
        conn.close()

    except OperationalError as err:
        print("Table doesn't exist:", err)


if __name__ == "__main__":
    items_ids = [-2, -3]
    for item in items_ids:
        data = fetch_product_data(item)
        file = write_retrieved_data(data)
        product = load_written_data(file)
        if product["type"] != "bundle":
            print("product loaded")

            for x in product["supply"]:
                for y in x["stock_data"]:
                    if y["stock_id"] == 1:
                        product_supply = y["quantity"]

                        supplied_product = (
                            str(datetime.datetime.now())[:19],
                            str(product["id"]),
                            str(x["variant_id"]),
                            str(1),
                            str(product_supply)
                        )

                        save_to_db(supplied_product)

        elif product["type"] == "bundle":
            products_ids = []
            for p in product["bundle_items"]:
                products_ids.append(p["id"])
            print("products " + str(len(products_ids)))
            product_id = product["id"]
            total_supply = []
            for p in products_ids:
                data = fetch_product_data(item)
                file = write_retrieved_data(data)
                product = load_written_data(file)
                supply = 0
                for stock in product["supply"]:
                    print(stock)
                    for s in stock["stock_data"]:
                        if s["stock_id"] == 1:
                            supply += s["quantity"]
                            total_supply.append(supply)
            product_supply = min(total_supply)
            supplied_product = (
                str(datetime.datetime.now())[:19],
                str(product_id),
                "NULL",
                str(1),
                str(product_supply)
            )

            save_to_db(supplied_product)
