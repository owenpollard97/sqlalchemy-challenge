# Import the dependencies.
import numpy as np
import sqlalchemy
import datetime as dt
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from flask import Flask, jsonify

# Python SQL toolkit and Object Relational Mapper
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.inspection import inspect
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from flask import Flask, jsonify

#Initializing Flask
#################################################


# Database Setup
#################################################


#reflect an existing database into a new model

engine = create_engine("sqlite:///db_path = "C:/BootCamp/AllHW/sqlalchemy-challenge/Starter_Code/sqlalchemy-challenge/Resources/hawaii.sqlite")

# reflect the tables

base = automap_base()
base.prepare(engine, reflect=True)
                       
# Save references to each table

measurement = Base.classes.measurement
station = Base.classes.station
                       
# Create our session (link) from Python to the DB
                       
session =Session(engine)

#################################################
# Flask Setup
#################################################

climate_app = Flask(__name__)

#Calculate the date 1 year ago from the latest date
    last_date = session.query(Measurement.date).order_by(Measurement.date.desc()).first()[0]
    one_year_ago = dt.datetime.strptime(last_date, "%Y-%m-%d") - dt.timedelta(days=365)

#Perform a query to retrieve the data and precipitation scores
    results = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date >= one_year_ago).all()


#################################################
# Flask Routes
#################################################

                       #1./ Begin at homepage and all Available Routes
   @app.route("/")           
   def welcome():
    return (
        f"Welcome to the Hawaii Climate Analysis API!<br/>"
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/start (enter as YYYY-MM-DD)<br/>"
        f"/api/v1.0/start/end (enter as YYYY-MM-DD/YYYY-MM-DD)"

    ) 

                       #2./api/v1.0/precipitation
                       #Converting my query results from precipitation analysis into a dictionary
                       #Reporting the JSON representation of the dictionary
@app.route("/api/v1.0/precipitation)
    def precipitation():
    session = Session(engine)

    one_year_ago= dt.date(2017, 8, 23)-dt.timedelta(days=365)
    latest_date = dt.date(one_year.year, one_year.month, one_year.day)

    results= session.query(measurement.date, measurement.prcp).filter(measurement.date >= prev_last_date).order_by(measurement.date.desc()).all()


    precip_dict = dict(results)
           print(f"Results for Precipitation - {precip_dict}")
    print("Out of Precipitation section.")
    return jsonify(precip_dict)
           
                          #3./api/v1.0/stations
                          #Here I return a JSON lisst of stations
 @app.route("/api/v1.0/stations")
def stations():
    # Create a session
    session = Session(engine)
    
    # Query stations data
    sel = [Station.station, Station.name, Station.latitude, Station.longitude, Station.elevation]
    query_result = session.query(*sel).all()

    # Create a list to store station data as dictionaries
    stations_list = []
    
    # Loop through the query result and format it into dictionaries
    for station, name, lat, lon, el in query_result:
        station_dict = {
            "Station": station,
            "Name": name,
            "Latitude": lat,
            "Longitude": lon,
            "Elevation": el
        }
        stations_list.append(station_dict)

    # Here I Return the JSON response
    return jsonify(stations_list)

                           #4./api/v1.0/tobs
                           #Temperature/Dates of most active station in past year
        @app.route("/api/v1.0/tobs")
def temperature_observations():
    # Establish a session with the database
    database_session = Session(engine)

# Query temperature observations for the most active station in the previous year
    most_active_station_query = database_session.query(measurement.date, measurement.tobs) \
                                                .filter(measurement.station == 'USC00519281') \
                                                .filter(measurement.date >= '2016-08-23') \
                                                .all()

    # Close the session
    database_session.close()

    # Convert query result to a list of dictionaries
    temperature_observations_list = []
    for date, temperature in most_active_station_query:
        temperature_observation = {
            "Date": date,
            "Temperature": temperature
        }
        temperature_observations_list.append(temperature_observation)

    # Return the temperature observations as JSON
    return jsonify(temperature_observations_list) 
           
                                     #5. /api/v1.0/<start> and /api/v1.0/<start>/<end>
           
   @app.route("/api/v1.0/<start_date>")
def get_temperatures_start(start_date):
    # Start a session with the database
    db_session = Session(engine)
    
    # Query minimum, average, and maximum temperatures starting from the provided start date
    temperature_results = db_session.query(func.min(Measurement.tobs),
                                            func.avg(Measurement.tobs),
                                            func.max(Measurement.tobs)) \
                                     .filter(Measurement.date >= start_date) \
                                     .all()
    
    # Close the database session
    db_session.close()
    
    # Format the temperature results into a list of dictionaries
    temperature_list = []
    for min_temp, avg_temp, max_temp in temperature_results:
        temperature_dict = {
            "Minimum Temperature": min_temp,
            "Average Temperature": avg_temp,
            "Maximum Temperature": max_temp
        }
        temperature_list.append(temperature_dict)
    
    # Return the temperature results as JSON
    return jsonify(temperature_list)


@app.route("/api/v1.0/<start_date>/<end_date>")
def get_temperatures_start_end(start_date, end_date):
    # Start a session with the database
    db_session = Session(engine)
    
    # Query minimum, average, and maximum temperatures within the provided date range
    temperature_results = db_session.query(func.min(Measurement.tobs),
                                            func.avg(Measurement.tobs),
                                            func.max(Measurement.tobs)) \
                                     .filter(Measurement.date >= start_date) \
                                     .filter(Measurement.date <= end_date) \
                                     .all()
    
    # Close the session
    db_session.close()
    
    # Format the results into a list of dictionaries
    temperature_list = []
    for min_temp, avg_temp, max_temp in temperature_results:
        temperature_dict = {
            "Minimum Temperature": min_temp,
            "Average Temperature": avg_temp,
            "Maximum Temperature": max_temp
        }
        temperature_list.append(temperature_dict)
    
    # Return the temperature results as JSON
    return jsonify(temperature_list)