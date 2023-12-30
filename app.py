from flask import Flask, request
from flask import render_template
from flask import g
import sqlite3
import pynmea2

DATABASE = 'database.db'

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db

app = Flask(__name__)

with app.app_context():
    table_names = get_db().cursor().execute("SELECT name FROM sqlite_master").fetchall()
    if(len(table_names) == 0):
        print("Creating and inserting into table")
        get_db().cursor().execute("CREATE TABLE locations(id, name, latitude, longitude, temperature, humidity, pressure)")

@app.route("/")
def locations(name=None):
    return render_template('show_locations.html')

@app.route("/locs")
def locations_api():
    locations = []
    for row in get_db().cursor().execute("SELECT id, name, latitude, longitude, temperature, humidity, pressure FROM locations"):
        locations.append(
            {
                "id":row[0],
                "name":row[1],
                "location":[row[2],row[3]],
                "temperature":row[4],
                "humidity":row[5],
                "pressure":row[6],
            }
        )
    return locations

@app.route("/new_location", methods=['POST'])
def new_location():
    content=request.json
    maxid = get_db().cursor().execute("SELECT MAX(id) from locations").fetchone()
    maxid = maxid[0]
    if (maxid is None): 
        maxid = 1
    else:
        maxid +=1

    if content.get('nmea', None) is not None:
        try:
            nmea = pynmea2.parse(content['nmea'])
            print(f"nmea: {nmea}")
            print(f"longitude, latitude: {nmea.longitude}, {nmea.latitude}")
            if nmea.status == 'A':
                content['location'] = [nmea.latitude, nmea.longitude]
            else:
                return 'Error parsing request data', 400
        except:
            return 'Error parsing request data', 400

    statement = f"""
        INSERT INTO locations VALUES
            ({maxid}, '{content['name']}', {content['location'][0]}, 
            {content['location'][1]}, {content['temperature']}, 
            {content['humidity']}, {content['pressure']})
    """
    print(statement)
    get_db().cursor().execute(statement)
    get_db().commit()
    return ''
    

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()
