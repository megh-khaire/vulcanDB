import os


def delete_database(db_file: str):
    """
    Deletes the database file if it exists.

    :param db_file: The file path of the database to delete.
    """
    if os.path.exists(db_file):
        os.remove(db_file)
        print(f"Deleted existing database file: {db_file}")
    else:
        print("Database file does not exist, no need to delete.")
