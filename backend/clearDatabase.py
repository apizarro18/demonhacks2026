from database import database


def clearTables():
    db = database()

    db.clear_all_data()

    db.reset_table_sequence("raw_news")
    db.reset_table_sequence("parsed_incidents")

    print("Successfully cleared all data and reset id counter!")

if __name__ == "__main__":
    clearTables()