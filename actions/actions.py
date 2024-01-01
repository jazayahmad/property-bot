from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.events import SlotSet, EventType, Restarted, ConversationResumed, ConversationPaused
from rasa_sdk.types import DomainDict
from rasa_sdk.executor import CollectingDispatcher


class ValidatePropertyForm(Action):
    def name(self) -> Text:
        return "property_form"
    def run(
        self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict
    ) -> List[EventType]:
        required_slots = ["location","numberOf_rooms", "rent_range"]
        for slot_name in required_slots:
            if tracker.slots.get(slot_name) is None:
                # The slot is not filled yet. Request the user to fill this slot next.
                return [SlotSet("requested_slot", slot_name)]

        # All slots are filled.
        return [SlotSet("requested_slot", None)]
class ActionSubmitCard(Action):
    def name(self) -> Text:
        return "action_submit"

    def run(
        self,
        dispatcher,
        tracker: Tracker,
        domain: "DomainDict",
    ) -> List[Dict[Text, Any]]:
        dispatcher.utter_message(response="utter_details", LOC=tracker.get_slot("location"),Rooms=tracker.get_slot("numberOf_rooms"), Rent = tracker.get_slot("rent_range"))



class ActionRestart(Action):

  def name(self) -> Text:
      return "action_restart"

  async def run(
      self, dispatcher, tracker: Tracker, domain: Dict[Text, Any]
  ) -> List[Dict[Text, Any]]:

      return [Restarted()]