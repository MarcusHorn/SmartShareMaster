from flask import *
from peewee import *
from datetime import datetime, timedelta
import string
import random

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

class UserInfo(Model):
    id = PrimaryKeyField()
    username = TextField()
    password = TextField()
    fullname = TextField()

    class Meta:
        db_table = 'user_info'
        database = db_rentals

@app.route('/stoprental/', methods=['POST'])
def updateActiveRental():
    rental_id = request.form['rental_id']
    rental = ActiveRentals.get(ActiveRentals.id == rental_id)
    rental.delete_instance()

    return 'Ok'

# Get thee nfc code for an rental
@app.route('/getnfccode/', methods=['POST'])
def getRentalInfo():
    try:
        # TODO: Add a lot more security
        rental = ActiveRentals.get(ActiveRentals.posting == request.form['rental_id'])
        return rental.nfc_code

    except Exception as e:
        return 'Error: {}'.format(e)


@app.route('/rentals/')
def rentalsPage():
    """ Display posted rentals """
    str_output = '<b>Posted Rentals</b><br>'
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

    str_output += '<b>Active Rentals:</b><br>'
    for rental in ActiveRentals.select():
        str_output += '{}: {}, {}, {}, Paid: ${}, {}, {}km/h, {}'.format(
                    rental.id,
                    rental.posting,
                    rental.dist_travelled, 
                    rental.is_completed,
                    rental.is_paid,
                    rental.latest_loc,
                    rental.max_speed,
                    rental.nfc_code)
        str_output += '<br>'

    return str_output

def getRandomString(size=8, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


@app.route('/book/', methods=['POST'])
def bookRental():
    try:    
        rental_id = request.form['rental_id']
        rental = PostedRentals.get(PostedRentals.id == rental_id)
        
        # Car is already rented
        if not rental.is_vacant:
            return 'Not Vacant'
        
        current_time = datetime.utcnow()
        print(current_time.strftime(__datetime_frt__))

        rental.is_vacant = False

        active_rental = ActiveRentals(posting=rental.id, 
                                      dist_travelled=0,
                                      is_completed=False,
                                      is_paid=False,
                                      latest_loc=rental.location,
                                      max_speed=0,
                                      nfc_code=getRandomString())

        rental.save()
        active_rental.save()

        # Give the client their NFC code
        return active_rental.nfc_code
    except Exception as e:
        return 'Error' + str(e)

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

@app.route('/login/', methods=['POST'])
def login():
    """Mock login procedure"""
    try:

        username = request.form['username']
        password = request.form['password']

        user = UserInfo.get(UserInfo.username == username and UserInfo.password == password)
        if(user is None):
            return 'Failure!'
        
        return str(user.id)
    except:
        return 'Error'

@app.route('/updatelocation/', methods=['POST'])
def updateLocation():
    print(requests.form)
    if not 'location' in request.form:
        return 'Invalid location update!'

    rental_id = request.form['rental_id']
    rental = ActiveRentals.get(ActiveRentals.posting == rental_id)
    
    loc = request.form['location']
    loc_data = loc.split(',')
    lat = float(loc_data[0]) * 0.0166667
    lon = float(loc_data[1]) * 0.0166667
    alt = float(loc_data[2])
    heading = float(loc_data[3])

    rental.latest_loc = '{}, {}, {}, {}'.format(lat, lon, alt, heading)
    rental.save()

    return 'Ok'

"""Launch the app and make it externally visible"""
if __name__ == '__main__':
    
    db_rentals.connect()
    db_rentals.begin()

    # Remove excess whitespace from templates
    app.jinja_env.trim_blocks = True
    app.jinja_env.lstrip_blocks = True

    app.debug = True
    app.run(host='0.0.0.0', port=8080)
