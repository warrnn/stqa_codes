from flask import Flask
import status

app = Flask(__name__)

COUNTERS = {}

@app.route("/counters/<name>", methods=["POST"])
def create_counter(name):
    """Creates a counter"""
    global COUNTERS
    
    if name in COUNTERS:
        return {}, status.HTTP_409_CONFLICT
    
    COUNTERS[name] = 1
    return {name: COUNTERS[name]}, status.HTTP_201_CREATED

@app.route("/counters/<name>", methods=["PUT"])
def update_counter(name):
    """Updates a counter"""
    global COUNTERS
    
    if name not in COUNTERS:
        return {}, status.HTTP_404_NOT_FOUND
    
    COUNTERS[name] += 1
    return {name: COUNTERS[name]}, status.HTTP_200_OK

@app.route("/counters/<name>", methods=["GET"])
def read_counter(name):
    """Reads a counter"""
    global COUNTERS
    
    if name not in COUNTERS:
        return {}, status.HTTP_404_NOT_FOUND
    
    return {name: COUNTERS[name]}, status.HTTP_200_OK

@app.route("/counters/<name>", methods=["DELETE"])
def delete_counter(name):
    """Deletes a counter"""
    global COUNTERS
    
    if name not in COUNTERS:
        return {}, status.HTTP_404_NOT_FOUND
    
    del COUNTERS[name]
    return {}, status.HTTP_200_OK