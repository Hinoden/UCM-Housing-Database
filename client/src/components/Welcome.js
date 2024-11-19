import React from "react";
import { useNavigate} from 'react-router-dom';
import Button from '@mui/material/Button';

import '../style/Welcome.css';

function Welcome() {
    const navigate = useNavigate();

    const handleUserTypeClick = (buttonType) => {
        if (buttonType === "student") {
            navigate("/login/student");
        }
        if (buttonType === "employee") {
            navigate("/login/employee");
        }
    };

    return(
        <div className="WelcomeContainer">
            <h1 id="headerText">Welcome!</h1>
            <p id="descText">Are you a(n)...</p>
            <div className="WelcomeButtons">
                <Button variant="contained" className="StudentButton" onClick={()=>handleUserTypeClick("student")}>Student</Button>
                <p id="orWelcome">or</p>
                <Button variant="contained" className="EmployeeButton" onClick={()=>handleUserTypeClick("employee")}>Employee</Button>
            </div>
        </div>
    )
}

export default Welcome;