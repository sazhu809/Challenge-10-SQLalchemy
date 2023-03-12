import numpy as np
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from flask import Flask, jsonify

# Database Setup
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine=engine, reflect=True)

# Save references to each table
measurement = Base.classes.measurement
station = Base.classes.station

# Flask Setup
app = Flask(__name__)


first_day = '2016-08-23'
last_day = '2017-08-23'


# Flask Routes
@app.route("/")
def welcome():
    
    return (
        '<style type="text/css">'

        'body {'
            'font-family: Arial, sans-serif;'
            'text-align: center;'
        '}'
        '</style>'
        f"<h1>Welcome to the Climate App</h1><br/>"
        f"<h3>Below are the available APIs</h3><br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/YYYY-MM-DD<br/>"
        f"/api/v1.0/YYYY-MM-DD/YYYY-MM-DD<br/>"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    session = Session(engine)

    # Querying Measurement 
    results = session.query(measurement.date, measurement.prcp).filter(measurement.date >= last_day).order_by(measurement.date).all()

    session.close()

    # Dictionary 
    temp_list = []
    for date, prcp in results:
        dict = {}
        dict['date'] = date
        dict['precipitation'] = prcp
        temp_list.append(dict)

    return jsonify(temp_list)

@app.route('/api/v1.0/stations')
def stations():

    session = Session(engine)

    # Query stations
    results = session.query(station.name).all()

    session.close()

    # Turn to list
    station_list = list(np.ravel(results))

    return jsonify(station_list)

@app.route('/api/v1.0/tobs')
def tobs():
    session = Session(engine)

    # Query Stations
    results = session.query(measurement.tobs).\
        filter(measurement.station == 'USC00519281').\
        filter(measurement.date >= first_day).\
        order_by(measurement.date).all()

    session.close()

    # List
    tobs_list = list(np.ravel(results))

    return jsonify(tobs_list)

@app.route("/api/v1.0/<start_date>")
def Start_date(start):
    session = Session(engine)

    # Query tobs
    results = session.query(func.min(measurement.tobs), func.avg(measurement.tobs), func.max(measurement.tobs)).filter(measurement.date >= start).all()

    session.close()

    # Create a dictionary 
    stat_tobs = []
    for min, avg, max in results:
        stat_dict = {}
        stat_dict["min_temp"] = min
        stat_dict["avg_temp"] = avg
        stat_dict["max_temp"] = max
        stat_dict.append(stat_dict) 
    return jsonify(stat_tobs)

@app.route("/api/v1.0/<start_date>/<end_date>")
def Start_end_date(start_date, end_date):
    session = Session(engine)

    # Query tobs
    results = session.query(func.min(measurement.tobs), func.avg(measurement.tobs), func.max(measurement.tobs)).filter(measurement.date >= start_date).filter(measurement.date <= end_date).all()

    session.close()
  
    # Create a dictionary 
    end_stat_tobs = []
    for min, avg, max in results:
        end_tobs_dict = {}
        end_tobs_dict["min_temp"] = min
        end_tobs_dict["avg_temp"] = avg
        end_tobs_dict["max_temp"] = max
        end_stat_tobs.append(end_tobs_dict) 
    

    return jsonify(end_stat_tobs)


if __name__ == '__main__':
    app.run(debug=True)