import psycopg2

def execute_query(query):
  # Establish a connection to the PostgreSQL database
  conn = psycopg2.connect(
      host="localhost",
      database="nyc_data",
      user="postgres",
      password="super"
  )

  # Create a cursor object
  cur = conn.cursor()

  cur.execute(query)

  # Fetch the results
  results = cur.fetchall()

  cur.close()
  conn.close()
  
  return results

  