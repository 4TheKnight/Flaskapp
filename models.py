from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
db = SQLAlchemy()

class User(UserMixin,db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)
    admin = db.Column(db.Boolean, nullable=False, default=False)  # New admin field

    def __repr__(self):
        return f"User('{self.username}', role='{self.role}')"


class Property(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    contact_email = db.Column(db.String(100), nullable=False)
    contact_number = db.Column(db.String(10), nullable=False)
    location = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Integer, nullable=False)
    bedrooms = db.Column(db.Integer, nullable=False)
    bathrooms = db.Column(db.Integer, nullable=False)
    carpet_area = db.Column(db.Integer, nullable=False)

    # Change to one-to-many relationship
    images = db.relationship('PropertyImage', backref='property', lazy=True)

    def __repr__(self):
        return f"<Property {self.location}>"

class PropertyImage(db.Model):
    __tablename__ = 'property_image'

    id = db.Column(db.Integer, primary_key=True)
    property_id = db.Column(db.Integer, db.ForeignKey('property.id'), nullable=False)
    image_file = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return f"<PropertyImage {self.image_file}>"