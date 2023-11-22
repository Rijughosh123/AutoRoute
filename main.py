from tokenize import Single
import configparser, mysql.connector, json, logging
from flask import Flask, render_template, request, jsonify
from flask_restful import Resource, Api, reqparse
from flask_httpauth import HTTPBasicAuth
from views.routing_algo import AutoRouteAlgo
from views.autorote_or_tools import AutorouteOR


from dotenv import load_dotenv
load_dotenv(verbose=True)

config = configparser.ConfigParser()
config.read('env.conf')

environment = config.get('Environment', 'mode')
host = str(config.get('Environment', 'host'))
port = int(config.get('Environment', 'port'))
debug = False if config.get('Environment', 'debug') == '0' else True

Config = config._sections[environment]


app = Flask(__name__, template_folder='./templates')
api = Api(app, prefix="/api/v1")
auth = HTTPBasicAuth()

# Configure the logging module
log_file = 'error.log'
logging.basicConfig(filename=log_file, level=logging.ERROR)

@app.errorhandler(Exception)
def handle_error(error):
    # Log the error to the configured log file
    logging.error("An error occurred: %s", str(error))

    # You can also log the request information, including the URL and method
    logging.error("Request URL: %s", request.url)
    logging.error("Request Method: %s", request.method)

    # Return a custom error response
    response = jsonify({'error': 'An unexpected error occurred'})
    response.status_code = 500
    return response

def getConnection():
    config = {
        'host': '127.0.0.1',
        'user': 'root',
        'password': 'Pa$$W0rD&2022',
        'database': 'bokakyltransport'
    }
    mydb = mysql.connector.connect(**config)
    return mydb

@app.route('/')
def home():
    # print('asasd')
    return render_template('index.html')

USER_DATA = {
    "admin": "SuperSecretPwd"
}

@auth.verify_password
def verify(username, password):
    if not (username and password):
        return False
    return USER_DATA.get(username) == password



def create_data_model_time(list_id):
    """Stores the data for the problem."""
    data = {}
    mydb = getConnection()
    mycursor = mydb.cursor()
    mycursor = mydb.cursor( buffered=True , dictionary=True)
    mycursor.execute("SELECT * FROM autoroute_list where id = "+format(list_id))
    myresult = mycursor.fetchone()
    data['delivery_type_status'] = myresult["delivery_type_status"]
    data['calculate_driver_starting_time'] = myresult["calculate_driver_starting_time"]

    row_count = mycursor.rowcount
    if row_count == 0:
        return 0
    start_end_time = myresult["start_end_time"]
    start_end_time_arr = start_end_time.split('-')
    hour_list = []
    for time_string in start_end_time_arr:
        hours, minutes = map(int, time_string.split(':'))
        minutes_since_midnight = (hours * 60) + minutes
        hour_list.append(minutes_since_midnight)

    distt = myresult["time_matrix"]
    times = json.loads(distt)
    data['time_matrix'] = times
    if myresult["working_hours"] != None:
        working_hours, working_minutes = map(int, myresult["working_hours"].split(':'))
        total_working_hours_in_minutes = working_hours * 60 + working_minutes
        data['working_hours'] = total_working_hours_in_minutes
    else:
        data['working_hours'] = 525
    if myresult["break_time"] != None:
        data['break_time'] = int(myresult["break_time"])
    else:
        data['break_time'] = 30

    if myresult["break_after_x_hours"] != None:
        try:
            if ':' in val:
                hours, minutes = map(int, str(myresult["break_after_x_hours"]).split(':'))
                break_after_time = hours * 60 + minutes
            else:
                break_after_time = int(val)*60

            data['break_after_time'] = int(break_after_time)
        except:
            data['break_after_time'] = 300
    else:
        data['break_after_time'] = 300

    
    mycursor.execute("SELECT * FROM autoroutes_addresses where list_id = "+format(list_id)+" ORDER BY address_id ASC")
    myres = mycursor.fetchall()
    row_count = mycursor.rowcount
    depot = row_count-1
    time_windows=[]
    for res in myres:
        time = res["delivery_type"]
        # print(time)
        tAr = time.split('-')
        # print("tAr",tAr)
        for i in range(len(tAr)):
            n_tAr = tAr[i].split(":")
            n_tAr = [int(k) for k in n_tAr]
            val = sum(n_tAr)
            tAr[i] = val
        ntAr=[]
        start_diff = abs(int(hour_list[0])-int(tAr[0]*60))
        end_diff = abs(int(hour_list[0])-int(tAr[1]*60))
        ntAr.append(start_diff)
        ntAr.append(end_diff)
        time_windows.append(ntAr)
    data['time_windows'] = time_windows
    data['num_vehicles'] = 35
    data['depot'] = depot
    data['hour_list'] = hour_list
    
    mycursor.close()
    mydb.close()
    return data





class new_route_plan_with_break(Resource):
    # @auth.login_required
    def get(self):
        try:
            parser = reqparse.RequestParser()  # initialize parser
            parser.add_argument('list_id', required=True, type=int)   
            args = parser.parse_args()  # parse arguments to dictionary
            listId = args['list_id']
            data = create_data_model_time(listId)
            if(data == 0):
                return {'res': "no-data"}, 200
            if int(data['delivery_type_status']) == 1:
                res = AutorouteOR(data) 
                return res, 200
            else:
                res = AutoRouteAlgo(data)
                return res, 200
        except:
            return {'res': "no-data"}, 200


api.add_resource(new_route_plan_with_break, '/new_route_plan/with_break')



    
if __name__ == "__main__":
    # Specify the path to the SSL certificate and key files
    # ssl_cert = 'keys/fullchain.txt'
    # ssl_key = 'keys/privkey.txt'
    
    # Set the host and port
    host = '0.0.0.0'  # Listen on all network interfaces
    port = 8001
   
    # Start the Flask application with SSL
    app.run(host=host, port=port, debug=True)

    

# from flask import Flask, render_template, request, jsonify
# app = Flask(__name__)
# @app.route('/')
# def hello_world():
#     return 'Hello World'
 
# # main driver function
# if __name__ == '__main__':
#     host = '0.0.0.0'  # Listen on all network interfaces
#     port = 8001
#     app.run(host=host, port=port, debug=True)
