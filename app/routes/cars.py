
from flask import Blueprint, jsonify, request, make_response, abort
from app import db
from app.models.cars import Car

# we can put many different pys inside the folder routes 
# jsonify is a function

# making car class
# class Car:
#     def __init__(self, id, driver, team, mass_kg):
#         self.id = id
#         self.driver = driver
#         self.team = team
#         self.mass_kg = mass_kg

# cars = [
#     Car(7, "Sainz", "Ferrari", 795),
#     Car(88, "SHARLES", "Ferrari", 800),
#     Car(4, "Danny Ric","McLaren", 1138)
# ]

# blueprint holds information for route
#Blueprint is a class
cars_bp = Blueprint("cars", __name__, url_prefix="/cars")


# POST
@cars_bp.route("", methods = ["POST"])
def create_car():
    # request_body is a dict
    request_body = request.get_json()
    new_car = Car(
        driver_id = request_body["driver_id"],
        mass_kg = request_body["mass_kg"])
    
    # nedd the database to keep track of the car
    # db.session is the database's way of collecting changes that need to be made. Here, we are saying we want the database to add new_car.
    db.session.add(new_car)
    db.session.commit()

    # get back the id that postgres created for us 
    return {"id": new_car.id}, 201

@cars_bp.route("", methods=["GET"])
def get_all_cars():
    # params is a dictionary 
    # params = request.args.get("driver")
    # if params: 
    #     cars = Car.query.filter_by(driver = params)
    params = request.args
    # "driver": "Danny Ric",
    # "mass_kg": 1138,
    # "team": "McLaren"
    if "driver" in params and "team" in params:
        driver_name = params["driver"]
        team_name = params["team"]
        cars = Car.query.filter_by(driver = driver_name, team = team_name)
    elif "driver" in params:
        driver_name = params["driver"]
        cars = Car.query.filter_by(driver = driver_name)
    elif "team" in params:
        team_name = params["team"]
        cars = Car.query.filter_by(team = team_name)
    else:
        cars = Car.query.all()
    response = []
    for car in cars:
        response.append(car.to_dict())
    return jsonify(response)


# consider about requests coming in and response coming out
# this decorator tells about where the request coming from
# methods is a parameter
# @cars_bp.route("", methods=["GET"])
# def get_all_cars():
#     response = []
#     for car in cars:
#         response.append(
#             {
#                 "id": car.id,
#                 "driver": car.driver,
#                 "team": car.team,
#                 "mass_kg": car.mass_kg
#             }
#         )
#     return jsonify(response)

# helper_function
def get_car_or_abort(car_id):
    try:
        car_id = int(car_id)
    except ValueError:
        return make_response(jsonify({"msg":f"car id: {car_id} is invalid"})), 400
    # .get is only for using car_id
    chosen_car = Car.query.get(car_id)
    
    if chosen_car is None:
        return abort(make_response(jsonify({"msg":f"{car_id} not found"}), 404))
    return chosen_car

# get a specific car
# using <> to indicate it is a parameter
@cars_bp.route("/<car_id>", methods=["GET"])
def get_one_car(car_id):
    chosen_car = get_car_or_abort(car_id)
    rsp = {chosen_car.to_dict()}
    # for car in cars:
    #     if car.id == car_id:
    #         chosen_car = {
    #             "id": car.id,
    #             "driver": car.driver,
    #             "team": car.team,
    #             "mass_kg": car.mass_kg
    #         }
    return jsonify(rsp), 200
    
# put, replace some objects in the database
# keep the same id num
@cars_bp.route("/<car_id>", methods=["PUT"])
def place_one_car(car_id):
    chosen_car = get_car_or_abort(car_id)

    request_body = request.get_json()

    if "driver" not in request_body or "team" not in request_body or "mass_kg" not in request_body:
        return jsonify({"msg":f"Request must include all parameters except id"}), 400
    chosen_car.driver_id = request_body["driver_id"]
    chosen_car.team = request_body["team"]
    chosen_car.mass_kg = request_body["mass_kg"]

    db.session.commit()

    return jsonify({"msg":f"{car_id} updated successfully"}), 200


@cars_bp.route("/<car_id>", methods=["DELETE"])
def delete_on_car(car_id):
    chosen_car = get_car_or_abort(car_id)
    db.session.delete(chosen_car)
    db.session.commit()

    return jsonify({"msg":f"{car_id} deleted successfully"})


