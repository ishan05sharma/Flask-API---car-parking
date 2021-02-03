from flask import Flask, jsonify, request
from flask_limiter.util import get_remote_address
from flask_limiter import Limiter
from dotenv import load_dotenv
import os
load_dotenv()

app = Flask(__name__)
limiter = Limiter(app, key_func=get_remote_address)

total_slots = int(os.getenv("parking_lot_size"))
parking_slots = [0] * total_slots


@app.route("/")
@limiter.limit('10/10 second')
def index():
    return jsonify({"to park": "use /park/car_number",
                    "to unpark": "use /unpark/car_number",
                    "to get information": "use info/car_number"
    
    })

@app.route('/park/<int:num>', methods = ['GET'])    
@limiter.limit('10/10 second')
def park_car(num):
    for i in range(0,total_slots):
        if parking_slots[i] == num:
            return jsonify({"car parked at": i})

    for i in range(0,total_slots):
        if parking_slots[i] == 0:
            parking_slots[i] = num
            return jsonify({'Car Number': num,
            "Parking Slot" : i,
            })
        
    return jsonify(
        {'Car Number': num,
        "Parking Slot" : "Not available, Parking is full",
    })



@app.route('/unpark/<int:num>', methods = ['GET'])
@limiter.limit('10/10 second')
def unpark_car(num):
    if num>=5:
        return "invalid slot number"
    
    if parking_slots[num] == 0:
        return jsonify({
            "parking slot" : "Already free"
        })

    for i in range(0,total_slots):
        if i+1 == num:
            parking_slots[i] = 0
            return jsonify({
            "Parking Slot freed up" : i+1,
            "car num": parking_slots[i]
            })
        
    return jsonify(
        {
        "Parking Slot" : "not found",
    })


@app.route('/info/<int:num>', methods = ['GET'])
@limiter.limit('10/10 second')
def slot_info(num):
    for i in range(0,total_slots):
        if parking_slots[i] == num:
            parking_slots[i] = 0
            return jsonify({
            "car number" : num,    
            "found on slot number" : i+1,
            })

    for i in range(0,total_slots):
        if i==num:
            parking_slots[i] = 0
            return jsonify({
            "car number" : parking_slots[i],   
            "found on slot number" : i+1,
            })
        
    return jsonify(
        {
        "Parking Slot" : "not found",
    })




if __name__ == '__main__':
    app.run(debug=True)