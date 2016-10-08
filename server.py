from flask import *
from peewee import *

app = Flask(__name__) #, static_folder='static', template_folder='.')

db_rentals = SqliteDatabase('db/rentals.db')
__datetime_frt__ = '%Y-%m-%d %H:%M:%S'

class PostedRentals(Model):
    car_info = TextField(null=True)
    dt_begin = TextField()
    dt_end = TextField(null=True)
    is_vacant = IntegerField()
    location = TextField() # lat,long,altitude,heading
    price = FloatField()

    class Meta:
        db_table = 'posted_rentals'
        database = db_rentals

class ActiveRentals(Model):
    dist_travelled = FloatField(null=True)
    is_completed = IntegerField()
    is_paid = IntegerField()
    latest_loc = TextField()
    max_speed = FloatField(null=True)
    nfc_code = TextField()

    class Meta:
        db_table = 'active_rentals'
        database = db_rentals

@app.route('/rentals/')
def landing_page():
    for rental in PostedRentals.select():
        print(1)

    return "It worked!"

"""Launch the app and make it externally visible"""
if __name__ == '__main__':
    
    db_rentals.connect()
    db_rentals.begin()

    # Remove excess whitespace from templates
    app.jinja_env.trim_blocks = True
    app.jinja_env.lstrip_blocks = True

    app.debug = True
    app.run(host='0.0.0.0', port=8080)
