CREATE TABLE IF NOT EXISTS student (
    s_studentID decimal(12,0) NOT NULL,
    s_name VARCHAR(25) NOT NULL,
    s_gender CHAR(1) NOT NULL,
    s_year INT NOT NULL,
    s_email VARCHAR(100) NOT NULL UNIQUE,
    s_buildingID decimal(12,0) NOT NULL,
    s_roomID decimal(12,0) NOT NULL,
    PRIMARY KEY (s_studentID),
    FOREIGN KEY (s_buildingID) REFERENCES building(b_buildingID),
    FOREIGN KEY (s_roomID) REFERENCES room(r_roomID)
);

CREATE TABLE IF NOT EXISTS building (
    b_buildingID decimal(12,0) NOT NULL,
    b_name VARCHAR(25) NOT NULL,
    b_numRooms INT NOT NULL,
    PRIMARY KEY (b_buildingID)
);

CREATE TABLE IF NOT EXISTS room (
    r_roomID decimal(12,0) NOT NULL,
    r_roomType INT NOT NULL,
    r_occupied CHAR(1) NOT NULL,
    r_buildingID decimal(12,0) NOT NULL,
    PRIMARY KEY (r_roomID),
    FOREIGN KEY (r_buildingID) REFERENCES building(b_buildingID)
);

CREATE TABLE IF NOT EXISTS employee (
    e_employeeID decimal(12,0) NOT NULL,
    e_name VARCHAR(25) NOT NULL,
    e_email VARCHAR(100) NOT NULL UNIQUE,
    PRIMARY KEY (e_employeeID)
);

CREATE TABLE IF NOT EXISTS canUnlock (
    u_accessDateTime DATETIME NOT NULL,
    u_reason VARCHAR(255) NOT NULL,
    u_buildingID decimal(12,0) NOT NULL,
    u_employeeID decimal(12,0) NOT NULL,
    FOREIGN KEY (u_buildingID) REFERENCES building(b_buildingID),
    FOREIGN KEY (u_employeeID) REFERENCES employee(e_employeeID)
);

CREATE TABLE IF NOT EXISTS contact (
    c_contactDateTime DATETIME NOT NULL,
    c_reason VARCHAR(255) NOT NULL,
    c_studentID decimal(12,0) NOT NULL,
    c_employeeID decimal(12,0) NOT NULL,
    FOREIGN KEY (c_studentID) REFERENCES student(s_studentID),
    FOREIGN KEY(c_employeeID) REFERENCES employee(e_employeeID)
);

CREATE TABLE IF NOT EXISTS housingForm (
    f_formID decimal(12,0) NOT NULL,
    f_status CHAR(1) NOT NULL,
    f_accomodations CHAR(1) NOT NULL,
    f_surveyID decimal(12,0) NOT NULL,
    FOREIGN KEY (f_surveyID) REFERENCES profileSurvey(ps_surveyID)
);

CREATE TABLE IF NOT EXISTS profileSurvey (
    s_surveyID decimal(12,0) NOT NULL,
    s_prefRoomType INT NOT NULL,
    s_cleanliness VARCHAR(255) NOT NULL,
    s_prefRoomGen CHAR(1) NOT NULL
);

CREATE TABLE IF NOT EXISTS canAccess (
    a_approved CHAR(1) NOT NULL,
    a_formID decimal(12,0) NOT NULL,
    a_employeeID decimal(12,0) NOT NULL,
    FOREIGN KEY (a_formID) REFERENCES housingForm(f_formID),
    FOREIGN KEY (a_employeeID) REFERENCES employee(e_employeeID)
);

insert into building (b_buildingID, b_name, b_numRooms)
values
(1, 'Half Dome', 100),
(2, 'Cathedral', 100),
(3, 'Tenaya', 100),
(4, 'Sierra Terraces', 100),
(5, 'Valley Terraces', 100),
(6, 'Granite Pass', 100),
(7, 'El Portal', 100),
(8, 'Glacier Point', 100),
(9, 'Sentinel Rock', 100);

insert into student (s_studentID, s_name, s_gender, s_year, s_email, s_buildingID, s_roomID)
values 
(1, 'Adam', 'M', 1, 'adam@ucmerced.edu', 1, 1),
(2, 'Sarah', 'F', 2, 'sarah@ucmerced.edu', 1, 2),
(3, 'David', 'N', 4, 'david@ucmerced.edu', 2, 1),
(4, 'test', 'N', 10, 'test@ucmerced.edu', 6, 1); 

delete from student
where s_year > 4;

update student
set s_gender = 'M'
where s_studentID = 3;

insert into room (r_roomID, r_roomType, r_occupied, r_buildingID)
values
(1, 3, 'T', 1),
(2, 3, 'T', 1),
(3, 1, 'T', 2);

insert into employee(e_employeeID, e_name, e_email)
values
(1, 'Scott', 'scott@ucmerced.edu'),
(2, 'Carla', 'carla@ucmerced.edu');

insert into canAccess(a_approved, a_formID, a_employeeID)
values
('T', 1, 2),
('T', 2, 2),
('T', 3, 1);

insert into canUnlock(u_accessDateTime, u_reason, u_buildingID, u_employeeID)
values
('2020-11-11 12:00:00', 'confirming if room has been vacated', 1, 1);

insert into contact(c_contactDateTime, c_reason, c_studentID, c_employeeID)
values
('2020-05-06 11:53:47', 'update on my housing application please', 1, 1);

insert into housingForm(f_formID, f_status, f_accomodations, f_surveyID)
values
(1, 'A', 'F', 1),
(2, 'A', 'F', 2),
(3, 'A', 'T', 3);


insert into profileSurvey(s_surveyID, s_prefRoomType, s_cleanliness, s_prefRoomGen)
values
(1, 3, 'Very Clean', 'M'),
(2, 3, 'Somewhat Clean', 'F'),
(3, 1, 'Somewhat Clean', 'N');