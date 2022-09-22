import os
import secrets
import numpy as np
from PIL import Image
from flask import render_template, url_for, flash, redirect, request, abort, session
from flaskDemo import app, db, bcrypt
from flaskDemo.forms import RegistrationForm, LoginForm, UpdateAccountForm, AddEmployee, AddDonor, AddSupplyRecord, AddBloodDonation, UpdateBloodDonation, DeleteBloodDonation
from flaskDemo.models import User, Employee, Donor, Supply_Record, Blood_Donation
from flask_login import login_user, current_user, logout_user, login_required
from datetime import datetime
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError,Regexp
from sqlalchemy import and_, or_, func


@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html', title='Home')


@app.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)

        getEmpEmail = Employee.query.filter_by(Employee_Email=form.email.data).first()    # Check if employee has profile in system before creating login
        if getEmpEmail:
            db.session.add(user)
            db.session.commit()
            flash('Your account has been created! You are now able to log in', 'success')
            return redirect(url_for('login'))
        else:
            flash('Please inform your Administrator to enter your profile in the system before creating Admin Login')
    return render_template('register.html', title='Register', form=form)


@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            session['email'] = form.email.data                                          #get session email
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', title='Login', form=form)


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))


def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/profile_pics', picture_fn)

    output_size = (125, 125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)

    return picture_fn


