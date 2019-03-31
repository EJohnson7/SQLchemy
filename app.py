import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func, inspect

from flask import Flask, jsonify
import datetime as dt






# Create Engine
engine = create_engine("sqlite:///Resources/hawaii.sqlite", connect_args={'check_same_thread': False}, echo=True)
# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the table
Measurement = Base.classes.measurement
Station = Base.classes.station
# Create our session (link) from Python to the DB
session = Session(engine)

#################################################
# Flask Setup
#################################################
app = Flask(__name__)


#################################################
# Flask Routes
#################################################

@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Dictionary of preciptiation by date:<br/>"
        f"/api/v1.0/precipitation<br/>"

        f"Returns a JSON list of stations from the dataset:<br>"
        f"/api/v1.0/stations<br/>"

        f"Return a JSON list of Temperature Observations (tobs) for the previous year: <br/>"
        f"/api/v1.0/tobs<br/>"

        f"Return a JSON list of the minimum temperature, the average temperature, and the max temperature for a given start or start-end range: (example replace to look like: /api/v1.0/2017-01-01<br/>"
        f"/api/v1.0/<start><br/>"

        f"Return a JSON list of tmin, tmax, tavg for the dates in range of start date and end date inclusive:(example replace to look like: /api/v1.0/2017-01-01/2017-01-07)<br/>"
        f"/api/v1.0/<start>/<end><br/>"

    )


@app.route("/api/v1.0/precipitation")
def precipitation():
      # Perform a query to retrieve the data and precipitation scores
    data = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date).all()
    precipitation_dict = dict(data)

    return jsonify(precipitation_dict)

@app.route("/api/v1.0/stations")
def stations(): 
    # Query stations
    # What are the most active stations? (i.e. what stations have the most rows)?
# List the stations and the counts in descending order.
    active = session.query(Measurement.station,func.count(Measurement.station)).group_by(Measurement.station).order_by(func.count(Measurement.station).desc()).all()


    stations = list(np.ravel(active))

    return jsonify(stations_list)

@app.route("/api/v1.0/tobs")
def tobs(): 
    # Design a query to retrieve the last 12 months of precipitation data and plot the results
     query = session.query(Measurement.date).order_by(Measurement.date.desc())

    # Calculate the date 1 year ago from the last data point in the database
     last = query.first()
     last = str(last[0])
     y_ago = dt.datetime.strptime(last, "%Y-%m-%d") - dt.timedelta(days=366)

    # Perform a query to retrieve the data and precipitation scores
     data = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date > y_ago).all()

     precipitation_dict = dict(data)

     return jsonify(precipitation_dict)



@app.route("/api/v1.0/<start>")
def start(start=None):
    st = session.query(Measurement.date, func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).filter(Measurement.date >= start).group_by(Measurement.date).all()
    st_list=list(st)
    return jsonify(st_list)

    

@app.route("/api/v1.0/<start>/<end>")
def start_end(start=None, end=None):
     
    stend = session.query(Measurement.date, func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).filter(Measurement.date >= start).filter(Measurement.date <= end).group_by(Measurement.date).all()
    stend_list=list(stend)
    return jsonify(stend_list)



if __name__ == '__main__':
    app.run(debug=True)