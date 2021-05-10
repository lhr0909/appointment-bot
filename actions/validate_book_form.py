import logging
from typing import Text, List, Any, Dict, Optional

from rasa_sdk import Tracker, FormValidationAction
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.types import DomainDict

from .calendar import get_available_time_slots, book_appointment

logger = logging.getLogger(__name__)


def extract_range_value(range_value: str):
    return [int(x) if x is not None and isinstance(x, str) and len(x) > 0 else 0 for x in range_value[1:-1].split(',')]


class ValidateBookForm(FormValidationAction):
    def name(self) -> Text:
        return "validate_book_form"

    async def required_slots(
        self,
        slots_mapped_in_domain: List[Text],
        dispatcher: "CollectingDispatcher",
        tracker: "Tracker",
        domain: "DomainDict",
    ) -> Optional[List[Text]]:
        logger.info("required_slots is called")
        return [
            "appointment_item",
            "appointment_time",
        ]

    def validate_appointment_item(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:
        appointment_item_slot = tracker.slots.get("appointment_item")
        if appointment_item_slot is None or appointment_item_slot == "unknown":
            return {"appointment_item": slot_value}
        else:
            return {"appointment_item": appointment_item_slot}

    def validate_appointment_time(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:
        appointment_item_slot = tracker.slots.get("appointment_item")
        duration_hour_slot = tracker.slots.get("duration_hour")
        appointment_time_slot = tracker.slots.get("appointment_time")
        time_slot = tracker.slots.get("time")
        if time_slot is not None:
            time_slot = time_slot.get("additional_info", {})

        if appointment_time_slot is None or appointment_time_slot == "unknown":
            if time_slot is None:
                return {"appointment_time": slot_value}
            else:
                time_from = time_slot.get('from', {}).get('value')
                time_to = time_slot.get('to', {}).get('value')
                time_slots = get_available_time_slots(time_from, time_to, duration_hour_slot)
                return {"appointment_time": None, "suggested_times": time_slots}
        else:
            appointment_time = book_appointment(appointment_time_slot, duration_hour_slot, appointment_item_slot)
            return {"appointment_time": appointment_time}

    async def extract_appointment_item(
        self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict
    ) -> Dict[Text, Any]:
        appointment_item_slot = tracker.slots.get("appointment_item")
        # requested_slot_slot = tracker.slots.get("requested_slot")

        if appointment_item_slot != '理发' and appointment_item_slot != '染发':
            # TODO: add more here
            return {"appointment_item": None}

        if appointment_item_slot == '理发':
            duration_hour = 1

        if appointment_item_slot == '染发':
            duration_hour = 3

        return {"appointment_item": appointment_item_slot, "duration_hour": duration_hour}

    async def extract_appointment_time(
        self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict
    ) -> Dict[Text, Any]:
        appointment_time_slot = tracker.slots.get("appointment_time", "unknown")
        requested_slot_slot = tracker.slots.get("requested_slot")

        if appointment_time_slot is not None and appointment_time_slot != 'unknown' and requested_slot_slot != "appointment_time":
            return {"appointment_time": appointment_time_slot}

        if appointment_time_slot is None and requested_slot_slot == "appointment_time":
            appointment_time_slot = "unknown"

        entities = tracker.latest_message.get("entities", [])

        if len(entities) == 0:
            return {"appointment_time": appointment_time_slot}

        time_entities = list(filter(lambda e: e.get(
            "entity", "").startswith("time"), entities))
        if len(time_entities) == 0:
            return {"appointment_time": appointment_time_slot}

        time_entity = time_entities[0]
        logger.debug(time_entity)
        time_additional_info = time_entity.get("additional_info", {})
        time_type = time_additional_info.get("type")
        time_granularity = time_additional_info.get("grain")
        if time_type == "value" and time_granularity == "hour":
            appointment_time = time_entity.get("value")
        else:
            return {"time": time_entity, "appointment_time": None}

        return {"time": None, "appointment_time": appointment_time}
