from flask import Flask, request, render_template
import psycopg2
import random
import configparser
from time import sleep

# Flask App
app = Flask(__name__)

# Parser
parser = configparser.ConfigParser()
try:
    parser.read('config.ini')
except configparser.Error as e:
    print(f"Error reading config file: {e}")

db = parser['DATABASE']

# DB Connection
@app.route('/dbConnection')
def connect():
    connection = psycopg2.connect(database = db['database'],
                                    user = db['user'],
                                    password = db['password'],
                                    host = db['host'],
                                    port=db['port'])
    return connection

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate',methods = ['GET'])
def generate():

    sleep(0.1)

    random.seed()
    num = int(random.random()*100)
    print(num)

    conn = connect()
    cursor = conn.cursor()
    
    cursor.execute("SELECT COUNT(*) FROM songs")
    max = cursor.fetchall()[0][0]

    # Maximum Constraint
    if(num > max):
        num = (num % max)
        print(num)

    # temporary change
    num=1
    songStatement = str("SELECT * FROM songs WHERE \"song_id\" = " + str(num))
    cursor.execute(songStatement)
    song = cursor.fetchall()
    print(song)
    song= song[0]

    artistRef = song[2]
    artistStatment = str("SELECT * FROM artists WHERE \"artist_id\" = " + str(artistRef))
    cursor.execute(artistStatment)
    artist = cursor.fetchall()[0]

    result = song[1] + " by " + artist[1]

    cursor.close()
    conn.close()

    print(result)
    return render_template('generate.html', listen = result)

if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True)