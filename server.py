from flask import *
from peewee import *

app = Flask(__name__)

db_rentals = SqliteDatabase('db/rentals.db')
__datetime_frt__ = '%Y-%m-%d %H:%M:%S'

class PostedRentals(Model):
    id = PrimaryKeyField()
    car_info = TextField(null=True)
    dt_begin = TextField()
    dt_end = TextField(null=True)
    is_vacant = IntegerField()
    location = TextField() # lat,long,altitude,heading
    price = FloatField()
    user_key = IntegerField()

    class Meta:
        db_table = 'posted_rentals'
        database = db_rentals

class ActiveRentals(Model):
    id = PrimaryKeyField()
    posting = IntegerField()    
    dist_travelled = FloatField(null=True)
    is_completed = IntegerField()
    is_paid = IntegerField()
    latest_loc = TextField()
    max_speed = FloatField(null=True)
    nfc_code = TextField()

    class Meta:
        db_table = 'active_rentals'
        database = db_rentals

@app.route('/deleterental/', methods=['POST'])
def rmRental():
    try:
        user_key = request.form['user_key']
        rentals = PostedRentals.select().where(PostedRentals.user_key == user_key)
        print(len(rentals))
        for rental in rentals:
            rental.delete_instance()

    except Exception as e:

        print(e)
        return 'Error occured'


@app.route('/addrental/', methods=['POST'])
def addRental():
    """ Add a rental to the database"""
    try:
        print(request.form)
        new_rental = PostedRentals(car_info=request.form['car_info'],
                                dt_begin=request.form['dt_begin'],
                                dt_end=request.form['dt_end'],
                                is_vacant=True,
                                location=request.form['location'],
                                price=float(request.form['price']),
                                user_key=int(request.form['user_key']))
        
        new_rental.save()
        return 'Succesfully added a new rental!'
    except Exception as e:
        print(e)
        return 'Error occured'

@app.route('/book/', methods=['POST'])
def bookRental():


    return 'Hi'

@app.route('/rentals/')
def rentalsPage():
    """ Display rentals """
    str_output = ''
    for rental in PostedRentals.select():
        str_output += '{}: {}, Available from {} to {}, {}, {}, ${}, {}'.format(
                        rental.id,
                        rental.car_info,
                        rental.dt_begin, 
                        rental.dt_end,
                        rental.is_vacant,
                        rental.location,
                        rental.price,
                        rental.user_key)
        str_output += '<br>'

    return str_output

@app.route('/updatelocation/', methods=['POST'])
def updateLocation():
    if not 'location' in request.form:
        return 'Invalid location update!'

    loc = request.form['location']
    loc_data = loc.split(',')
    lat = float(loc_data[0])
    lon = float(loc_data[1])


    return str(loc_data) + '\n'


"""Launch the app and make it externally visible"""
if __name__ == '__main__':
    
    db_rentals.connect()
    db_rentals.begin()

    # Remove excess whitespace from templates
    app.jinja_env.trim_blocks = True
    app.jinja_env.lstrip_blocks = True

    app.debug = True
    app.run(host='0.0.0.0', port=8080)
