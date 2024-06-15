import pandas as pd
import os
import glob
from langchain.embeddings import OpenAIEmbeddings
from dotenv import load_dotenv
import psycopg2

load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

embeddings = OpenAIEmbeddings(
    model="text-embedding-3-large",
    openai_api_key=OPENAI_API_KEY
)

# PostgreSQLデータベースに接続
conn = psycopg2.connect(
    dbname=os.getenv("POSTGRES_DB"),
    user=os.getenv("POSTGRES_USER"),
    password=os.getenv("POSTGRES_PASSWORD"),
    host=os.getenv("POSTGRES_HOST"),
    port=os.getenv("POSTGRES_PORT")
)
cursor = conn.cursor()

# テーブル作成クエリ
create_table_query = """
CREATE TABLE IF NOT EXISTS mammal_embeddings (
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

def get_embedding(text):
    return embeddings.embed_query(text)

# 全CSVファイルに対してベクトル化の処理を実行
for input_file_path in csv_files:
    df = pd.read_csv(input_file_path)

    # ベクトル化
    df['toc(vector)'] = df['toc'].apply(lambda x: get_embedding(x))

    # ベクトルデータをPostgreSQLに挿入
    for index, row in df.iterrows():
        insert_query = """
        INSERT INTO mammal_embeddings (file_name, toc, page, toc_vector)
        VALUES (%s, %s, %s, %s);
        """
        cursor.execute(insert_query, (row['file_name'], row['toc'], row['page'], row['toc(vector)']))

    conn.commit()

cursor.close()
conn.close()
