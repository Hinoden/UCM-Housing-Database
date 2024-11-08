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