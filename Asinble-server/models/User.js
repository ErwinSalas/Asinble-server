var mongoose = require('mongoose'),
    Schema = mongoose.Schema;


var usersSchema = new Schema({

    username:		{ type: String },
    password:       {type : String},
    access:		{ type: Number },

});


module.exports = mongoose.model('User', usersSchema);
