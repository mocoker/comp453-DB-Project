from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from flask_login import current_user
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField, DecimalField, IntegerField, DateField, SelectField, HiddenField, DecimalField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError,Regexp
#from wtforms.ext.sqlalchemy.fields import QuerySelectField
from flaskDemo import db
from flaskDemo.models import User, Employee, Donor, Supply_Record, Blood_Donation
#from wtforms.fields.html5 import DateField


#***********************************************************************************************************
#QUERIES BELOW ARE FOR DROP DOWN MENU PURPOSE

# Dropdown choice for blood group
bloodGroupChoice = ['select option', 'A', 'B', 'AB', 'O']

# Dropdown choice for sex
sexChoice = ['select option', 'Male', 'Female']

# Dropdown choice for blood test result
testChoice = ['select option', 'Positive', 'Negative']

# Dropdown choice for inventory status
statusChoice = ['select option', 'In Stock', 'To be disposed of']

# Dropdown for blood test comclusion
conclusionChoice = ['select option', 'All test passed - Good for supply','One, more test failed - Not good for supply']

# Dropdown to list names of helath care facilities
getHealthFacilityNames = ['select option', 'Advocate Aurora Health', 'Amita Health', 'BJC HealthCare', 'Cancer Treatment Centers of America',
        'Cook County Health and Hospitals System', 'Chicago Lakeshore Hospital', 'Decatur Memorial Hospital', 'Fairfield Memorial Hospital',
        'Genesis Health System', 'Graham Health System', 'Hamilton Memorial Hospital', 'Hartgrove Hospital', 'Iroquois Memorial Hospital',
        'Kindred Healthcare', 'Lawrence County Memorial Hospital', 'Midwest Medical Center']

# Query the database to list donor email
getDonorEmail = Donor.query.with_entities(Donor.Donor_Email).distinct().order_by(Donor.Donor_ID)
result2=list()
for row in getDonorEmail:
    rowDict=row._asdict()
    result2.append(rowDict)
myChoice2 = [(row['Donor_Email'],row['Donor_Email']) for row in result2]

