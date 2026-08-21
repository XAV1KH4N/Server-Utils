from common.events.Events import Event, EventDesitination, EventOrigin

class VerifiedEvent(Event):
    def get_destination(self) -> EventDesitination:
        return EventDesitination.CLIENT_SERVER_HANDLER

    def get_origin(self) -> EventOrigin:
        return EventOrigin.MESSAGE_HANDLER
