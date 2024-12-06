import express from 'express';      // framework to create API
import cors from 'cors';            // set up connection between the front-end and back-end
import cookieParser from 'cookie-parser';   // parse all the cookies we have
import bodyParser from 'body-parser';
import session from 'express-session';      // creating our sessions and maintaining them
import sqlite3 from 'sqlite3';    // SQLite3 database
import path from 'path';          // For absolute file paths

const app = express();

// Get the current directory using import.meta.url
const __dirname = path.dirname(new URL(import.meta.url).pathname);

// Set up the SQLite database
const db = new sqlite3.Database(path.join(__dirname, 'housing.db'), (err) => {
    if (err) {
        console.error("Error opening database:", err);
    } else {
        console.log("Connected to the SQLite database!");
    }
});

app.use(express.json());
app.use(cors({
    origin: ["http://localhost:3000"],
    credentials: true       // allows cookies to be enabled
}));

app.use(cookieParser());
app.use(bodyParser.urlencoded({ extended: true }));

// Setup session management
app.use(session({
    key: "userId",     // name of the cookie you'll create
    secret: "illhaveabetteridealater",
    resave: false,
    saveUninitialized: false,
    cookie: {
        secure: false,
        httpOnly: true,
        sameSite: 'lax',
        maxAge: 1000 * 60 * 60 * 24     // expires in a day
    },
}));

// Listen on Port 3500
app.listen(3500, () => {
    console.log("Server running on Port 3500");
});

// Login Route
app.post('/api/login', (req, res) => {
    const { username, password } = req.body;

    if (!username || !password) {
        return res.status(400).send({ message: "Username and password are required!" });
    }

    const query = `SELECT * FROM student WHERE s_email = ? AND s_password = ?`;
    db.get(query, [username, password], (err, row) => {
        if (err) {
            console.error(err);
            return res.status(500).send({ message: "Server error!" });
        }

        if (row) {
            req.session.user = row; // Save user data in session
            res.status(200).send({ message: "Login successful!", user: row });
        } else {
            res.status(401).send({ message: "Invalid username or password!" });
        }
    });
});

// Sign-Up Route
app.post('/api/signup', (req, res) => {
    const { fullName, username, password } = req.body;

    if (!fullName || !username || !password) {
        return res.status(400).send({ message: "All fields are required!" });
    }

    const query = `INSERT INTO users (fullName, username, password) VALUES (?, ?, ?)`;
    db.run(query, [fullName, username, password], function (err) {
        if (err) {
            if (err.message.includes("UNIQUE constraint failed")) {
                return res.status(400).send({ message: "Username already exists!" });
            }
            console.error(err);
            return res.status(500).send({ message: "Server error!" });
        }

        res.status(201).send({ message: "Sign-up successful!" });
    });
});

// Check if User is Logged in
app.get('/api/session', (req, res) => {
    if (req.session.user) {
        res.status(200).send({ loggedIn: true, user: req.session.user });
    } else {
        res.status(401).send({ loggedIn: false });
    }
});

// Logout Endpoint
app.post('/api/logout', (req, res) => {
    req.session.destroy((err) => {
        if (err) {
            return res.status(500).send({ message: "Error logging out!" });
        }
        res.clearCookie('userId');
        res.status(200).send({ message: "Logout successful!" });
    });
});
