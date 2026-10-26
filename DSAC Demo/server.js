var url = require('url');
var qs = require('querystring');
var request = require('request');
var formidable = require('formidable');
var fs = require('fs');
var sa = require('superagent');

var wwwRoot = process.env.WWWROOT || './';
var googleCredentials = {};
var googleAccessToken = '';
var twitterAccessToken = '';

// var getGoogleAccessToken = function() {
//   request.post('https://accounts.google.com/o/oauth2/token', { form: googleCredentials }, function (error, response, body) {
//     if (response.statusCode == 200) {
//       var data = JSON.parse(body);
//       googleAccessToken = data.access_token;
//       setTimeout(getGoogleAccessToken, data.expires_in * 1000);
//     }
//   });
// }

// require('jsonfile').readFile(wwwRoot + 'oauth.json', function(err, obj) {
//   if (err || obj == null) {
//     console.log('No or invalid "oauth.json" file found. Please provide one in the following format:', JSON.stringify({ "google": { "client_id": "", "client_secret": "", "refresh_token": "", "grant_type": "refresh_token" }, "twitter": { "access_token": "" } }));
//     return;
//   }
//   googleCredentials = obj.google;
//   twitterAccessToken = obj.twitter.access_token;
//   getGoogleAccessToken();
// });

var serveStatic = require('serve-static')(wwwRoot, { 'index': ['index.html'] });
var blackList = [ '/oauth.json' ];

require('http').createServer(function(req, res){

  var reqUrl = url.parse(req.url, true);
  console.log(reqUrl.pathname)


  if (reqUrl.pathname == '/proxy/') {
    if (reqUrl.query.url) {
      var targetUrl = url.parse(reqUrl.query.url);
      req.headers.host = targetUrl.host;
      if (targetUrl.host == 'api.twitter.com') req.headers.Authorization = 'Bearer ' + twitterAccessToken;
      if (targetUrl.host == 'www.googleapis.com') req.headers.Authorization = 'Bearer ' + googleAccessToken;
      var options = { url: targetUrl, headers: req.headers, method: req.method };
      if (req.method == 'POST') {
        var body = [];
        req.on('data', function(chunk) {
          body.push(chunk);
        }).on('end', function() {
          options.form = Buffer.concat(body).toString();
          request(options).on('error', function(e) { res.end(e); }).pipe(res);
        });
      } else {
        request(options).on('error', function(e) { res.end(e); }).pipe(res);
      }
    } else {
      res.statusCode = 400;
      res.end('No "url" parameter found');
    }
  } else if (reqUrl.pathname == '/processnl' && req.method == 'POST'){
    let body = '';
    
    req.on('data', chunk => {
        body += chunk.toString();
        console.log('chunk')
    });

    req.on('end', () => {
        var data = qs.parse(body);
        
        let text = data['nl-text']
        console.log(text)

        request.post('http://localhost:8000/anlayse', { body: text }, function (error, response, body) {
          if (response.statusCode == 200) {
            var data = JSON.parse(body);
            console.dir(data)
          }
        });    

        res.statusCode = 200;
        fs.readFile('./composition.html',null,function(error,data){
          if (error) {
            res.writeHead(404);
            res.write('file not found');
          } else {
            res.write(data);
          }
          res.end();
        });
        
    });
  } else if (reqUrl.pathname == '/upload' && req.method == 'POST') {
        let body = '';
        var form = new formidable.IncomingForm();
          form.parse(req, function (err, fields, files) {
            var oldpath = files.file.path;
            var newpath = 'C:/Users/devel/Desktop/Demo-Mashup/FilesN/' + files.file.name;
            fs.appendFile('./FilesN/merged.txt', ' This is my text.', function (err) {
              if (err) throw err;
            });
            fs.rename(oldpath, newpath, function (err) {
              if (err) throw err;
                var forward_request = request.post({
                    url: 'http://localhost:8000/upload',
                    formData: {
                      attachments: [
                        fs.createReadStream(newpath)
                      ],
                    },
                    headers: {
                      'Content-type': 'multipart/form-data'
                    }
                  }, function (error, response, body) {
                    if (!error && response.statusCode == 200) {
                      console.dir('success')
                      res.writeHead(200, { });
                    }
                    else {
                      res.writeHead(500, { });
                    }
                    return res.end('done')
                });
            });
          });

          res.statusCode = 200;
        fs.readFile('./ontology.html',null,function(error,data){
          if (error) {
            res.writeHead(404);
            res.write('file not found');
          } else {
            res.write(data);
          }
          res.end();
        });
        
    } else {
    if (blackList.indexOf(reqUrl.pathname) > -1) {
      res.statusCode = 404;
      res.end('File not found');
    }
    serveStatic(req, res, require('finalhandler')(req, res));
  }
}).listen(process.env.PORT || 8080);