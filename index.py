from __future__ import print_function
from bs4 import BeautifulSoup
from urllib.request import urlopen

def lambda_handler(event, context):

    print("event.session.application.applicationId" +
        event['session']['application']['applicationId'])

    if event['session']['new']:
        on_session_started({'requestId': event['request']['requestId']},
                           event['session'])
    
    if event['request']['type'] == "LaunchRequest":
        return on_launch(event['request'], event['session'])
    elif event['request']['type'] == "IntentRequest":
        return on_intent(event['request'], event['session'])
    elif event['request']['type'] == "SessionEndedRequest":
        return on_session_ended(event['request'], event['session'])


def on_session_started(session_started_request, session):
    print("on_session_started requestId=" + session_started_request['requestId']
          + ", sessionId=" + session['sessionId'])

def on_launch(launch_request, session):
    return get_welcome_response()

def on_intent(intent_request, session):
    print("on_intent requestId=" + intent_request['requestId'] +
          ", sessionId=" + session['sessionId'])

    intent = intent_request['intent']
    intent_name = intent_request['intent']['name']
    
    if intent_name == "GetBuild":
        return get_build(intent_request)
    elif intent_name == "GetTalent":
        return get_talent(intent_request)
    elif intent_name == "AMAZON.HelpIntent":
        return get_help_response()
    elif intent_name == "AMAZON.CancelIntent" or intent_name == "AMAZON.StopIntent":
        return handle_session_end_request()
    else:
        raise ValueError("Invalid intent")

def on_session_ended(session_ended_request, session):
    print("on_session_ended requestId=" + session_ended_request['requestId'] +
          ", sessionId=" + session['sessionId'])

def get_welcome_response():
    session_attributes = {}
    card_title = "Welcome"
    speech_output = "Welcome to the Heroes of the Storm Info Skill. You can ask me for the best builds or talent choices at a particular level. For examples of what you can say, ask me for help."
    reprompt_text = speech_output
    should_end_session = False
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))

def get_help_response():
    session_attributes = {}
    card_title = "Help"
    speech_output = "I can currently find information on 2 things. I can either find the highest win rate build for a particular hero, or find the highest winrate talent for a hero at a particular talent tier. You can say something like what is the top build for Li Li or level 4 for Li Ming."
    reprompt_text = speech_output
    should_end_session = False
    return build_response(session_attributes, build_speechlet_response(card_title,speech_output,reprompt_text,should_end_session))

def get_build(intent_request):
    session_attributes = {}
    card_title = "Hero_Build"
    speech_output = ""
    heroRequest = intent_request["intent"]["slots"]["Hero"]["value"]

    #Insert HTML Extracting Logic Here
    page = 'https://www.hotslogs.com/Sitewide/HeroDetails?Hero=' + heroRequest
    actualPage = urlopen(page)
    soup = BeautifulSoup(actualPage, 'html.parser')
    info = soup.find(id="ctl00_MainContent_RadGridPopularTalentBuilds_ctl00__0")
    info = info.find_all("td", style="display:none;")
    speech_output = "Level 1, " + info[0].text.strip + "level 4, "+ info[1].text.strip + "level 7, "+ info[2].text.strip + "level 10, "+ info[3].text.strip + "level 13, "+ info[0].text.strip + "level 16, "+ info[0].text.strip + "level 20, "

    #End of Logic

    #speech_output = "You said you wanted a build for " + heroRequest + ", but I can't do that just yet. Sorry!"
    reprompt_text = speech_output
    should_end_session = True
    return build_response(session_attributes, build_speechlet_response(card_title,speech_output,reprompt_text,should_end_session))

def get_talent():
    session_attributes = {}
    card_title = "Hero_Build"
    speech_output = ""
    talentRequest = intent_request["intent"]["slots"]["Talents"]["value"]
    heroRequest = intent_request["intent"]["slots"]["Hero"]["value"]

    #Insert HTML Extracting Logic Here
    speech_output = "You said you wanted a talent for " + heroRequest + " at level " + levelRequest + ", but I can't do that just yet. Sorry!"
    reprompt_text = speech_output
    should_end_session = True
    return build_response(session_attributes, build_speechlet_response(card_title,speech_output,reprompt_text,should_end_session))

def handle_session_end_request():
    card_title = "Session End"
    speech_output = "Thank you for using Heroes of the Storm Info. If something's wrong, please yell at Jon as always."
    should_end_session = True
    return build_response({}, build_speechlet_response(
        card_title, speech_output, None, should_end_session))

def build_speechlet_response(title, output, reprompt_text, should_end_session):
    return {
        'outputSpeech': {
            'type': 'PlainText',
            'text': output
        },
        'card': {
            'type': 'Simple',
            'title': 'SessionSpeechlet - ' + title,
            'content': 'SessionSpeechlet - ' + output
        },
        'reprompt': {
            'outputSpeech': {
                'type': 'PlainText',
                'text': reprompt_text
            }
        },
        'shouldEndSession': should_end_session
    }


def build_response(session_attributes, speechlet_response):
    return {
        'version': '1.0',
        'sessionAttributes': session_attributes,
        'response': speechlet_response
    }