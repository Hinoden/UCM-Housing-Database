import {BrowserRouter, Routes, Route} from 'react-router-dom';
import Welcome from './components/Welcome.js';
import StudentLogin from './components/StudentLogin.js';
import EmployeeLogin from './components/EmployeeLogin.js';
import './App.css';

function App() {
  return (
    <div className="App">
      <BrowserRouter>
        <Routes>
          <Route path="/" element={<Welcome/>} />
            <Route path="/login/student" element={<StudentLogin />} />
            <Route path="/login/employee" element={<EmployeeLogin />} />
        </Routes>
      </BrowserRouter>
    </div>
  );
}

export default App;