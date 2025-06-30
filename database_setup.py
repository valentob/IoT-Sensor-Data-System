from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os

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

def add_initial_data():
    # Add default sensor types if missing
    if not SensorType.query.first():
        sensor_types = [
            SensorType(type_name="Temperature", unit="°C"),
            SensorType(type_name="Pressure", unit="hPa"),
            SensorType(type_name="Air Quality", unit="PM10"),
            SensorType(type_name="CO2", unit="ppm"),
        ]
        db.session.add_all(sensor_types)
        db.session.commit()
        print("✅ Initial sensor types added.")

    # Add a default sensor if none exist
    if not Sensor.query.first():
        default_sensor = Sensor(location_lat=41.3275, location_lon=19.8189)
        db.session.add(default_sensor)
        db.session.commit()
        print(f"✅ Default sensor added with ID {default_sensor.id}.")

    # Ensure test Pressure measurement exists
    pressure_type = SensorType.query.filter_by(type_name="Pressure").first()
    if pressure_type and not Measurement.query.filter_by(type_id=pressure_type.id).first():
        test_pressure = Measurement(
            sensor_id=1,
            timestamp="2025-03-16 18:30:00",
            type_id=pressure_type.id,
            value=1013.25
        )
        db.session.add(test_pressure)
        db.session.commit()
        print("✅ Added test Pressure data.")

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
        print(f"Database created successfully at: {db_path}")
        add_initial_data()