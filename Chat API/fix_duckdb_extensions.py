import duckdb

con = duckdb.connect()  # crea DB temporal

# Instala la extensión sqlite
con.execute("INSTALL sqlite;")
con.execute("LOAD sqlite;")

print("SQLite extension installed!")

con.close()
