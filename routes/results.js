var express = require('express');
var router = express.Router();

/* GET users listing. */
router.post('/', function(req, res, next) {
  req.session.query = req.body.searchbar;
  req.session.results = { "Repo Page": "https://github.com/Koustav-Samaddar/Noodle-Search" };

  res.redirect('/search/results');
});

router.get('/results', function(req, res, next) {
  res.render('results', { title: 'Noodle Results', results: req.session.results, query: req.session.query });

  // Resetting the session variables
  req.session.query = null;
  req.session.results = {};
});

module.exports = router;
