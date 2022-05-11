# use this file to create fixtures
import imp
import pytest
from app import create_app
from app import db
from flask.signals import request_finished
from app.models.cars import Car

@pytest.fixture
def app():
    app = create_app({"TESTING": True})

    @request_finished.connect_via(app)
    def expire_session(sender, response, **extra):
        db.session.remove()
    
    with app.app_context():
        db.create_all()
        yield app
    
    with app.app_context():
        db.drop_all()


@pytest.fixture
def client(app):
    return app.test_client()



@pytest.fixture
def two_cars(app):
    tesla= Car(driver="Jura", team="Tesla", mass_kg = 794)
    ferrari = Car(driver="Tanya", team="Ferrari", mass_kg = 234)

    db.session.add(tesla)
    db.session.add(ferrari)

    db.session.commit()