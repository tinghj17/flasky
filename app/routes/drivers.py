
import json
from flask import Blueprint, jsonify, request, make_response, abort
from app import db
from app.models.drivers import Driver
from app.models.cars import Car
from app.routes.cars import get_car_or_abort

# blueprint holds information for route
#Blueprint is a class
drivers_bp = Blueprint("drivers", __name__, url_prefix="/drivers")

# helper_function
def get_driver_or_abort(driver_id):
    try:
        driver_id = int(driver_id)
    except ValueError:
        abort(make_response(jsonify({"msg":f"driver id: {driver_id} is invalid"})), 400)
    # .get is only for using car_id
    chosen_driver = Driver.query.get(driver_id)
    
    if chosen_driver is None:
        abort(abort(make_response(jsonify({"msg":f"{driver_id} not found"}), 404)))
    return chosen_driver

# POST
@drivers_bp.route("", methods = ["POST"])
def create_driver():
    # request_body is a dict
    request_body = request.get_json()
    new_driver = Driver(
        name = request_body["name"],
        team = request_body["team"],
        country = request_body["country"],
        handsome = request_body["handsome"])

    db.session.add(new_driver)
    db.session.commit()

    # get back the id that postgres created for us 
    return {"id": new_driver.id}, 201

@drivers_bp.route("", methods=["GET"])
def get_all_drivers():
    response = []
    drivers = Driver.query.order_by(Driver.id).all()
    for driver in drivers:
        response.append(
            driver.to_dict()
        )
    return jsonify(response)

# get a specific car
# using <> to indicate it is a parameter
@drivers_bp.route("/<driver_id>", methods=["GET"])
def get_one_driver(driver_id):
    chosen_driver = get_driver_or_abort(driver_id)

    return jsonify(chosen_driver.to_dict()), 200

# nested route
@drivers_bp.route("<driver_id>/cars", methods = ["POST"])
def add_cars_to_driver(driver_id):
    driver = get_driver_or_abort(driver_id)
    # request_body is a dict
    request_body = request.get_json()
    try: 
        car_ids = request_body["car_ids"]
    except KeyError:
        return jsonify({"msg":"missing car_ids in request body"}), 400

    if not isinstance(request_body["car_ids"], list):
        return jsonify({"msg":"expected list of car ids"}), 400
    
    cars = []
    # request_body is a dict
    for id in car_ids:
        cars.append(get_car_or_abort(id))
    
    for car in cars:
        car.driver_id = driver_id
    
    db.session.commit()
    
    return jsonify({'msg':"Added cars to driver {driver_id}"}), 200

@drivers_bp.route("/<driver_id>", methods=["DELETE"])
def delete_one_driver(driver_id):
    chosen_driver = get_driver_or_abort(driver_id)
    
    db.session.delete(chosen_driver)
    db.session.commit()

    return jsonify({'msg': f'Deleted driver with id {driver_id}'})


@drivers_bp.route("/<driver_id>/fliphandsome", methods=["PATCH"])
def flip_driver_handsomeness_with_id(driver_id):
    driver = get_driver_or_abort(driver_id)
    driver.handsome = not driver.handsome

    db.session.commit()
    return jsonify({'msg': f'Flipped driver handsomeness with id {driver_id} to {driver.handsome}'})