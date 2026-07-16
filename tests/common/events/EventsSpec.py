from unittest import TestCase, main
from common.events.Events import Event,  EventOrigin, EventDesitination, EventHandler, EventPublisher

class TestEvents(TestCase):

    def test_event(self):
        handler = TestHandler()
        publisher = TestPublisher()
        event = TestEvent("1234")

        publisher.register(handler)
        self.assertIsNone(handler.getLastEvent())

        publisher.publish(event)

        last_event = handler.getLastEvent()
        is_instance = isinstance(last_event, TestEvent)
        self.assertTrue(is_instance)
        if (is_instance):
            self.assertEqual(last_event.getData(), "1234")        

    def test_multiple_event(self):
        handler_1 = TestHandler()
        handler_2 = TestHandler()
        handler_3 = TestHandler()

        publisher = TestPublisher()
        event = TestEvent("abc")

        publisher.register(handler_1)
        publisher.register(handler_2)

        self.assertIsNone(handler_1.getLastEvent())
        self.assertIsNone(handler_2.getLastEvent())
        self.assertIsNone(handler_3.getLastEvent())

        publisher.publish(event)

        last_event_1 = handler_1.getLastEvent()
        is_instance_1 = isinstance(last_event_1, TestEvent)
        self.assertTrue(is_instance_1)
        if (is_instance_1):
            self.assertEqual(last_event_1.getData(), "abc")    

        last_event_2 = handler_2.getLastEvent()
        is_instance_2 = isinstance(last_event_2, TestEvent)
        self.assertTrue(is_instance_2)
        if (is_instance_2):
            self.assertEqual(last_event_2.getData(), "abc")   

        self.assertIsNone(handler_3.getLastEvent())

    def test_remove(self):
        handler_1 = TestHandler()
        handler_2 = TestHandler()

        publisher = TestPublisher()
        event = TestEvent("qwer")

        publisher.register(handler_1)
        publisher.register(handler_2)

        self.assertIsNone(handler_1.getLastEvent())
        self.assertIsNone(handler_2.getLastEvent())

        publisher.publish(event)

        last_event_1 = handler_1.getLastEvent()
        is_instance_1 = isinstance(last_event_1, TestEvent)
        self.assertTrue(is_instance_1)
        if (is_instance_1):
            self.assertEqual(last_event_1.getData(), "qwer")    

        last_event_2 = handler_2.getLastEvent()
        is_instance_2 = isinstance(last_event_2, TestEvent)
        self.assertTrue(is_instance_2)
        if (is_instance_2):
            self.assertEqual(last_event_2.getData(), "qwer")   

        publisher.unregister(handler_2)

        event_2 = TestEvent("asdf")
        publisher.publish(event_2)

        last_event_1 = handler_1.getLastEvent()
        is_instance_1 = isinstance(last_event_1, TestEvent)
        self.assertTrue(is_instance_1)
        if (is_instance_1):
            self.assertEqual(last_event_1.getData(), "asdf")    

        last_event_2 = handler_2.getLastEvent()
        is_instance_2 = isinstance(last_event_2, TestEvent)
        self.assertTrue(is_instance_2)
        if (is_instance_2):
            self.assertEqual(last_event_2.getData(), "qwer")   

        
class TestEvent(Event):
    def __init__(self, data: str):
        self.__data = data

    def getDestination(self) -> Event:
        return EventDesitination.ALL

    def getOrigin(self) -> EventOrigin:
        return EventOrigin.MESSAGE_HANDLER

    def getData(self) -> str:
        return self.__data
    
class TestPublisher(EventPublisher):
    pass

class TestHandler(EventHandler):
    def __init__(self):
        self.__last_event = None

    def on_change(self, event: Event) -> None:
        self.__last_event = event

    def getLastEvent(self):
        return self.__last_event




if __name__ == '__main__':
    main()