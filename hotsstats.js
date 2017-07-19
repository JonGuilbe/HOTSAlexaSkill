const bodyParser = require('body-parser');
//const app = express();
const request = require('request');
const Alexa = require('alexa-sdk');
exports.handler = function(event, context, callback){
    var alexa = Alexa.handler(event, context, callback);
    alexa.registerHandlers(handlers);
    alexa.execute();
};
//app.use(bodyParser.json());
//app.use(bodyParser.urlencoded({extended: true}));

var handlers = {
    'LaunchRequest': function (){
         this.attributes['speechOutput'] = "Welcome to the Heroes of the Storm info skill. You can currently ask me for a hero build and I will try to get it from HOTS Logs .com";
         this.attributes['repromptSpeech'] = "What would you like to do?";
        this.emit(':ask', this.attributes['speechOutput'], this.attributes['repromptSpeech']);
    },
    'GetBuild': function(){
        let restUrl = 'http://jonguilbe.us/HOTS/herobuilds.json';
        var heroName = (this.event.request.intent.slots.Hero.value); // Special cases for ' and spaced out names!
        var speechOutput = "Test " + heroName.charAt(0).toUpperCase() + heroName.slice(1);   
        request.get(restUrl, (err, response, body) =>{
        if(!err && response.statusCode == 200){
            console.log("We successfully grabbed what we needed!");
            let json = JSON.parse(body);
            speechOutput = json[heroName.charAt(0).toUpperCase() + heroName.slice(1)];
            console.log("Output is currently " + speechOutput);
            this.emit(':tell', speechOutput);
            
        }
        else{
            speechOutput = ("There seems to be a problem with looking up that hero...");
        }
        })
        console.log("Speech output is " + speechOutput);
        //this.emit(':tell', speechOutput);
    }

}

/*const server = app.listen(process.env.PORT || 5001, () => {
    console.log('Express server listening on port %d in %s mode', server.address().port, app.settings.env);
}); */

/*
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
*/