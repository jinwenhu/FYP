var express = require ('express');
var http = require('http');
//var httpProxy = require('http-proxy');
var fs = require('fs');
var app = express ();
var PythonShell = require('python-shell');
var pyshell = new PythonShell('operate.py');
var movie_result = new Array() //returned recommended movie list

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
        // sends a message to the Python script via stdin
        console.log(message);
        pyshell.send(message);

        pyshell.on('message', function (message) {
            // received a message sent from the Python script (a simple "print" statement)
            console.log('feedback');
            console.log(message);
            var temp_list = message.split(",");
            movie_result.push(temp_list);
        });

        // end the input stream and allow the process to exit
        pyshell.end(function (err) {
            if (err) throw err;
            console.log('finished');
            //console.log(movie_result[0][0]);

        });
        //socket.disconnect(0);
    });
    socket.on('next', function (message) {
        console.log(message);
        var id = parseInt(message);
        if (movie_result[id] == undefined || movie_result[id] == null){
            socket.emit('message', "you have not completed rating or you do not have enough movie_space.");
        }
        else{
            socket.emit('movie_name', movie_result[id][0]);
            socket.emit('movie_description', movie_result[id][1]);
            socket.emit('movie_image', movie_result[id][2]);
            socket.emit('movie_url', movie_result[id][3]);
        }
    });
});

server.listen(8080);