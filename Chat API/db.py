import duckdb

def run_sql(sql: str):

    # Create an in-memory DuckDB and install the SQLite extension first
    tmp = duckdb.connect(database=':memory:', read_only=False)
    tmp.execute("INSTALL sqlite;")
    tmp.execute("LOAD sqlite;")

    # Now open your SQLite file using the installed extension
    con = duckdb.connect(database=':memory:', read_only=False)
    con.execute("LOAD sqlite;")

    # ATTACH the SQLite DB as an external database
    con.execute("ATTACH '/data/banff_city.db' AS banff (TYPE sqlite);")

    # Run SQL against the attached SQLite DB
    df = con.execute(sql).df()

    con.close()
    tmp.close()

    return df
