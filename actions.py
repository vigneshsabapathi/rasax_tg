
from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet
from weather import Weather


class ActionSearchSuggest(Action):
#
    def name(self) -> Text:
        return "actions_search_suggest"

    def run(self, dispatcher: CollectingDispatcher,

            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        import gspread
        from oauth2client.service_account import ServiceAccountCredentials
        scope = ['https://www.googleapis.com/auth/drive']

        credentials = ServiceAccountCredentials.from_json_keyfile_name('gsconfig.json' , scope)

        client = gspread.authorize(credentials)

        sheet = client.open('rasatest').sheet1
        data = sheet.get_all_records()

        response = "Ok, Here you go \n Is it a) " + data +  "?"
        
        dispatcher.utter_message(response)
        
        print(tracker.events)
        
        dispatcher.utter_message(text='Here are your search results')
        return[]

class ActionWeatherApi(Action):

    def name(self) -> Text:
        return "action_weather_api"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        city=tracker.latest_message['text']
        temp=int(Weather(city)['temp']-273)
        dispatcher.utter_template("utter_temp",tracker,temp=temp)

        return []