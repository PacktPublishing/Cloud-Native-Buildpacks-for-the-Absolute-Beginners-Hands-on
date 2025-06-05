const http = require('http');
 
const hostname = '0.0.0.0';
const port = 8080;
 
const server = http.createServer((req, res) => {
  res.statusCode = 200;
  res.setHeader('Content-Type', 'text/plain');
  res.end('Hello and welcome to world of Cloud Native Buildpacks!');
});
 
// For demo purposes we do not actually start the server.  This
// allows us pretend to start the server and check if the output
// message is correct.
server.listen(port, hostname, () => {
  console.log(`Server running at http://${hostname}:${port}/`);
});
console.log(`Server running at http://${hostname}:${port}/`)
