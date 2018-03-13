const express = require('express') 
const app = express() 


app.get('/', (req, res) => res.send('Servicio')) 

app.get('/servicio2', (req, res) => res.send('Servicio2'))





app.listen(3000, () => console.log('Example app listening on port 3000!'))