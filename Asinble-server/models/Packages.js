var mongoose = require('mongoose'),
    Schema = mongoose.Schema;


var packagesSchema = new Schema({

    name:		{ type: String },
    img:       {type : String},
    playbook:		{ type: String },

});


module.exports = mongoose.model('Package', packagesSchema);
