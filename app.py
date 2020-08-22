from flask import Flask, jsonify
import numpy as np
import pandas as pd
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

engine = create_engine("sqlite:///Resources/hawaii.sqlite")
connection = engine.connect()

Base = automap_base()
Base.prepare(engine, reflect=True)

measurement = Base.classes.measurement
station = Base.classes.station

app = Flask(__name__)

@app.route("/")
def index():
    return (
        f"WELCOME!<br/>"
        f"<br/>"
        f"AVAILABLE ROUTES:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>" 
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/choose_start_date<br/>"
        f"/api/v1.0/choose_start_date/choose_end_date" 
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    session = Session(engine)
    results = session.query(measurement.date, measurement.prcp).all()
    session.close()

    date_prcp = []
    for date, prcp in results:
        date_precip_dict = {}
        date_precip_dict["date"] = date
        date_precip_dict["prcp"] = prcp
        date_prcp.append(date_precip_dict)
    
    return jsonify(date_prcp)

@app.route("/api/v1.0/stations")
def stations():
    session = Session(engine)
    results = session.query(station.station, station.name).all()
    session.close()
  
    return jsonify(results)

@app.route("/api/v1.0/tobs")
def tobs():
    session = Session(engine)
    tobs_results = session.query(measurement.tobs, measurement.date).\
            filter(measurement.date >='2016-08-23').\
            filter(measurement.station == 'USC00519281').all()
    session.close()
    all_tobs = list(np.ravel(tobs_results))

    return jsonify(all_tobs)
    

@app.route("/api/v1.0/<start>")
def start_date(start):
    session = Session(engine)
    search_start = session.query(func.min(measurement.tobs), func.avg(measurement.tobs), func.max(measurement.tobs)).\
            filter(measurement.date >= start).all()
    temp_summary = list(np.ravel(search_start))
    session.close()

    return jsonify(temp_summary)


@app.route("/api/v1.0/<start>/<end>")
def start_end_date(start, end):
    session = Session(engine)

    search_start_end = session.query(func.min(measurement.tobs), func.avg(measurement.tobs), func.max(measurement.tobs)).\
            filter(measurement.date >= start).filter(measurement.date < end).all()
    temp_summary = list(np.ravel(search_start_end))
    session.close()

    return jsonify(temp_summary)

if __name__ == "__main__":
    app.run(debug=True)