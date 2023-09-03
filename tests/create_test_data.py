import psycopg2
from psycopg2.extras import execute_values
from ppygis3 import Point
import random

def generate_random_coordinates():
    lat = random.uniform(8.4, 37.6)
    lon = random.uniform(68.1, 97.4)
    return (lat, lon)
    


def insert_test_data(num_rows):
    print(f"Inserting {num_rows} rows")
    
    table= 'test_scatter'
    
    # Connect to the database
    conn = psycopg2.connect(
      host="localhost",
      database="nyc_data",
      user="postgres",
      password="super"
    )
    
    cur = conn.cursor()

    # CREATE THE TABLE
    # cur.execute(f"""
    #     CREATE TABLE IF NOT EXISTS {table} (
    #         id SERIAL PRIMARY KEY,
    #         lat NUMERIC NOT NULL,
    #         lon NUMERIC NOT NULL,
    #         geom GEOMETRY(POINT, 4326) NOT NULL
    #     )
    # """)
    
    # # Delete all rows from the table
    cur.execute(f"DELETE FROM {table}")

    # Generate test data
    data = []
    for i in range(num_rows):
        lat, lon = generate_random_coordinates()
        point = Point(lon, lat, srid=4326)
        data.append((i+1, lat, lon, point))

    # Insert test data into the table
    execute_values(
        cur,
        f"INSERT INTO {table} (id, lat, lon, geom) VALUES %s",
        data,
        template="(%s, %s, %s, %s)"
    )

    # Commit the changes and close the connection
    conn.commit()
    cur.close()
    conn.close()
    
if __name__ == "__main__":
    rows = 100_000
    insert_test_data(rows)