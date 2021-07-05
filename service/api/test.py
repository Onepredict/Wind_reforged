import time
from flask import Response
from flask_restful import Resource, request


class TestAPI(Resource):
    @classmethod
    def get(cls):
        device_id = request.args.get('device_id')
        time_current = time.strftime('%y-%m-%d %H:%M:%S')
        res = f'''<!DOCTYPE html><html><body><h1>
        In testing<br> ID: {device_id}<br>Current time: {time_current}
        </h1></body></html>'''
        return Response(res, mimetype='text/html')