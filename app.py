from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
import datetime
import os
import sys

app = Flask(__name__)

db_path = os.path.join(os.getcwd(), "iot_data.db")
app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{db_path}"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

class Sensor(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    location_lat = db.Column(db.Float, nullable=False)
    location_lon = db.Column(db.Float, nullable=False)

class SensorType(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    type_name = db.Column(db.String(50), unique=True, nullable=False)
    unit = db.Column(db.String(10), nullable=False)

class Measurement(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    sensor_id = db.Column(db.Integer, db.ForeignKey("sensor.id"), nullable=False)
    timestamp = db.Column(db.String(50), nullable=False)
    type_id = db.Column(db.Integer, db.ForeignKey("sensor_type.id"), nullable=False)
    value = db.Column(db.Float, nullable=False)

@app.route("/")
def home():
    return "Data stored successfully!"

@app.route("/retrieve", methods=["GET"])
def retrieve_data():
    sensor_id = request.args.get("sensor_id")
    start_time = request.args.get("start_time")
    end_time = request.args.get("end_time")

    if not sensor_id or not start_time or not end_time:
        return jsonify({"error": "Missing required query parameters"}), 400

    records = Measurement.query.filter(
        Measurement.sensor_id == sensor_id,
        Measurement.timestamp >= start_time,
        Measurement.timestamp <= end_time
    ).all()

    result = {"Temperature": [], "Pressure": [], "Air Quality": [], "CO2": []}

    for record in records:
        sensor_type = SensorType.query.get(record.type_id)
        result[sensor_type.type_name].append({
            "Timestamp": record.timestamp,
            sensor_type.unit: record.value
        })
    return jsonify(result)

@app.route("/fetch", methods=["GET"])
def fetch_data():
    sensor_type = request.args.get("type")

    if not sensor_type:
        return jsonify({"error": "Sensor type parameter is required"}), 400

    sensor_type_entry = SensorType.query.filter_by(type_name=sensor_type).first()
    if not sensor_type_entry:
        return jsonify({"error": "Invalid sensor type"}), 400

    records = Measurement.query.filter_by(type_id=sensor_type_entry.id).all()
    response = "\n".join([f"{r.timestamp},{r.value}" for r in records])
    return response, 200, {"Content-Type": "text/plain"}

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 5000
    app.run(debug=True, host="0.0.0.0", port=port)