# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions

API_PATH = "https://3333-plum-egret-wx8hj8rw.ws-us18.gitpod.io"

# This is a simple example for a custom action which utters "Hello World!"

    from typing import Any, Text, Dict, List
#
    from rasa_sdk import Action, Tracker
    from rasa_sdk.executor import CollectingDispatcher
#
#
class ActionExclusionSelect(Action):

    def name(self) -> Text:
        return "action_delete_case_selection"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        

        id = str(tracker.get_slot('ong_id'))
        print("Deletando.." + id)
        
        if(id and id != "" and id != "None"):
            
            r = requests.get(API_PATH+ '/ongs/'+str(id))  
            if(int(r.status_code)==404):
                dispatcher.utter_message(text ="Não há casos para serem excluidos ou id incorreto")
                return
            if(int(r.status_code)==500 or int(r.status_code)==401 ):
                dispatcher.utter_message(text ="Pera que eu fiquei confuso.... deu um errinho aqui kk vamos de novo!")
                return
            print(r.json())
            cases = r.json()

            btns = []
            for i in range(len(cases)):
                btns.append({"payload":'/delete_specific_case{"case_id":"'+str(cases[i]["id"])+'"}',"title":cases[i]["title"]})
            btns.append({"payload":"/cancel_operation","title":"Nenhum"})
            dispatcher.utter_message(text="Escolha qual caso quer excluir", buttons=btns)
        else:
            dispatcher.utter_message(text ="Id não informado, ou está incorreto")
        return []
