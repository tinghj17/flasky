from app import db


class Driver(db.Model):
    # defining columns, add column names 
    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    name = db.Column(db.String)
    team = db.Column(db.String)
    country = db.Column(db.String)
    handsome = db.Column(db.Boolean)
    # each driver has some cars
    # Car is a class name
    # backref can be put on either side of relationship, but it is good for readability to put it on the parent side 
    # add cars to drivers, will have variable on cars called drivers 
    cars = db.relationship("Car", backref = "driver")


    def to_dict(self):
        cars_list = []
        for car in self.cars:
            cars_list.append(car.to_dict_basic())

        return {
            "id": self.id,
            "name": self.name,
            "team": self.team,
            "country": self.country,
            "handsom": self.handsome,
            "cars": cars_list
        }