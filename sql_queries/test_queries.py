from queries import QUERIES, run_query

for query_name, query in QUERIES.items():

    print("\n" + "=" * 50)
    print(query_name)
    print("=" * 50)

    try:
        result = run_query(query)
        print(result.head())

    except Exception as e:
        print("Error:", e)