@app.route("/account", methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Your account has been updated!', 'success')
        return redirect(url_for('account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
    return render_template('account.html', title='Account', image_file=image_file, form=form)


#***********************************************************************************************************

# View for Blood Donor
@app.route("/viewdonor")
@login_required
def viewdonor():
    resultDonor = Donor.query.add_columns(Donor.First_Name, Donor.Last_Name, Donor.Donor_Phone_Number, Donor.Donor_Email, Donor.Donor_Blood_Group, Donor.Sex) \
                  .order_by(Donor.First_Name)
    return render_template('viewdonor.html', title='View Donor', result=resultDonor)

#***********************************************************************************************************

# View for Blood Supply Record
@app.route("/viewsupplyrecord")
@login_required
def viewsupplyrecord():
    resultSupplyRecord = Supply_Record.query \
                    .add_columns(Supply_Record.Blood_Supply_ID, Supply_Record.Health_Facility_Name, Supply_Record.Blood_Group, Supply_Record.Quantity_Supplied, Supply_Record.Date_of_Supply) \
                    .order_by(Supply_Record.Blood_Supply_ID)
    return render_template('viewsupplyrecord.html', title='View Supply Record', result=resultSupplyRecord)

#***********************************************************************************************************

# View for Blood Donor - Joining 2 tables Blood Donation and Donor
@app.route("/viewblooddonation")
@login_required
def viewblooddonation():
    resultBloodDonor = Blood_Donation.query.join(Donor, Blood_Donation.Donor_ID == Donor.Donor_ID) \
                    .add_columns(Blood_Donation.Donation_ID, Donor.First_Name, Donor.Last_Name, Donor.Donor_Blood_Group, Blood_Donation.Blood_Test_Conclusion, Blood_Donation.Blood_Supply_ID) \
                    .order_by(Donor.First_Name)
    return render_template('viewblooddonation.html', title='View Blood Donation', result=resultBloodDonor)


#***********************************************************************************************************

# View for employee
@app.route("/viewemployee")
@login_required
def viewemployee():
    resultEmployee = Employee.query \
                    .add_columns(Employee.First_Name, Employee.Last_Name, Employee.Employee_Designation) \
                    .order_by(Employee.First_Name)
    return render_template('viewemployee.html', title='View Blood Donation', result=resultEmployee)

#***********************************************************************************************************

# View Blood available grouped by blood type
@app.route("/viewbloodavailable")
@login_required
def viewbloodavailable():
    resultBloodAvailable = Blood_Donation.query.join(Donor, Blood_Donation.Donor_ID == Donor.Donor_ID) \
                    .add_columns(Donor.Donor_Blood_Group, Blood_Donation.Blood_Test_Conclusion, Blood_Donation.Inventory_Status, func.count(Blood_Donation.Inventory_Status).label('totCount')) \
                    .filter(Blood_Donation.Inventory_Status=='In Stock') \
                    .group_by(Donor.Donor_Blood_Group) \
                    .order_by(Donor.Donor_Blood_Group)
    return render_template('viewbloodavailable.html', title='View Available Blood', result=resultBloodAvailable)

#***********************************************************************************************************

# View Blood not available grouped by blood type
@app.route("/viewbloodnotavailable")
@login_required
def viewbloodnotavailable():
    resultBloodNotAvailable = Blood_Donation.query.join(Donor, Blood_Donation.Donor_ID == Donor.Donor_ID) \
                    .add_columns(Donor.Donor_Blood_Group, Blood_Donation.Blood_Test_Conclusion, Blood_Donation.Inventory_Status, func.count(Blood_Donation.Inventory_Status).label('totCount')) \
                    .filter(Blood_Donation.Inventory_Status=='Out of Stock') \
                    .group_by(Donor.Donor_Blood_Group) \
                    .order_by(Donor.Donor_Blood_Group)
    return render_template('viewbloodnotavailable.html', title='View Not Available Blood', result=resultBloodNotAvailable)

#***********************************************************************************************************

# View Blood that failed test grouped by blood type
@app.route("/viewbloodfailtest")
@login_required
def viewbloodfailtest():
    resultBloodDisposedOf = Blood_Donation.query.join(Donor, Blood_Donation.Donor_ID == Donor.Donor_ID) \
                    .add_columns(Donor.Donor_Blood_Group, Blood_Donation.Blood_Test_Conclusion, Blood_Donation.Inventory_Status, func.count(Blood_Donation.Inventory_Status).label('totCount')) \
                    .filter(Blood_Donation.Inventory_Status=='To be disposed of') \
                    .group_by(Donor.Donor_Blood_Group) \
                    .order_by(Donor.Donor_Blood_Group)
    return render_template('viewbloodfailtest.html', title='View Blood Disposed of', result=resultBloodDisposedOf)

#***********************************************************************************************************

# *** route to input employee data ***
@app.route("/add_employee", methods=['GET', 'POST'])
@login_required
def add_employee():
    form = AddEmployee()
    if form.validate_on_submit():
        addEmployee = Employee(Employee_Email=form.Employee_Email.data, First_Name=form.First_Name.data, Last_Name=form.Last_Name.data, Employee_Address=form.Employee_Address.data,
                      Employee_Phone_Number=form.Employee_Phone_Number.data, Employee_Designation=form.Employee_Designation.data)
        db.session.add(addEmployee)
        db.session.commit()
        flash('SUCCESS: Employee has been added to the system !!!')

        return redirect(url_for('add_employee'))
    return render_template('add_employee.html', title='Add Employee', form=form)

#***********************************************************************************************************

# *** route to input donor data ***
@app.route("/add_donor", methods=['GET', 'POST'])
@login_required
def add_donor():
    form = AddDonor()
    if form.validate_on_submit():
        addDonor = Donor(First_Name=form.First_Name.data, Last_Name=form.Last_Name.data, Donor_Address=form.Donor_Address.data,
                    Donor_Phone_Number=form.Donor_Phone_Number.data, Donor_Email=form.Donor_Email.data, Donor_Blood_Group=form.Donor_Blood_Group.data,
                    Donor_Medical_Report=form.Donor_Medical_Report.data, Sex=form.Sex.data, Birth_Date=form.Birth_Date.data)
        if form.Donor_Blood_Group.data == 'select option':
            flash('ALERT: select a valid option for Blood Group')
        elif form.Sex.data == 'select option':
            flash('ALERT: select a valid option for Sex')
        else:
            db.session.add(addDonor)
            db.session.commit()
            flash('SUCCESS: Blood Donor has been addedd to the system !!!')
            return redirect(url_for('add_donor'))
    return render_template('add_donor.html', title='Add Donor', form=form)

#***********************************************************************************************************

# *** route to input supply record ***
@app.route("/add_supply", methods=['GET', 'POST'])
@login_required
def add_supply():
    form = AddSupplyRecord()
    if form.validate_on_submit():
        addSupply = Supply_Record(Health_Facility_Name=form.Health_Facility_Name.data, Blood_Group=form.Blood_Group.data, Quantity_Supplied=form.Quantity_Supplied.data, Date_of_Supply=form.Date_of_Supply.data)
        if form.Health_Facility_Name.data == 'select option':
            flash('ALERT: select a valid option for Health Facility Name')
        elif form.Blood_Group.data == 'select option':
            flash('ALERT: select a valid option for Blood Group')
        else:
            db.session.add(addSupply)
            db.session.commit()
            flash('SUCCESS: Supply Record has been added to the system !!!')
            return redirect(url_for('add_supply'))
    return render_template('add_supply.html', title='Add Supply Record', form=form)

#***********************************************************************************************************

#*** route to input blood test data ***
@app.route("/add_blood_donation", methods=['GET', 'POST'])
@login_required
def add_blood_donation():
    form = AddBloodDonation()
    if form.validate_on_submit():
        getDonorID = Donor.query.with_entities(Donor.Donor_ID).filter(Donor.Donor_Email==form.Donor_Email.data)
        testResult=list(getDonorID)             #pass query result to list
        toArray = np.array(testResult)          #pass to array
        toInt = int(toArray[0])

        getEmployeeEmail = session['email']     #get employee email logged in

        addBloodDonation = Blood_Donation(Donor_ID=toInt, Employee_Email=getEmployeeEmail, Date_of_Donation=form.Date_of_Donation.data, Hepatitis_B=form.Hepatitis_B.data,
                    Hepatitis_C=form.Hepatitis_C.data, HIV=form.HIV.data, Syphilis=form.Syphilis.data, Zika_Virus=form.Zika_Virus.data, West_Nile_Virus=form.West_Nile_Virus.data,
                    Blood_Test_Conclusion=form.Blood_Test_Conclusion.data, Inventory_Status=form.Inventory_Status.data)
        if form.Hepatitis_B.data == 'select option' or form.Hepatitis_C.data == 'select option':
            flash('ALERT: select a valid option for blood test')
        elif form.HIV.data == 'select option' or form.Syphilis.data == 'select option':
            flash('ALERT: select a valid option for blood test')
        elif form.Zika_Virus.data == 'select option' or form.West_Nile_Virus.data == 'select option':
            flash('ALERT: select a valid option for blood test')
        elif form.Blood_Test_Conclusion.data == 'select option':
            flash('ALERT: select a valid option for blood test conclusion')
        elif form.Inventory_Status.data == 'select option':
            flash('ALERT: select a valid option for status')
        else:
            db.session.add(addBloodDonation)
            db.session.commit()
            flash('SUCCESS: Blood Donation has been addedd to the system !!!')
            return redirect(url_for('add_blood_donation'))
    return render_template('add_blood_donation.html', title='Add Blood Test Data', form=form)

#***********************************************************************************************************

# Update for Blood donation
@app.route("/updateblooddonation", methods=['GET', 'POST'])
@login_required
def updateblooddonation():
    form = UpdateBloodDonation()
    if form.validate_on_submit():          # notice we are are not passing the dnumber from the form

        getBloodSupplyID = Blood_Donation.query.filter_by(Donation_ID = form.Donation_ID.data, Blood_Supply_ID = None).first()      # Check if Blood Supply ID is NULL

        if getBloodSupplyID:
            updateBSID = Blood_Donation.query.filter_by(Donation_ID = form.Donation_ID.data, Blood_Supply_ID = None) \
                        .update({Blood_Donation.Blood_Supply_ID: form.Blood_Supply_ID.data, Blood_Donation.Inventory_Status: 'Out of Stock'})
            db.session.commit()
            flash('SUCCESS: Blood Supply ID in Blood Donation Table has been updated !!!')
            return redirect(url_for('updateblooddonation'))
        else:
            flash('ALERT: The Blood Donation ID is already associated with a Blood Supply ID')
    elif request.method == 'GET':              # notice we are not passing the dnumber to the form
        form.Donation_ID.data = Blood_Donation.Donation_ID
        form.Blood_Supply_ID.data = Blood_Donation.Blood_Supply_ID
    return render_template('updateblooddonation.html', title='Update Blood Donation', form=form)

#***********************************************************************************************************

# View Blood not available grouped by blood type
@app.route("/viewbloodfailtest2")
@login_required
def viewbloodfailtest2():
    resultBloodDisposedOf2 = Blood_Donation.query \
                    .add_columns(Blood_Donation.Donation_ID, Blood_Donation.Date_of_Donation, Blood_Donation.Blood_Test_Conclusion, Blood_Donation.Inventory_Status) \
                    .filter(Blood_Donation.Inventory_Status=='To be disposed of') \
                    .order_by(Blood_Donation.Donation_ID)
    return render_template('viewbloodfailtest2.html', title='View Blood to be disposed of', result=resultBloodDisposedOf2)


#***********************************************************************************************************

# Delete blood that failed test
@app.route("/deletebloodfailtest", methods=['GET', 'POST'])
@login_required
def deletebloodfailtest():
    form = DeleteBloodDonation()
    if form.validate_on_submit():
        checkDonationID = Blood_Donation.query.filter_by(Donation_ID = form.Donation_ID.data, Inventory_Status = 'To be disposed of').first()

        if checkDonationID:
            resultDeleteBlood = Blood_Donation.query.filter(Blood_Donation.Donation_ID==form.Donation_ID.data).delete()
            db.session.commit()
            flash('SUCCESS: You have successfuly deleted from Blood Doonation Table !!!')
            return redirect(url_for('deletebloodfailtest'))
        else:
            flash('ALERT: You are about to delete a Blood Donation Record with no Failed Test')
    return render_template('deletebloodfailtest.html', title='Delete Blood that Failed Test', form=form)
