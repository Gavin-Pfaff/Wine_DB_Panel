from flask import Flask, jsonify, request
from WINE_DB_FUNCT import Drink_Bottle, Undrink_Bottle, Rack_Bottle, get_wineries, Wines_by_Winery, Wines_by_Winery_var_subset, get_varietals
from flask_cors import CORS


app = Flask(__name__)
CORS(app)

@app.route('/add_wine', methods=['POST'])

def add_wine():
	data = request.json

	result = Rack_Bottle(
	data['name'], 
	data['year'], 
	data['make'], 
	**data['varietals']
	)

	return jsonify({"status": "success", "message": result})

@app.route('/drink_wine', methods=['POST'])
def drink_wine():
	data = request.json

	result = Drink_Bottle(
	data['name'],
	data['year'],
	data['make']
	)

	return jsonify({"status": "success", "message": result})




#picklist backend


@app.route('/wineries')
def pass_wineries():
	Wineries = get_wineries()
	return jsonify(Wineries)

@app.route('/varietals')
def pass_varietals():
	varietals = get_varietals()
	return jsonify(varietals)


@app.route('/dynamic_wines')
@app.route('/dynamic_wines/<winery>')
def dynamic_wines(winery=None):
	varietals_select = request.args.get('varietals','')

	if varietals_select:
		varietals_select = varietals_select.split(',')
	else:
		varietals_select = None
		
	if varietals_select == None:
		wines = Wines_by_Winery(winery)
	else:
		wines = Wines_by_Winery_var_subset(winery, varietals_select)

	return jsonify(wines)





if __name__ == '__main__':
	app.run(host='localhost', port=5000, debug=True)


