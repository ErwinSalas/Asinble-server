const express = require('express') 
const userController = require('./controllers/UserController.js')
const app = express() 


app.mongoose.connect('mongodb://ersalas:rockero123456789@ds213229.mlab.com:13229/ansible-db', function(err, res) {
	if(err) {
		console.log('ERROR: connecting to Database. ' + err);
	}else {
		console.log('Connected to Database');
	}
});

app.post('/auth', userController.Login) 

app.get('/servicio-test', (req, res) => res.send('Prueba'))





app.listen(3000, () => console.log('Example app listening on port 3000!'))