from backend.llm import LLMClient

def main():
    llm = LLMClient()
    query = "プレミアリーグでハーランドは何ゴール決めていますか？"
    sql = llm.generate_sql(query)
    print(sql)

if __name__ == "__main__":
    main() 