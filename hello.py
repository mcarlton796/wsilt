from flask import Flask, request, render_template
import psycopg2
import random

# Flask App
app = Flask(__name__)

# DB Connection
@app.route('/dbConnection')
def connect():
    connection = psycopg2.connect(database = "music",user = "postgres", password = "1234", host = "localhost")
    return connection

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate',methods = ['GET'])
def generate():

    random.seed()
    num = int(random.random()*10)

    # TEMPORARY CONSTRAINT
    if(num > 3):
        num = (num % 3) + 1
        print(num)

    conn = connect()

    cursor = conn.cursor()

    songStatement = str("SELECT * FROM public.songs WHERE \"songId\" = " + str(num))
    cursor.execute(songStatement)
    song = cursor.fetchall()[0]

    artistRef = song[2]
    artistStatment = str("SELECT * FROM public.artists WHERE \"artistId\" = " + str(artistRef))
    cursor.execute(artistStatment)
    artist = cursor.fetchall()[0]

    result = "You should listen to " + song[1] + " by " + artist[1]

    cursor.close()
    conn.close()

    print(result)
    return render_template('generate.html', listen = result)

if __name__ == '__main__':
    app.run(debug = True)