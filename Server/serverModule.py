# Forget abstracting
# Server will always need to first, verify connection
# Verify the user
# Then we can then go into the what the rest of apps want to do
# So maybe subclassing


# For each connection
# - Message Handling (Own encryoted messages)
# - - But once decrypted, can be sent to message handling for all users


# Message Handler (Singleton)
# - Takes a message + the current user (just added meta data)
# - Then handles it, and then finds the communication for that user and sends once done
# - - This is async. Maybe make some sort of worker. Sends reqyest and waits on a thread
# - Can take support for additional messages and there mappings

# Connection Handler (Singleton)
# Manged a list of connections
# can find a connection based on meta data like username
# Single thread to listent
# - Handles new connection, not the main server

# DB Handler (Singleton)
# Manages login stuff
# Extends to manage extra

# Encrytion Builder (Per Connection)
# - K will be different for each connection

# ServerModule
# - Message Handler (To Be Extended)
# - Connection Handler

# Lets say i want...
# A message to send a message to another user
# Message will be handled by Message handler
# Which i extend, and handled there
# Now need to speak to DB
# Ive extended DB handler
# How to get the two to speak? Raise an event from one
# Event includes, who the message is for (I.e DBModule)
# Plus the request
# Server listens to handler, then forwards the message (maybe its put on a queue, handled by another thread)
# Handler recieves, then forwards a response back if needed
# Some util worker that will wait for a response 

from abc import ABC, abstractmethod 
from __future__ import annotations

class Event(ABC):
    pass

class EventHandler(ABC): # Tests for allt his too

    @abstractmethod
    def onChange(event: Event) -> None:
        pass

    def listenTo(self, publisher: EventPublisher):
        publisher.register(self)


class EventPublisher(ABC):
    def __init__(self):
        self.observers: list[EventHandler] = []

    def publish(self, event: Event):
        for observer in self.observers:
            observer.onChange(event)
        
    def register(self, handler: EventHandler):
        self.observers += handler

    def unregister(self, handler: EventHandler):
        self.observers = [observer for observer in self.observers if observer != handler]


class MessageHandler:
    pass

class ConnectionHandler: # Does not need to be extended
    def __init__(self):
        self.__verifiedConnections = [] # These lists to only be handled by a single thread
        self.__unverifiedConnections = [] 

    def start(self):
        pass
     # Start listening

    def new_connection(self):
        pass

    # listen to Single Sub connection handler
    # Might raise event to

class Server:
    def __init__(self, messageHandler: MessageHandler):
        self.__messageHandler = messageHandler
        self.__connectionHandler = ConnectionHandler()

    def start(self):
        # Check DB, and apply changes
        # Add listeners to verythin
        self.__connectionHandler.start()
