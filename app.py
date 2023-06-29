# Import the dependencies.
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
import pandas as pd
import datetime as dt
import numpy as np



#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()

# reflect the tables
Base.prepare(autoload_with=engine)
Base.classes.keys()

# Save references to each table
measurements = Base.classes.measurement
station = Base.classes.station

# Create our session (link) from Python to the DB
session = Session(engine)

#################################################
# Flask Setup
#################################################

#import Flask and jsonify
from flask import Flask, jsonify

app = Flask(__name__)



#################################################
# Flask Routes
#################################################
@app.route("/")
def home():
    """List all available routes"""
    return (
        f"Precipitation"
        f"Stations"
        f"Tobs"
        f"Start"
        f"Start_end"
    )

#################################################
@app.routes("/api/v1.0/precipitation")
def precipitation():
    most_recent_date = session.query(measurements.date).order_by(measurements.date.desc()).first().date
    year_ago = dt.date(2017,8,23) - dt.timedelta(days= 365)
    year_prcp = session.query(measurements.date, measurements.prcp).\
        filter(measurements.date >= year_ago, measurements.prcp != None).\
        order_by(measurements.date).all()

#################################################
@app.routes("/api/v1.0/stations")
def stations():
    stations_query = session.query(station.name, station.station)
    stations = pd.read_sql(stations_query.statement, stations_query.session.bind)
    return jsonify(stations.to_dict())

#################################################
@app.routes("/api/v1.0/tobs")
def tobs():
    most_recent_date = session.query(measurements.date).order_by(measurements.date.desc()).first().date
    year_ago = dt.date(2017,8,23) - dt.timedelta(days= 365)
    temperature = session.query(measurements.date, measurements.tobs).filter(measurements.date > year_ago).\
        order_by(measurements.date).all()

#################################################
@app.routes("/api/v1.0/<start>")
def start():
    start_date= dt.datetime.strptime(start, '%Y-%m-%d')
    last_year = dt.timedelta(days=365)
    start = start_date-last_year
    end =  dt.date(2017, 8, 23)
    trip_data = session.query(func.min(measurements.tobs), func.avg(measurements.tobs), func.max(measurements.tobs)).\
        filter(measurements.date >= start).filter(measurements.date <= end).all()
    trip = list(np.ravel(trip_data))
    return jsonify(trip)
#################################################
@app.routes("/api/v1.0/<start>/<end>")
def start_end():
    start_date= dt.datetime.strptime(start, '%Y-%m-%d')
    end_date= dt.datetime.strptime(end,'%Y-%m-%d')
    last_year = dt.timedelta(days=365)
    start = start_date-last_year
    end = end_date-last_year
    trip_data = session.query(func.min(measurements.tobs), func.avg(measurements.tobs), func.max(measurements.tobs)).\
        filter(measurements.date >= start).filter(measurements.date <= end).all()
    trip = list(np.ravel(trip_data))
    return jsonify(trip)