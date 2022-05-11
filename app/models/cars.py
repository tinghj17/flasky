from app import db


#sqlalchemy will use the following code to figure out the table 
# use this class to create the table. will use sqlalchemy syntax
class Car(db.Model):
    # defining columns, add column names 
    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    driver_id = db.Column(db.Integer, db.ForeignKey('driver.id'))
    # driver = db.Column(db.String)
    # team = db.Column(db.String)
    mass_kg = db.Column(db.Integer)
    # one to many relationship
    # driver = db.relationship("Driver", backref = "cars")

    def to_dict(self):
        return {
            "id": self.id,
            "driver": self.driver.name,
            "team": self.driver.team,
            "mass_kg": self.mass_kg
            }
    
    def to_dict_basic(self):
        return {
            "id": self.id,
            "mass_kg": self.mass_kg
        }



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