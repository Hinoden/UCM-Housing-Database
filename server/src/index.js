import express from 'express';      //framework to create API
import cors from 'cors';        //set up connection between the front-end and back-end
import cookieParser from 'cookie-parser';   //parse all the cookies we have
import bodyParser from 'body-parser';
import session from 'express-session';      //creating our sessions and maintaining them

const app = express();

app.use(express.json());
app.use(cors({
    origin: ["http://localhost:3000"],
    // methods: ["GET", "POST", ]
    credentials: true       //allows cookies to be enabled
}));

app.use(cookieParser());
app.use(bodyParser.urlencoded({extended: true}));

app.use(session({
    key: "userId",     //name of the cookie you'll create
    secret: "illhaveabetteridealater",
    resave: false,
    saveUninitialized: false,
    cookie: {
        secure: false,
        httpOnly: true,
        sameSite: 'lax',
        maxAge: 1000 * 60 * 60 * 24     //will expire in a day;
    },
}))

app.listen(3500, () => {
    console.log("Server running on Port 3500");
});