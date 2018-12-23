const express = require('express');
const router = express.Router();
const gsearch = require('../bin/search');

/* GET users listing. */
router.post('/', function(req, res, next) {
  req.session.query = req.body.query;
  const searchPromise = gsearch(req.body.query)
        .then((result) => {
          req.session.results = result;
          console.log(result);
          res.redirect('/search/results');
        }, (error) => {console.error(error)});  
});

router.get('/results', function(req, res, next) {
  res.render('results', { title: 'Noodle Results', results: req.session.results, query: req.session.query });
  
  // Resetting the session variables
  req.session.query = null;
  req.session.results = {};
});

module.exports = router;
