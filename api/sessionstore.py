import base64
import os


class SessionStore:

    def __init__(self):
        ## data members:
        self.sessions = {}  # dictionary of diciotnaries, one per sessions
        return

    def createEmptySession(self):
        newSessionId = self.generateSessionId()
        # you should check if the id already exists
        self.sessions[newSessionId] = {}
        return newSessionId

    def generateSessionId(self):
        randomNum = os.urandom(32)
        randomStr = base64.b64encode(randomNum).decode("utf-8")
        return randomStr

    def loadSessionData(self, sessionId):
        # check for the key before it is loaded (prevent key error)
        if sessionId in self.sessions:
            return self.sessions[sessionId]
        else:
            return None
