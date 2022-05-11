from ssl import ALERT_DESCRIPTION_DECOMPRESSION_FAILURE
from urllib import response
from app.models.cars import Car


def test_get_all_cars_with_no_return(client):
    response = client.get("/cars")
    response_body = response.get_json()

    assert response.status_code == 200
    assert response_body == []

def test_get_one_car_with_return(client, two_cars):
    response = client.get("/cars/1")
    response_body = response.get_json()
    
    # tesla= Car(driver="Jura", team="Tesla", mass_kg = 794)
    assert response.status_code == 200
    assert response_body == {
        "id": 1,
        "driver": "Jura", 
        "team": "Tesla",
        "mass_kg":794
    }
def test_get_all_cars_with_all_return(client, two_cars):
    response = client.get("/cars")
    response_body = response.get_json()

    assert response.status_code == 200
    assert len(response_body) == 2

def test_post_one_car(client):
    response = client.post('/cars', json = {
        "driver": "Alice",
        "team": "McLauren",
        "mass_kg": 900
    })
    response_body = response.get_json()
    assert response.status_code == 201
    assert "id" in response_body
    # assert "msg" in response_body

    cars = Car.query.all()
    assert len(cars) == 1
    assert cars[0].driver == "Alice"
    assert cars[0].team == "McLauren"

def test_get_car_return_404(client):
    response = client.get("/cars/1")
    assert response.status_code == 404


