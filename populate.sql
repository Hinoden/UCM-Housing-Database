-- insert into building (b_buildingID, b_name, b_numRooms)
-- values
-- (1, 'Half Dome', 100),
-- (2, 'Cathedral', 100),
-- (3, 'Tenaya', 100),
-- (4, 'Sierra Terraces', 100),
-- (5, 'Valley Terraces', 100);
-- (6, 'Granite Pass', 100),
-- (7, 'El Portal', 100),
-- (8, 'Glacier Point', 100),
-- (9, 'Sentinel Rock', 100);

-- insert into student (s_studentID, s_name, s_gender, s_year, s_email, s_buildingID, s_roomID)
-- values 
-- (1, 'Adam', 'M', 1, 'adam@ucmerced.edu', 1, 1),
-- (2, 'Sarah', 'F', 2, 'sarah@ucmerced.edu', 1, 2);
-- (3, 'David', 'N', 4, 'david@ucmerced.edu', 2, 1);

-- insert into room (r_roomID, r_roomType, r_occupied, r_buildingID)
-- values
-- (1, 3, 'T', 1),
-- (2, 3, 'T', 1),
-- (3, 1, 'T', 2);

-- insert into employee(e_employeeID, e_name, e_email)
-- values
-- (1, 'Scott', 'scott@ucmerced.edu'),
-- (2, 'Carla', 'carla@ucmerced.edu');

-- insert into canAccess(a_approved, a_formID, a_employeeID)
-- values
-- ('T', 1, 2),
-- ('T', 2, 2),
-- ('T', 3, 1);

-- insert into canUnlock(u_accessDateTime, u_reason, u_buildingID, u_employeeID)
-- values
-- ('2020-11-11 12:00:00', 'confirming if room has been vacated', 1, 1);

-- insert into contact(c_contactDateTime, c_reason, c_studentID, c_employeeID)
-- values
-- ('2020-05-06 11:53:47', 'update on my housing application please', 1, 1);

-- insert into housingForm(f_formID, f_status, f_accomodations, f_surveyID)
-- values
-- (1, 'A', 'F', 1),
-- (2, 'A', 'F', 2),
-- (3, 'A', 'T', 3);

-- delete from housingForm;

-- insert into profileSurvey(s_surveyID, s_prefRoomType, s_cleanliness, s_prefRoomGen)
-- values
-- (1, 3, 'Very Clean', 'M'),
-- (2, 3, 'Somewhat Clean', 'F'),
-- (3, 1, 'Somewhat Clean', 'N');