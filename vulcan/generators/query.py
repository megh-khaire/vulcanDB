import vulcan.generators.metadata as vgm
import vulcan.utils.openai as vuo


def generate_sql_queries(dataframe: str, db_type: str):
    info = vgm.get_dataframe_description(dataframe)
    samples = vgm.get_dataframe_samples(dataframe)
    data = vuo.generate_schema(
        {"database": db_type, "raw_data": samples, "structure": info},
    )
    data = vuo.generate_constraints(data)
    response = vuo.generate_sql_queries(data)
    return response
