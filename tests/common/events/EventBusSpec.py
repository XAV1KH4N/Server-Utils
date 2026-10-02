from unittest import TestCase, main
from common.events.EventBus import EventBus
from common.events.Events import Event,  EventOrigin, EventDesitination, EventHandler, EventPublisher

class TestEvents(TestCase):

    def test_valid(self):
        bus = EventBus()
        self.assertTrue(bus.is_valid())
        bus.dispose()

    def test_invalid(self):
        bus_1 = EventBus()
        bus_2 = EventBus()

        self.assertFalse(bus_1.is_valid())
        self.assertFalse(bus_2.is_valid())

        bus_1.dispose()
        bus_2.dispose()

    def test_subscribe_count_zero(self):
        bus = EventBus()
        self.assertEqual(bus.count(), 0)
        bus.dispose()

    def test_subscribe_count_one(self):
        bus = EventBus()
        bus.subscribe(TestHandler())
        self.assertEqual(bus.count(), 1)
        bus.dispose()

    def test_publish(self):
        bus = EventBus()
        handler = TestOnceHandler()
        bus.subscribe(handler)
        bus.publish(TestEvent())
        self.assertEqual(handler.count(), 1)
        bus.dispose()
    
    def test_publish_remove(self):
        bus = EventBus()
        handler = TestOnceHandler()

        self.assertEqual(bus.count(), 0)

        bus.subscribe(handler)
        self.assertEqual(bus.count(), 1)
        self.assertEqual(handler.count(), 0)

        bus.publish(TestEvent())
        self.assertEqual(handler.count(), 1)

        bus.unsubscribe(handler)
        self.assertEqual(handler.count(), 1)
        self.assertEqual(bus.count(), 0)

        bus.dispose()
        
class TestEvent(Event):

    def get_destination(self) -> Event:
        return EventDesitination.ALL

    def get_origin(self) -> EventOrigin:
        return EventOrigin.MESSAGE_HANDLER
    
class TestPublisher(EventPublisher):
    pass

class TestHandler(EventHandler):
    def __init__(self):
        self.__last_event = None

    def on_change(self, event: Event) -> None:
        self.__last_event = event

    def getLastEvent(self):
        return self.__last_event

class TestOnceHandler(EventHandler):
    def __init__(self):
        self.__events = 0

    def on_change(self, event: Event) -> None:
        self.__events += 1

    def count(self) -> int:
        return self.__events



if __name__ == '__main__':
    main()