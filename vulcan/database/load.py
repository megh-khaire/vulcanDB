from sqlalchemy import MetaData


def push_data_in_db(engine, dataframe, table_order):
    # Reflect the database schema
    metadata = MetaData()
    metadata.reflect(bind=engine)

    # Process and insert data for each table
    for table_name in table_order:
        table = metadata.tables.get(table_name)
        if table is None:
            print(f"Table {table_name} does not exist in the database.")
            continue

        # Determine which columns are present both in the DataFrame and the table
        table_columns_in_df = [
            col.name for col in table.columns if col.name in dataframe.columns
        ]

        # Create a temporary DataFrame filtered to relevant columns
        df_filtered = dataframe[table_columns_in_df].copy()

        # Remove auto-increment columns from DataFrame
        for col in table.columns:
            if (
                col.autoincrement
                and col.autoincrement != "auto"
                and col.name in df_filtered.columns
            ):
                df_filtered.drop(columns=[col.name], inplace=True, errors="ignore")

        # Insert the filtered DataFrame into the database
        df_filtered.to_sql(table_name, con=engine, if_exists="append", index=False)
        print(f"Data successfully inserted into {table_name}.")
