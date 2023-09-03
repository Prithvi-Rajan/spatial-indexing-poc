from flask import request
from flask_restful import Resource
from postgres_client import execute_query
import time


class Nearby(Resource):
    def get(self):
        table= "test_scatter"
        query_response_time_logs_path = "./logs/query_response_time.txt"


        latitude= request.args.get('lat')
        longitude= request.args.get('lon')
        
        query = f"""SELECT {table}.id, {table}.lat, {table}.lon,
                        ST_AsEWKT({table}.geom),
                        {table}.geom <-> ST_SetSRID(ST_MakePoint({longitude}, {latitude}), 4326)::geometry AS dist
                    FROM
                        {table}
                    ORDER BY
                        dist
                    LIMIT 3"""
        start_time = time.perf_counter()
        resp = str(execute_query(query))
        end_time = time.perf_counter()
        
        
        elapsed_time = end_time - start_time
        with open(query_response_time_logs_path, "a") as f:
            f.write(f"{elapsed_time:.6f}\n")       
            f.close()
        return resp
