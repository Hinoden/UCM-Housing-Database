import React from "react";
import {useNavigate} from 'react-router-dom';
import TextField from '@mui/material/TextField';
import Button from '@mui/material/Button';
import '../style/EmployeeLogin.css';

function EmployeeLogin() {
    const navigate = useNavigate();

    const GoBackClick = () => {
        navigate("/");
    };

    return(
        <div>
            <div id="goBackEmpContainer">
                <p id="whoopsEmp">Not an Employee?</p>
                <Button id="goBackEmp" variant="text" onClick={() => GoBackClick()}>Go Back</Button>
            </div>
            <div className="EmpLoginContainer">
                <h1 id="empHeader">Employee Portal</h1>
                <p id="empUsernameLabel">Email (Required)</p>
                <TextField id="username" variant="outlined" required/>
                <p id="empPasswordLabel">Password (Required)</p>
                <TextField id="password" variant="outlined" required/>
                <Button variant="contained" id="empLogin">Sign In</Button>
            </div>
        </div>
    )
}

export default EmployeeLogin;