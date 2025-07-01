from . import db # '.': current package, __init__.py should define 'db'
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from datetime import datetime, timezone

# Association table for FSEs and multiple owners (if an FSE can have multiple registered owner users)
# For now, assuming one primary owner_id on FSE table is sufficient.
# If many-to-many is needed for FSE owners:
# fse_owners_association = db.Table('fse_owners_association',
#     db.Column('user_id', db.Integer, db.ForeignKey('users.id'), primary_key=True),
#     db.Column('fse_id', db.Integer, db.ForeignKey('fses.id'), primary_key=True)
# )

class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False, index=True)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(256), nullable=False)
    role = db.Column(db.String(20), nullable=False, default='fse_owner') # Roles: 'assessor', 'fse_owner', 'admin'

    first_name = db.Column(db.String(64), nullable=True)
    last_name = db.Column(db.String(64), nullable=True)
    phone_number = db.Column(db.String(20), nullable=True)
    is_active = db.Column(db.Boolean, default=True) # For soft deletes or deactivation by admin
    date_created = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    last_login = db.Column(db.DateTime, nullable=True)

    # Relationships
    # For an FSE Owner user owning multiple FSEs (one-to-many from User to FSE)
    fses_owned = db.relationship('FSE', backref='owner_user', lazy='dynamic', foreign_keys='FSE.owner_id')

    # For an Assessor user conducting multiple Assessments (one-to-many from User to Assessment)
    assessments_conducted = db.relationship('Assessment', backref='assessor_user', lazy='dynamic', foreign_keys='Assessment.assessor_id')

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    @property
    def full_name(self):
        if self.first_name and self.last_name:
            return f"{self.first_name} {self.last_name}"
        return self.username

    def __repr__(self):
        return f'<User {self.username} ({self.role})>'

class FSE(db.Model): # Food Service Establishment
    __tablename__ = 'fses'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False, index=True)
    location_address = db.Column(db.String(250), nullable=False) # More descriptive name
    # Primary contact person at the FSE (might not be the 'User' owner)
    primary_contact_name = db.Column(db.String(100), nullable=True)
    primary_contact_phone = db.Column(db.String(20), nullable=True)
    primary_contact_email = db.Column(db.String(120), nullable=True)

    date_registered_in_system = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    # Link to the FSE Owner/Manager (User with 'fse_owner' role)
    owner_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True) # Nullable if Admin can create FSEs before assigning an owner

    # Relationships
    assessments = db.relationship('Assessment', backref='fse', lazy='dynamic', foreign_keys='Assessment.fse_id', cascade="all, delete-orphan")

    def __repr__(self):
        return f'<FSE ID: {self.id} - {self.name}>'

class Assessment(db.Model):
    __tablename__ = 'assessments'
    id = db.Column(db.Integer, primary_key=True)
    assessment_date = db.Column(db.DateTime, nullable=False, default=lambda: datetime.now(timezone.utc), index=True)

    fse_id = db.Column(db.Integer, db.ForeignKey('fses.id'), nullable=False)
    assessor_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False) # User with 'assessor' role

    total_score = db.Column(db.Integer, nullable=True)
    star_rating = db.Column(db.Integer, nullable=True)

    # Part 1: Background Information
    # Example fields if we don't use JSON. Using specific fields is better for querying.
    assessment_background_assessor_name_capture = db.Column(db.String(100), nullable=True) # Name of assessor as captured at time of assessment
    assessment_background_fse_type_capture = db.Column(db.String(100), nullable=True) # FSE Type as captured
    # If you have many such fields, JSON might be okay, or a separate related table for background key-value pairs.
    # background_info_json = db.Column(db.Text, nullable=True) # Alternative

    # Relationships
    scores = db.relationship('AssessmentScore', backref='assessment', lazy='dynamic', cascade="all, delete-orphan")

    def __repr__(self):
        return f'<Assessment ID {self.id} for FSE ID {self.fse_id} on {self.assessment_date.strftime("%Y-%m-%d")}>'

class ChecklistPart(db.Model):
    __tablename__ = 'checklist_parts'
    id = db.Column(db.Integer, primary_key=True)
    # Using a code might be useful if names change but logic relies on a stable identifier
    # part_code = db.Column(db.String(50), unique=True, nullable=False)
    part_name = db.Column(db.String(255), unique=True, nullable=False)
    max_score = db.Column(db.Integer, nullable=False)
    description = db.Column(db.Text, nullable=True)
    order = db.Column(db.Integer, default=0) # For displaying checklist parts in a specific order

    def __repr__(self):
        return f'<ChecklistPart ID {self.id} - {self.part_name}>'

class AssessmentScore(db.Model):
    __tablename__ = 'assessment_scores'
    id = db.Column(db.Integer, primary_key=True)
    assessment_id = db.Column(db.Integer, db.ForeignKey('assessments.id'), nullable=False)
    checklist_part_id = db.Column(db.Integer, db.ForeignKey('checklist_parts.id'), nullable=False)
    score = db.Column(db.Integer, nullable=False)

    # Relationship to easily get details of the checklist part
    checklist_part = db.relationship('ChecklistPart')

    # Unique constraint to ensure a part is scored only once per assessment
    __table_args__ = (db.UniqueConstraint('assessment_id', 'checklist_part_id', name='_assessment_part_uc'),)

    def __repr__(self):
        return f'<AssessmentScore for Assessment ID {self.assessment_id} - Part ID {self.checklist_part_id}: {self.score}>'

# Utility function to be called from __init__.py or a setup script
# This is moved to __init__.py to be within app_context
# def seed_checklist_parts(db_instance):
#     if ChecklistPart.query.count() == 0:
#         parts_data = [
#             {"part_name": "Part 2: Documentations", "max_score": 20, "description": "Hygiene Certificate of food handlers, Business Operating Permit, Suitability Permit, Hygiene Permit", "order": 1},
#             {"part_name": "Part 3: Personal Hygiene of Food handlers", "max_score": 20, "description": "Assessment of personal hygiene practices.", "order": 2},
#             {"part_name": "Part 4: Material sourcing", "max_score": 20, "description": "Verification of material sources and quality.", "order": 3},
#             {"part_name": "Part 5: Water Sources and Storage", "max_score": 10, "description": "Assessment of water sources and storage practices.", "order": 4},
#             {"part_name": "Part 6: Waste Disposal", "max_score": 20, "description": "Evaluation of waste disposal methods and compliance.", "order": 5},
#             {"part_name": "Part 7: Cleaning", "max_score": 10, "description": "Assessment of cleaning procedures and schedules.", "order": 6}
#         ]
#         for part_data in parts_data:
#             part = ChecklistPart(**part_data)
#             db_instance.session.add(part)
#         db_instance.session.commit()
#         print("Checklist parts seeded.")
#     else:
#         print("Checklist parts already exist or seeding is handled elsewhere.")
