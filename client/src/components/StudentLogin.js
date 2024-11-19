import React from "react";
import {useNavigate} from 'react-router-dom';
import TextField from '@mui/material/TextField';
import Button from '@mui/material/Button';
import '../style/StudentLogin.css';

function StudentLogin() {
    const navigate = useNavigate();

    const GoBackClick = () => {
        navigate("/");
    };

    return(
        <div>
            <div id="goBackStuContainer">
                <p id="whoopsStu">Not a Student?</p>
                <Button id="goBackStu" variant="text" onClick={() => GoBackClick()}>Go Back</Button>
            </div>
            <div className="LoginContainer">
                <h1 id="stuHeader">Student Portal</h1>
                <p id="stuUsernameLabel">UCMNetID or M.ID (Required)</p>
                <TextField id="username" variant="outlined" required/>
                <p id="stuPasswordLabel">Password (Required)</p>
                <TextField id="password" variant="outlined" required/>
                <Button variant="contained" id="stuLogin">Sign In</Button>
            </div>
            <p id="orStudent">OR</p>
            <div className="SignUpContainer">
                <h1 id="stuHeader">Sign Up</h1>
                <p id="stuNameLabel">Full Name (Required)</p>
                <TextField id="fullName" variant="outlined" required />
                <p id="stuUsername1Label">UCMNetID or M.ID (Required)</p>
                <TextField id="username" variant="outlined" required/>
                <p id="stuPassword1Label">Password (Required)</p>
                <TextField id="password" variant="outlined" required/>
                <Button variant="contained" id="stuSignUp">Sign Up</Button>
            </div>
        </div>
    )
}

export default StudentLogin;