const express = require ('express');
const bodyParser = require('body-parser');
const app = express();
const request = require('request');
app.use(bodyParser.json());
app.use(bodyParser.urlencoded({extended: true}));

const server = app.listen(process.env.PORT || 5001, () => {
    console.log('Express server listening on port %d in %s mode', server.address().port, app.settings.env);
});

function doThing(){
    let restUrl = 'http://jonguilbe.us/HOTS/herobuilds.json'
    request.get(restUrl, (err, response, body) =>{
        if(!err && response.statusCode == 200){
            let json = JSON.parse(body);
            let msg = json.Rexxar;
            console.log(msg);
        }
        else{
            console.log("I have no idea what I'm doing! Status code is %s", response.statusCode);
        }
    })
}

function main(){
    console.log("Yes");
    doThing();
    console.log("No");
}
main();