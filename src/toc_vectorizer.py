import pandas as pd
import os
import glob
from langchain_openai import OpenAIEmbeddings
from dotenv import load_dotenv

load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

embeddings = OpenAIEmbeddings(
    model="text-embedding-3-large",
    openai_api_key=OPENAI_API_KEY
)

input_directory = '../data/csv/'
output_directory = '../data/csv(vector)'
os.makedirs(output_directory, exist_ok=True)

# 入力ディレクトリ内の全CSVファイルを取得
csv_files = glob.glob(os.path.join(input_directory, '*.csv'))

# toc列の値をembeddingに変換する関数
def get_embedding(text):
    return embeddings.embed_query(text)

# 各CSVファイルに対してベクトル化の処理を実行
for input_file_path in csv_files:
    output_file_path = os.path.join(output_directory, os.path.splitext(os.path.basename(input_file_path))[0] + '_vectorized.csv')

    df = pd.read_csv(input_file_path)

    # "toc(vector)"列を追加してベクトル化
    df['toc(vector)'] = df['toc'].apply(lambda x: get_embedding(x))

    df.to_csv(output_file_path, index=False)
