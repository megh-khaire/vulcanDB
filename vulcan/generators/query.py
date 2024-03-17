import vulcan.generators.metadata as vgm
from vulcan.configs.prompts import query_generation_prompt
from vulcan.utils.lang_chain import generate_sequential_chain_response


def generate_sql_queries(dataframe: str, db_type: str):
    info = vgm.get_dataframe_description(dataframe)
    samples = vgm.get_dataframe_samples(dataframe)
    response = generate_sequential_chain_response(
        query_generation_prompt,
        {"database": db_type, "raw_data": samples, "structure": info},
    )
    return response
