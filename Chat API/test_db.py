import duckdb
con = duckdb.connect("data/banff_city.db")
df = con.execute("SELECT SUM(visitors_count) FROM city_mobility").df()
print(df)
