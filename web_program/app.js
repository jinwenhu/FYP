var express = require ('express');
var http = require('http');
var fs = require('fs');
var app = express ();
app.use(express.static(__dirname + '/public'));
app.listen(3000);

// Loading the index file . html displayed to the client
var server = http.createServer(function(req, res) {
	var pathname = require('url').parse(req.url).pathname;
	console.log("Request for " + pathname + " received.");
	//res.writeHead(200, {"Content-Type": "text/html"});
    fs.readFile(pathname.substr(1), function (err, data) {
      if (err) {
         console.log(err);
         res.writeHead(404, {'Content-Type': 'text/html'});
      }else {	
         res.writeHead(200, {'Content-Type': 'text/html'});	
         res.write(data.toString());		
      }
      res.end();
   });   

});

//var PythonShell = require('python-shell');

//PythonShell.run('test.py', function (err, results) {
//  if (err) throw err;
//  console.log('results: %j', results);
//});

// Loading socket.io
var io = require('socket.io').listen(server);

// When a client connects, we note it in the console
io.sockets.on('connection', function(socket) {
	socket.emit('message', 'You are connected!');
	socket.on('little_newbie', function(username) {	
		socket.username = username;
	});
	socket.on('message', function (message) {
        console.log(socket.username + 'is speaking to me! They’re saying: ' + message);
    });
	socket.on('result', function (message) {
		console.log("receive results");
        console.log(message);
    });
});

	
server.listen(8080);