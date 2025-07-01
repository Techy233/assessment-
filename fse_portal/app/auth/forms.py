from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, SelectField
from wtforms.validators import DataRequired, Email, EqualTo, Length, ValidationError
from ..models import User

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=4, max=64)])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=4, max=64)])
    email = StringField('Email', validators=[DataRequired(), Email(), Length(max=120)])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=8)])
    password2 = PasswordField(
        'Repeat Password', validators=[DataRequired(), EqualTo('password', message='Passwords must match.')])
    # Role selection could be admin-only or have specific logic
    # For now, let's make it a choice, but in practice, admin would likely set roles.
    role = SelectField('Role', choices=[
        ('fse_owner', 'FSE Owner/Manager'),
        ('assessor', 'Assessor'),
        # ('admin', 'Administrator') # Admin role should likely be granted manually or by another admin
        ], validators=[DataRequired()])
    first_name = StringField('First Name', validators=[Length(max=64)])
    last_name = StringField('Last Name', validators=[Length(max=64)])
    phone_number = StringField('Phone Number', validators=[Length(max=20)]) # Add more specific validation if needed
    submit = SubmitField('Register')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Please use a different username.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Please use a different email address.')

# Optional: Form for users to update their profile
class UpdateProfileForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=4, max=64)])
    email = StringField('Email', validators=[DataRequired(), Email(), Length(max=120)])
    first_name = StringField('First Name', validators=[Length(max=64)])
    last_name = StringField('Last Name', validators=[Length(max=64)])
    phone_number = StringField('Phone Number', validators=[Length(max=20)])
    submit = SubmitField('Update Profile')

    def __init__(self, original_username, original_email, *args, **kwargs):
        super(UpdateProfileForm, self).__init__(*args, **kwargs)
        self.original_username = original_username
        self.original_email = original_email

    def validate_username(self, username):
        if username.data != self.original_username:
            user = User.query.filter_by(username=self.username.data).first()
            if user:
                raise ValidationError('This username is already taken. Please choose a different one.')

    def validate_email(self, email):
        if email.data != self.original_email:
            user = User.query.filter_by(email=self.email.data).first()
            if user:
                raise ValidationError('This email address is already registered. Please choose a different one.')

# Optional: Form for admin to edit user details (more comprehensive)
class AdminEditUserForm(UpdateProfileForm): # Inherits from UpdateProfileForm
    role = SelectField('Role', choices=[
        ('fse_owner', 'FSE Owner/Manager'),
        ('assessor', 'Assessor'),
        ('admin', 'Administrator')
        ], validators=[DataRequired()])
    is_active = BooleanField('Active Account')
    submit = SubmitField('Save Changes')

    # No need to re-validate username/email if admin is just changing role/status for existing user
    # But if admin can change username/email, then original_username/email logic is needed.
    # For simplicity, let's assume admin might change these, so we reuse the parent's validation.
    def __init__(self, original_username, original_email, *args, **kwargs):
        super(AdminEditUserForm, self).__init__(original_username, original_email, *args, **kwargs)

```

I've added `LoginForm`, `RegistrationForm`, and optional `UpdateProfileForm` and `AdminEditUserForm`. The registration form includes basic role selection for now, though this would typically be more controlled. Validators for unique username/email are included.

Next, I will update `fse_portal/app/auth/routes.py` to use these forms and implement the login, logout, and registration logic. I'll also need to create simple HTML templates for these forms.
