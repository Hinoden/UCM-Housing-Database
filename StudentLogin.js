import React, { useState } from "react";
import { useNavigate } from 'react-router-dom';
import TextField from '@mui/material/TextField';
import Button from '@mui/material/Button';
import axios from 'axios';
import '../style/StudentLogin.css';

function StudentLogin() {
    const navigate = useNavigate();
    const [loginData, setLoginData] = useState({ username: '', password: '' });
    const [signupData, setSignupData] = useState({ fullName: '', username: '', password: '' });
    const [loginError, setLoginError] = useState('');
    const [signupError, setSignupError] = useState('');
    const [signupSuccess, setSignupSuccess] = useState('');

    // Login Handler
    const handleLogin = async () => {
        try {
            const response = await axios.post('http://localhost:3500/api/login', loginData);
            alert(response.data.message); // Success message
            navigate('/dashboard'); // Navigate on successful login
        } catch (error) {
            setLoginError(error.response ? error.response.data.message : 'Error connecting to server');
        }
    };

    // Sign-Up Handler
    const handleSignup = async () => {
        try {
            const response = await axios.post('http://localhost:3500/api/signup', signupData);
            setSignupSuccess(response.data.message);
            setSignupError('');
        } catch (error) {
            setSignupSuccess('');
            setSignupError(error.response ? error.response.data.message : 'Error connecting to server');
        }
    };

    return (
        <div>
            {/* Login Section */}
            <div id="goBackStuContainer">
                <p id="whoopsStu">Not a Student?</p>
                <Button id="goBackStu" variant="text" onClick={() => navigate("/")}>Go Back</Button>
            </div>
            <div className="LoginContainer">
                <h1 id="stuHeader">Student Portal</h1>
                <p id="stuUsernameLabel">UCMNetID or M.ID (Required)</p>
                <TextField
                    id="username"
                    variant="outlined"
                    required
                    value={loginData.username}
                    onChange={(e) => setLoginData({ ...loginData, username: e.target.value })}
                />
                <p id="stuPasswordLabel">Password (Required)</p>
                <TextField
                    id="password"
                    type="password"
                    variant="outlined"
                    required
                    value={loginData.password}
                    onChange={(e) => setLoginData({ ...loginData, password: e.target.value })}
                />
                <Button variant="contained" id="stuLogin" onClick={handleLogin}>Sign In</Button>
                {loginError && <p style={{ color: 'red' }}>{loginError}</p>}
            </div>

            <p id="orStudent">OR</p>

            {/* Sign-Up Section */}
            <div className="SignUpContainer">
                <h1 id="stuHeader">Sign Up</h1>
                <p id="stuNameLabel">Full Name (Required)</p>
                <TextField
                    id="fullName"
                    variant="outlined"
                    required
                    value={signupData.fullName}
                    onChange={(e) => setSignupData({ ...signupData, fullName: e.target.value })}
                />
                <p id="stuUsername1Label">UCMNetID or M.ID (Required)</p>
                <TextField
                    id="username"
                    variant="outlined"
                    required
                    value={signupData.username}
                    onChange={(e) => setSignupData({ ...signupData, username: e.target.value })}
                />
                <p id="stuPassword1Label">Password (Required)</p>
                <TextField
                    id="password"
                    type="password"
                    variant="outlined"
                    required
                    value={signupData.password}
                    onChange={(e) => setSignupData({ ...signupData, password: e.target.value })}
                />
                <Button variant="contained" id="stuSignUp" onClick={handleSignup}>Sign Up</Button>
                {signupError && <p style={{ color: 'red' }}>{signupError}</p>}
                {signupSuccess && <p style={{ color: 'green' }}>{signupSuccess}</p>}
            </div>
        </div>
    );
}

export default StudentLogin;
