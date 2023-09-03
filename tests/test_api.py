from create_test_data import insert_test_data, generate_random_coordinates
import time
import timeit
import requests
import json

api_response_logs_path = "./logs/api_output.txt"
api_benchmark_logs_path = "./logs/api_benchmark.txt"
query_response_time_logs_path = "./logs/query_response_time.txt"

def call_api():
    lat, lon = generate_random_coordinates()
    url = f"http://localhost:5000/nearby?lat={lat}&lon={lon}"
    response = requests.get(url)
    
    with open(api_response_logs_path, "a") as f:
        f.write(f"({lon}, {lat})\n")
        json.dump(response.json(), f)
        f.write("\n\n")
        f.close()


def write_benchmark_logs(message):
     with open(api_benchmark_logs_path, "a") as f:
        f.write(f"{message}\n")
        f.close()

def test_api(steps):
    with open(api_response_logs_path, "a") as f:
        f.truncate(0)        
        f.close()
    
    with open(api_benchmark_logs_path, "a") as f:
        f.truncate(0)        
        f.close()
        
    with open(query_response_time_logs_path, "a") as f:
        f.write(f"\n\nStarting a new test run via test_api.py\n")       
        f.close()
        
    for rows in steps:
        with open(api_response_logs_path, "a") as f:
            f.write(f"Responses for the step with {rows} rows:\n\n")
            f.close()
        
        write_benchmark_logs(f"Inserting {rows} rows to postgres")
        
        start_time = time.perf_counter()
        insert_test_data(rows)
        end_time = time.perf_counter()
                
        
        elapsed_time = end_time - start_time
        write_benchmark_logs(f"Inserted {rows} rows successfully in {elapsed_time:.6f} seconds")
        print(f"Elapsed time: {elapsed_time:.6f} seconds")
        
        times = 10
        elapsed_query_time = timeit.timeit(stmt=call_api, number=times) / times
        write_benchmark_logs(f"Average query time for {rows} rows: {elapsed_query_time:.6f} seconds\n\n\n")
        print(f"Average query time for {rows} rows: {elapsed_query_time:.6f} seconds\n\n")
        
        with open(api_response_logs_path, "a") as f:
            f.write("\n\n\n")
            f.close()
        

if __name__ == "__main__":
    steps= [1_000_000]
    test_api(steps)

    