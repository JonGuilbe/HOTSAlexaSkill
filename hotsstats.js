const express = require ('express');
const bodyParser = require('body-parser');
const app = express();
const request = require('request');
const Alexa = require('alexa-sdk');
exports.handler = function(event, context, callback){
    var alexa = Alexa.handler(event, context, callback);
    alexa.registerHandlers(handlers);
    alexa.execute();
};
app.use(bodyParser.json());
app.use(bodyParser.urlencoded({extended: true}));

var handlers = {
    'LaunchRequest': function (){
        var speechOutput = "Welcome to the Heroes of the Storm info skill. You can currently ask me for a hero build and I will try to get it from HOTS Logs .com";
        this.emit(':ask', speechOutput, "What would you like to do?");
    },
    'GetBuild': function(){
        let restUrl = 'http://jonguilbe.us/HOTS/herobuilds.json';
        var speechOutput = "Test " + this.event.request.slots.Hero.value;
        request.get(restUrl, (err, response, body) =>{
        if(!err && response.statusCode == 200){
            let json = JSON.parse(body);
            speechOutput = json[this.event.request.slots.Hero.value];
            
        }
        else{
            speechOutput = ("There seems to be a problem with looking up that hero...");
        }
        })
        console.log("Speech output is " + speechOutput);
        this.emit(':tell', speechOutput);
    }

}

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