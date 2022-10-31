const jwt = require('jsonwebtoken');
const User = require('../models/User');

const requireAuth = (req, res, next) => {
  const token = req.cookies.jwt;

  // check json web token exists & is verified
  if (token) {
    jwt.verify(token, 'secret key', (err, decodedToken) => {
      if (err) {
        console.log(err.message);
        res.redirect('/login'); // in ajax act differently
      } else {
          // we may here- check the user role ...
        console.log(decodedToken);
        next();
      }
    });
  } else {
    res.redirect('/login'); // in ajax act differently
  }
};

// check current user
const checkUser = (req, res, next) => {
    const token = req.cookies.jwt;
    if (token) {
      jwt.verify(token, 'secret key', async (err, decodedToken) => {
        if (err) {
          res.locals.user = null;
          next(); // ?? bad token
        } else {
          let user = await User.findById(decodedToken.id);
          res.locals.user = user; // ? . better user-id, name
          next(); 
        }
      });
    } else {
      res.locals.user = null;
      next();
    }
  };

  module.exports = { requireAuth, checkUser };
