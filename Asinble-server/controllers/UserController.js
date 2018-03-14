module.exports = function() {

    var Users = require('../models/User.js');

    //GET - Return all products in the DB
    Login = function(req, res) {
        Users.find(function(err, userList) {
            if(!err) {
                userList.forEach(element => {
                    if (element.username==req.body.username && element.pasword==req.body.password){
                        res.send(true);
                    }
                });
                
            } else {
                console.log('ERROR: ' + err);
            }
        });
    };

    

    //POST - Insert a new User in the DB
    addUser = function(req, res) {
        console.log('POST');
        console.log(req.body);

        var user = new User({
            username:    req.body.username,
            password: 	  req.body.password,
            access:  req.body.access
        });

        user.save(function(err) {
            if(!err) {
                console.log('Created');
            } else {
                console.log('ERROR: ' + err);
            }
        });

        res.send(user);
    };

    

    

};
