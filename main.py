import pandas as pd
import openai
from fastapi import FastAPI, File, UploadFile
from fastapi.responses import HTMLResponse
from io import StringIO
from openai.error import OpenAIError  # Make sure this is correctly imported


app = FastAPI()

# It's safer to use an environment variable
openai.api_key = 'INSERT API KEY HERE'


async def openai_call(prompt):
    try:
        response = openai.Completion.create(
            engine="gpt-3.5-turbo",  # Adjusted to the appropriate model
            prompt=prompt,
            max_tokens=150,  # Adjusted to generate up to 150 tokens
            n=1,
            logprobs=0
        )
        print("Response from openai:", response)
        return response.choices[0].text.strip()
    except OpenAIError as e:  # Broad catch for OpenAI errors, including rate limits
        # Handle the error (e.g., log it, notify the user, etc.)
        return f"OpenAI error: {str(e)}"


@app.post("/uploadfile/")
async def create_upload_file(file: UploadFile = File(...)):
    # Read the file into a DataFrame
    contents = await file.read()
    df = pd.read_csv(StringIO(contents.decode("utf-8")))
    df_info = dataframe_info(df)
    # TODO: need to add the main prompt
    additional_prompt = "Generate SQL commands to create a database table based on the above CSV file structure and sample data."
    # Sample Data
    random_sample = df.sample(n=min(5, len(df))).reset_index(drop=True)
    complete_prompt = f"This is the dataframe info from the CSV file - {df_info}\n\nSample CSV Data:\n{random_sample.to_string()}\n\n{additional_prompt}"
    print(complete_prompt)
    openai_response = await openai_call(complete_prompt)
    return {"filename": file.filename, "openai_response": openai_response}


def dataframe_to_text(df):
    text_data = ""
    for index, row in df.iterrows():
        row_text = ", ".join(f"{key}: {value}" for key, value in row.items())
        text_data += f"Row {index + 1}: {row_text}\n"
    return text_data


# Get info from dataframe
def dataframe_info(df):
    buffer = StringIO()
    df.info(buf=buffer)
    info_str = buffer.getvalue()
    return info_str


@app.get("/")
async def main():
    content = """
<body>
<form action="/uploadfile/" enctype="multipart/form-data" method="post">
<input name="file" type="file">
<input type="submit">
</form>
</body>
    """
    return HTMLResponse(content=content)
