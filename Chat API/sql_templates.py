SQL_TEMPLATES = {
    "visitors_anytime": """
        SELECT SUM(visitors_count) AS visitors
        FROM banff.city_mobility
        WHERE DATE(datetime) = CURRENT_DATE
    """,

    "total_vehicles_anytime": """
        SELECT SUM(vehicles_count) AS total_vehicles
        FROM banff.city_mobility
    """,

    "residents_anytime": """
        SELECT SUM(resident_count) AS residents
        FROM banff.city_mobility
    """,

    "total_occupancy_at_time": """
        SELECT datetime, vehicles_count
        FROM banff.city_mobility
        WHERE datetime = '{date}'
    """,

    "occupancy_by_hour": """
        SELECT hour, AVG(vehicles_count) AS avg_vehicles
        FROM banff.city_mobility
        GROUP BY hour
        ORDER BY hour
    """,

    "peak_occupancy_day": """
        SELECT DATE(datetime) AS day,
               SUM(vehicles_count) AS vehicles
        FROM banff.city_mobility
        GROUP BY day
        ORDER BY vehicles DESC
        LIMIT 1
    """,

    "low_occupancy_day": """
        SELECT DATE(datetime) AS day,
               SUM(vehicles_count) AS vehicles
        FROM banff.city_mobility
        GROUP BY day
        ORDER BY vehicles ASC
        LIMIT 1
    """
}