#***********************************************************************************************************

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('That username is taken. Please choose a different one.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('That email is taken. Please choose a different one.')


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')


class UpdateAccountForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    picture = FileField('Update Profile Picture', validators=[FileAllowed(['jpg', 'png'])])
    submit = SubmitField('Update')

    def validate_username(self, username):
        if username.data != current_user.username:
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError('That username is taken. Please choose a different one.')

    def validate_email(self, email):
        if email.data != current_user.email:
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError('That email is taken. Please choose a different one.')


#***********************************************************************************************************

# *** Form to Add Employee ***
class AddEmployee(FlaskForm):
    Employee_Email = StringField("E-Mail", validators=[DataRequired(), Email()])
    First_Name = StringField("First Name", validators=[DataRequired(), Length(max=30)])
    Last_Name = StringField("Last Name", validators=[DataRequired(), Length(max=30)])
    Employee_Address = StringField("Address", validators=[DataRequired(), Length(max=60)])
    Employee_Phone_Number = IntegerField("Phone Number", validators=[DataRequired()])
    Employee_Designation = StringField("Designation", validators=[DataRequired(), Length(max=40)])
    submit = SubmitField('Add Employee')

    def validate_Employee_Email(self, Employee_Email):                                        # email must be unique
        empEmail = Employee.query.filter_by(Employee_Email=Employee_Email.data).first()
        if empEmail:
            raise ValidationError('That email address is already being used. Please choose a different email.')

#***********************************************************************************************************

# *** Form to Add Donor ***
class AddDonor(FlaskForm):
    First_Name = StringField("First Name", validators=[DataRequired(), Length(max=30)])
    Last_Name = StringField("Last Name", validators=[DataRequired(), Length(max=30)])
    Donor_Address = StringField("Address", validators=[DataRequired(), Length(max=60)])
    Donor_Phone_Number = IntegerField("Phone Number", validators=[DataRequired()])
    Donor_Email = StringField("E-Mail", validators=[DataRequired(), Email()])
    Donor_Blood_Group = SelectField("Blood Group", validators=[DataRequired()], choices=bloodGroupChoice)
    Donor_Medical_Report = TextAreaField("Medical Report", validators=[DataRequired(), Length(max=500)])
    Sex = SelectField("Sex", validators=[DataRequired()], choices=sexChoice)
    Birth_Date = DateField ("Date of Birth", format='%Y-%m-%d', validators=[DataRequired()])
    submit = SubmitField('Add Blood Donor')

    def validate_Donor_Email(self, Donor_Email):                                        # email must be unique
        dEmail = Donor.query.filter_by(Donor_Email=Donor_Email.data).first()
        if dEmail:
            raise ValidationError('That email address is already being used. Please choose a different email.')

#***********************************************************************************************************

# *** Form to Add Supply Record ***
class AddSupplyRecord(FlaskForm):
    Health_Facility_Name = SelectField("Health Facility Name", validators=[DataRequired()], choices=getHealthFacilityNames)
    Blood_Group = SelectField("Blood Group", validators=[DataRequired()], choices=bloodGroupChoice)
    Quantity_Supplied = IntegerField("Quantity Supplied", validators=[DataRequired()])
    Date_of_Supply = DateField ("Date of Supply", format='%Y-%m-%d', validators=[DataRequired()])
    submit = SubmitField('Add Supply Record')

#***********************************************************************************************************

# *** Form to Add Blood Donation ***
class AddBloodDonation(FlaskForm):
    Donor_Email = SelectField("Donor Email", validators=[DataRequired()], choices=myChoice2)                #To get donor ID from Donor table
    Date_of_Donation = DateField ("Date of Donation", format='%Y-%m-%d', validators=[DataRequired()])
    Hepatitis_B = SelectField("Hepatitis B Test", validators=[DataRequired()], choices=testChoice)
    Hepatitis_C = SelectField("Hepatitis C Test", validators=[DataRequired()], choices=testChoice)
    HIV = SelectField("HIV Test", validators=[DataRequired()], choices=testChoice)
    Syphilis = SelectField("Syphilis Test", validators=[DataRequired()], choices=testChoice)
    Zika_Virus = SelectField("Zika Virus Test", validators=[DataRequired()], choices=testChoice)
    West_Nile_Virus = SelectField("West Nile Virus Test", validators=[DataRequired()], choices=testChoice)
    Blood_Test_Conclusion = SelectField("Blood Test Conclusion", validators=[DataRequired()], choices=conclusionChoice)
    Inventory_Status = SelectField("Status", validators=[DataRequired()], choices=statusChoice)
    submit = SubmitField('Add Blood Donation')

#***********************************************************************************************************

# *** Form to Update Blood Donation ***
class UpdateBloodDonation(FlaskForm):
    Donation_ID = IntegerField("Blood Donation ID", validators=[DataRequired()])
    Blood_Supply_ID = IntegerField("Blood Supply ID", validators=[DataRequired()])
    submit = SubmitField('Update Blood Donation')

    def validate_Donation_ID(self, Donation_ID):                                        # Check Donation ID if it exists
        dID = Blood_Donation.query.filter_by(Donation_ID=Donation_ID.data).first()
        if not dID:
            raise ValidationError('Blood Donation ID does not exist in the system.')

    def validate_Blood_Supply_ID(self, Blood_Supply_ID):                                        # Check Blood Supply ID if it exists
        bID = Supply_Record.query.filter_by(Blood_Supply_ID=Blood_Supply_ID.data).first()
        if not bID:
            raise ValidationError('Blood Supply ID does not exist in the system.')

#***********************************************************************************************************

# *** Form to delete contanminated blood***
class DeleteBloodDonation(FlaskForm):
    Donation_ID = IntegerField("Blood Donation ID", validators=[DataRequired()])
    submit = SubmitField('Delete From Blood Donation')

    def validate_Donation_ID(self, Donation_ID):                                        # Check Donation ID if it exists
        removeDID = Blood_Donation.query.filter_by(Donation_ID=Donation_ID.data).first()
        if not removeDID:
            raise ValidationError('Blood Donation ID does not exist in the system.')
