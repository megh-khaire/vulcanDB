import vulcan.generators.metadata as vgm
import sqlvalidator

from vulcan.configs.prompts import query_generation_prompt
from vulcan.utils.lang_chain import generate_sequential_chain_response


def validate_sql_query(query: str):
    # Parsing the sql query
    parsed_query = sqlvalidator.parse(query)
    # Checking the validity of the parsed query
    is_valid = parsed_query.is_valid()
    # Returning the validity and errors if any
    return is_valid, parsed_query.errors


def generate_sql_queries(csv_file_path: str):
    df = vgm.read_csv(csv_file_path)
    info = vgm.get_dataframe_description(df)
    samples = vgm.get_dataframe_samples(df)
    response = generate_sequential_chain_response(
        query_generation_prompt,
        {"raw_data": samples, "structure": info},
    )
    return response
