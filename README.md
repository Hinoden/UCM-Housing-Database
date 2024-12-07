# UC Merced/Fall2024/CSE111-Project
## By Jeffrey Peng and Kristina Wong

### Operating using Flask

### To run: python server.py 

### DB Tables and columns: 
  - assets
  
- building
  - buildingId
  - name
  - numRoom
- canAccess
  - approved
  - formID
  - employeeID
- canUnlock
  - accessDateTime
  - reason
  - buildingID
  - employeeID
- contact
  - contactDateTime
  - reason
  - studentID
  - employeeID
- employee
  - employeeID
  - name
  - email
- housingForm
  - formID
  - status
  - accommodations
  - surveyID
- profileSurvey
  - surveyID
  - prefRoomType
  - cleanliness
  - prefRoomGen
- room
  - roomID
  - roomType
  - occupied
  - buildingID
- student
  - studentID
  - name
  - gender
  - year
  - email
  - buildingID
  - roomID
