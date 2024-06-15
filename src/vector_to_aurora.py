import pandas as pd
import os
import glob
from langchain_openai import OpenAIEmbeddings
from dotenv import load_dotenv
import psycopg2

load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

embeddings = OpenAIEmbeddings(
    model="text-embedding-3-large",
    openai_api_key=OPENAI_API_KEY
)

conn = psycopg2.connect(
    dbname=os.getenv("DATABASE_NAME"),
    user=os.getenv("DATABASE_USER"),
    password=os.getenv("DATABASE_PASSWORD"),
    host=os.getenv("DATABASE_HOST"),
    port=os.getenv("DATABASE_PORT")
)
cursor = conn.cursor()

create_table_query = """
CREATE TABLE IF NOT EXISTS toc_embeddings (
    id SERIAL PRIMARY KEY,
    file_name TEXT,
    toc TEXT,
    page INTEGER,
    toc_vector FLOAT8[]
);
"""
cursor.execute(create_table_query)
conn.commit()

input_directory = '../data/csv/'
csv_files = glob.glob(os.path.join(input_directory, '*.csv'))
print(csv_files)

def get_embedding(text):
    embedding = embeddings.embed_query(text)
    print("Embedding for text:", text, "is", embedding)
    return embedding


# 全CSVファイルに対してベクトル化の処理を実行
for input_file_path in csv_files:
    df = pd.read_csv(input_file_path)

    # ベクトル化
    df['toc(vector)'] = df['toc'].apply(lambda x: get_embedding(x))

    # ベクトルデータをPostgreSQLに挿入
    for index, row in df.iterrows():
        print("Inserting row:", row)
        insert_query = """
        INSERT INTO toc_embeddings (file_name, toc, page, toc_vector)
        VALUES (%s, %s, %s, %s);
        """
        cursor.execute(insert_query, (row['file_name'], row['toc'], row['page'], row['toc(vector)']))
        print("Row inserted")

    conn.commit()

cursor.close()
conn.close()
