//const cors = require("cors");
//const config = require("./db_files/config");
//const port = config.get("ports");
const express = require("express");
const mongoose = require("mongoose");
const authRoutes = require('./routes/authRoutes');
const { logger } = require("./logger");
const cookieParser = require("cookie-parser");
const { requireAuth, checkUser } = require("./middleware/authMiddleware");

logger.debug("====== System startup ======");
const app = express(); const port = 8080

// middleware
//app.use(cors({ origin: "*" }));
app.use(express.static("public"));
app.use(express.json());
app.use(cookieParser());

// view engine
app.set('view engine', 'ejs');

const dbURI = 'mongodb+srv://admin:elbaz@cluster0.3wxcgz2.mongodb.net/node-auth';

//const dbURI = config.get("mongo");
mongoose.connect(dbURI, { useNewUrlParser: true, useUnifiedTopology: true})
  .then((result) => {
    console.log(result.connection)    
    app.listen(3000, () => console.log(`Listening to port ${3000}`))
  })
  .catch((err) => console.log(err));



// routes
app.get('*', checkUser)
app.get('/', (req, res) => res.render('home'));
app.get('/smoothies', (req, res) => res.render('smoothies'));
app.use(authRoutes);

// cookies
/*
app.get('/set-cookies', (req, res) => {
  // res.setHeader('Set-Cookie', 'newUser=true');
  res.cookie('newUser', false);
  res.cookie('isEmployee', true, { maxAge: 1000 * 60 * 60 * 24, httpOnly: true });
  res.send('you got the cookies!');
});

app.get('/read-cookies', (req, res) => {
  const cookies = req.cookies;
  console.log(cookies.newUser);
  res.json(cookies);
});
*/
