-- Create database for ABC Health Care
CREATE DATABASE abc_health_care;

USE abc_health_care;

-- Create table to record all employee data 
CREATE TABLE employee (
	Employee_Email VARCHAR(60) NOT NULL,
    First_Name VARCHAR(30) NOT NULL,
	Last_Name VARCHAR(30) NOT NULL,
	Employee_Address VARCHAR(60) NOT NULL,
	Employee_Phone_Number BIGINT NOT NULL,
	Employee_Designation VARCHAR(40) NOT NULL,

    PRIMARY KEY (Employee_Email)
);
    
    
-- Create table to record all donor data 
CREATE TABLE donor (
	Donor_ID INT NOT NULL AUTO_INCREMENT,
	First_Name VARCHAR(30) NOT NULL,
	Last_Name VARCHAR(30) NOT NULL,
	Donor_Address VARCHAR(60) NOT NULL,
	Donor_Phone_Number BIGINT NOT NULL,
    Donor_Email VARCHAR(60) NOT NULL,
	Donor_Blood_Group VARCHAR(10) NOT NULL,
	Donor_Medical_Report TEXT(500) NOT NULL,
	Sex VARCHAR(10) NOT NULL,
	Birth_Date DATE NOT NULL,
    
    PRIMARY KEY (Donor_ID)
);
-- Altering table donor to make auto increment start from 1001
ALTER TABLE donor AUTO_INCREMENT=1001;


-- Create table to record blood supplied to different health care facilities
CREATE TABLE supply_record (
	Blood_Supply_ID INT NOT NULL AUTO_INCREMENT,
    Health_Facility_Name VARCHAR(200) NOT NULL,
    Blood_Group VARCHAR(10) NOT NULL,
    Quantity_Supplied INT NOT NULL,
    Date_of_Supply DATE NOT NULL,
    
    PRIMARY KEY (Blood_Supply_ID)
);
-- Altering table blood_supplied to make auto increment start from 10000001
ALTER TABLE supply_record AUTO_INCREMENT=100001;


-- Create table to record all blood test data 
CREATE TABLE blood_donation(
	Donation_ID INT NOT NULL AUTO_INCREMENT,
	Donor_ID INT NOT NULL,
	Employee_Email VARCHAR(60) NOT NULL,
    Blood_Supply_ID INT,
	Date_of_Donation DATE NOT NULL,
	Hepatitis_B VARCHAR(10) NOT NULL,
	Hepatitis_C VARCHAR(10) NOT NULL,
	HIV VARCHAR (10) NOT NULL,
	Syphilis VARCHAR (10) NOT NULL,
	Zika_Virus VARCHAR(10) NOT NULL,
	West_Nile_Virus VARCHAR(10) NOT NULL,
	Blood_Test_Conclusion VARCHAR (200) NOT NULL,
    Inventory_Status VARCHAR (30) NOT NULL,
	
    PRIMARY KEY (Donation_ID),
    FOREIGN KEY (Donor_ID) REFERENCES donor(Donor_ID) ON DELETE CASCADE,
    FOREIGN KEY (Employee_Email) REFERENCES employee(Employee_Email) ON DELETE CASCADE,
    FOREIGN KEY (Blood_Supply_ID) REFERENCES supply_record(Blood_Supply_ID) ON DELETE CASCADE
);
-- Altering table blood_test_data to make auto increment start from 100001
ALTER TABLE blood_donation AUTO_INCREMENT=10000001;


-- Create user table for employee login authentication
CREATE TABLE user (
	id INT NOT NULL AUTO_INCREMENT,
    username VARCHAR(20) NOT NULL,
    email VARCHAR(120) NOT NULL,
    image_file VARCHAR(20),
    password VARCHAR(60),
    
    PRIMARY KEY (id),
    FOREIGN KEY (email) REFERENCES employee(Employee_Email) ON DELETE CASCADE
);


-- **************************************** BELOW ARE THE TEST DATA ****************************************
-- Test data for employee table
INSERT INTO employee ( Employee_Email, First_Name, Last_Name, Employee_Address, Employee_Phone_Number, Employee_Designation) VALUES
	('mcoker@abc.com', 'Muyiwa', 'Coker', '2020 Broadway, Chicago IL', 2345678987, 'Lab Tech'),
    ('mflowers@abc.com', 'Mia', 'Flowers', '2040 Broadway, Chicago IL', 2555678987, 'Manager'),
    ('iheard@abc.com', 'Isabel', 'Heard', '1040 Broadway, Chicago IL', 2599678987, 'Phlebotomist'),
    ('pparker@abc.com', 'Peter', 'Parker', '3040 Broadway, Chicago IL', 2555634587, 'Phlebotomist'),
    ('mjane@abc.com', 'Mary', 'Jane', '4020 Broadway, Chicago IL', 2345678922, 'Front Desk');
    
-- Test data for donor table
INSERT INTO donor (First_Name, Last_Name, Donor_Address, Donor_Phone_Number, Donor_Email, Donor_Blood_Group, Donor_Medical_Report, Sex, Birth_Date) VALUES
	('Loise', 'Lane', '504 Nissan Rd, Chicago IL', 2346543476, 'llane@planet.com', 'A', 'None', 'Female', '1970-01-11'),
    ('Clark', 'Kent', '524 Infiniti Rd, Chicago IL', 2356543476, 'ckent@krypton.com', 'O', 'None', 'Male', '1970-02-11'),
    ('Bruce', 'Wayne', '404 Maybach Rd, Chicago IL', 2346223476, 'bwayne@rich.com', 'B', 'None', 'Male', '1965-01-01'),
    ('Tony', 'Stark', '504 RollsRoyce Rd, Chicago IL', 2388543476, 'tstark@rich.com', 'AB', 'None', 'Male', '1975-03-03'),
    ('Wonder', 'Woman', '784 Lexus Rd, Chicago IL', 2346511476, 'wwoman@amazon.com', 'A', 'None', 'Female', '1960-01-01'),
    ('Thor', 'Oden', '504 VAlhala Rd, Chicago IL', 2346543276, 'toden@hammer.com', 'B', 'None', 'Male', '1970-06-20'),
    ('Dominic', 'Turedo', '557 Challenger Rd, Chicago IL', 2346543476, 'dturedo@fast.com', 'AB', 'None', 'Male', '1980-11-11'),
    ('Black', 'Widow', '794 bike Rd, Chicago IL', 2566543476, 'bwidow@fighter.com', 'O', 'None', 'Female', '1980-06-11');