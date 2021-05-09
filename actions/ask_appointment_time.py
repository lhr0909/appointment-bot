from typing import Dict, Text, List

from rasa_sdk import Tracker
from rasa_sdk.events import EventType, SlotSet
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk import Action


class AskForAppointmentTimeSlotAction(Action):
    def name(self) -> Text:
        return "action_ask_appointment_time"

    def run(
        self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict
    ) -> List[EventType]:
        events = []

        duration_announced_slot = tracker.slots.get("duration_announced")
        duration_hour_slot = tracker.slots.get("duration_hour")
        suggested_times_slot = tracker.slots.get("suggested_times", [])
        time_slot = tracker.slots.get("time", {})

        if duration_announced_slot != True:
            dispatcher.utter_message(response="utter_acknowledge")
            dispatcher.utter_message(response="utter_duration", duration_hour=duration_hour_slot)
            events.append(SlotSet("duration_announced", True))

        if suggested_times_slot is not None:
            dispatcher.utter_message(response="utter_ask_accurate_time", appointment_time=time_slot.get("text"))
            dispatcher.utter_message('\n'.join(suggested_times_slot))

        dispatcher.utter_message(response="utter_ask_appointment_time")
        return events
