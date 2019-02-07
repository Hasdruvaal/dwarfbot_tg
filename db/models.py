from peewee import *


db = SqliteDatabase("database.db")


class BaseModel(Model):
    class Meta:
        database = db


class User(BaseModel):
    userId = IntegerField(primary_key=True)
    pmId = IntegerField()


class Session(BaseModel):
    sessionId = IntegerField(primary_key=True)
    name = TextField()
    curator = ForeignKeyField(User)
    chatId = IntegerField()


class UserSession(BaseModel):
    user = ForeignKeyField(User)
    session = ForeignKeyField(Session)


class SessionManager:
    def initialise():
        db.create_tables([User, Session, UserSession])

    # returns sessionId
    def createSession(name, curatorId, chatId):
        curator = User.get(userId=curatorId)
        query = Session.select().where((Session.curator == curator) &
                                       (Session.chatId == chatId))
        if not query.exists():
            Session.create(name=name, curator=curator, chatId=chatId)
            return True
        return False

    #returns bool
    def checkUser(userId):
        return User.select().where(User.userId == userId).exists()

    # returns bool
    def addUser(userId, chatId):
        if (not SessionManager.checkUser(userId)):
            user = User.create(userId=userId, pmId=chatId)
            return True
        else:
            return False

    # returns bool
    def deleteSession(curatorId, chatId):
        curator = User.get(userId=curatorId)
        query = Session.select().where((Session.curator == curator) &
                                       (Session.chatId == chatId))
        if (query.exists()):
            query.get().delete_instance()
            return True
        else:
            return False

    # returns playerId[]
    def getPlayersList(sessionId):
        session = Session.get(sessionId=sessionId)
        players = UserSession.select().where(UserSession.session == session).get()
        playerIds = list(map(lambda x: x.userId, players))
        return playerIds

    # returns bool
    def togglePlayer(sessionId, userId):
        assert SessionManager.checkUser(userId)
        session = Session.get(sessionId=sessionId)
        user = User.get(userId=userId)
        query = UserSession.select().where(
            UserSession.session == session &
            UserSession.user == user)
        if (not query.exists()):
            entry = UserSession.create(session=session, user=user)
            return True
        else:
            query.get().delete_instance()
            return False

    # returns playerId[]
    def shufflePlayers(curatorId, sessionId):
        return # TODO:

    # returns sessionId[]
    def getChatSessionsList(chatId):
        return # TODO:

    # returns playerId[]
    def getPlayerSessionsList(playerId):
        return # TODO:

    # returns Session
    def readSession(sessionId):
        return # TODO:

    # returns bool
    def writeSession(sessionId):
        return # TODO:
