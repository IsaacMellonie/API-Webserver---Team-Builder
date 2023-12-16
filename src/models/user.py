from setup import db, ma
from datetime import date
from marshmallow import fields
from marshmallow.validate import Length, Regexp, ValidationError

# User model is defined with fields for id, admin,
# captain, date_created, first, last, dob, email, 
# password, bio, available, phone, and team_id.
# All of the users' biometric data is stored here,
# along with their login details. Users can update
# their availability each week with "available".
# User phone numbers are stored in case of game
# cancellations or last minute game changes.
# The dafault team_id value is set to 1, which
# represents free agents. These free agent players
# are then assigned to a team by an admin.
# Because of the social aspect of the app,
# a bio is included where users can let others
# know a little about themselves.
class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True, nullable=False, unique=True)

    admin = db.Column(db.Boolean, default=False)
    captain = db.Column(db.Boolean, default=False)
    date_created = db.Column(db.Date(), default=date.today(), nullable=False)
    first = db.Column(db.String, default="First", nullable=False)
    last = db.Column(db.String, default="Last", nullable=False)
    dob = db.Column(db.Date)
    email = db.Column(db.String(60), nullable=False, unique=True)
    password = db.Column(db.String, nullable=False)
    bio = db.Column(db.String(200), default="Introduce yourself")
    available = db.Column(db.Boolean, default=True)
    phone = db.Column(db.Integer())

    team_id = db.Column(db.Integer, db.ForeignKey("teams.id"))
    #SQLAlchemy is used to access an instance of the Team model
    team = db.relationship("Team", back_populates="users") 


# The UserSchema is defined here.
class UserSchema(ma.Schema):
    admin = fields.Boolean()
    captain = fields.Boolean()
    date_created = fields.Date()
    first = fields.String()
    last = fields.String()
    dob = fields.Date()
    bio = fields.String()
    available = fields.Boolean()
    phone = fields.Integer()
    email = fields.Email()
    password = fields.String(validate=[Length(min=6, max=12), 
                            Regexp(r".*[A-Z].*", error="Password must contain at least one uppercase letter"),
                            Regexp(r".*[a-z].*", error="Password must contain at least one lowercase letter"),
                            Regexp(r".*[@#$%!^&+=].*", error="Password must contain at least one special character")
                            ])


    # Here the "team" db.relationship needs to be defined so that
    # marshmallow can nest the data.
    team = fields.Nested("TeamSchema", exclude=["date_created", "win", "loss", "draw"])

    
    class Meta:
        fields = ("id", "admin", "captain", "date_created",
                  "first", "last", "dob", "email", "password",
                  "bio", "available", "phone", "team")
        
