import datetime


class User:
    def __init__(self, id: int, username: str):
        self.id = id
        self.username = username
        self.created_at = datetime.datetime.now()


class Chat:
    def __init__(self, id: int, name: str, users: list):
        self.id = id
        self.name = name
        self.users = users
        self.created_at = datetime.datetime.now()


class Message:
    def __init__(self, id: int, chat: Chat, author: User, text: str):
        self.id = id
        self.chat = chat
        self.author = author
        self.text = text
        self.created_at = datetime.datetime.now()


class UserStorage:
    def __init__(self):
        self.__RECORDS = {}
        self.id_counter = 0

    def add_user(self, username: str) -> User:
        user = User(self.id_counter, username)
        self.__RECORDS[user.id] = user
        self.id_counter += 1
        return user

    def get_user(self, user_id: int) -> User:
        return self.__RECORDS.get(user_id)

    def get_users(self) -> list[User]:
        return self.__RECORDS.values()


class ChatStorage:
    def __init__(self):
        self.__RECORDS = {}
        self.id_counter = 0

    def add_chat(self, name: str, users: list) -> Chat:
        chat = Chat(self.id_counter, name, users)
        self.__RECORDS[chat.id] = chat
        self.id_counter += 1
        return chat

    def get_chat(self, chat_id: int) -> Chat:
        return self.__RECORDS.get(chat_id)

    def get_chats_for_user(self, user: User) -> list[Chat]:
        return list(filter(lambda c: user in c.users, self.__RECORDS.values()))


class MessageStorage:
    def __init__(self):
        self.__RECORDS = {}
        self.id_counter = 0

    def add_message(self, chat: Chat, author: User, text: str) -> Message:
        message = Message(self.id_counter, chat, author, text)
        self.__RECORDS[message.id] = message
        self.id_counter += 1
        return message

    def get_message(self, message_id: int) -> Message:
        return self.__RECORDS.get(message_id)

    def get_messages_in_chat(self, chat: Chat) -> list[Message]:
        return list(filter(lambda m: m.chat == chat, self.__RECORDS.values()))

class UserService:
    def __init__(self, user_storage: UserStorage):
        self.user_storage = user_storage

    def create_user(self, username: str):
        return self.user_storage.add_user(username).id

class ChatService:
    def __init__(self, user_storage: UserStorage, chat_storage: ChatStorage):
        self.user_storage = user_storage
        self.chat_storage = chat_storage
    
    def create_chat(self, name: str, users_ids: list[int]):
        users = [self.user_storage.get_user(user_id) for user_id in users_ids]
        return self.chat_storage.add_chat(name, users).id
    
    def get_user_chats(self, user_id: int):
        user = self.user_storage.get_user(user_id)
        chats = self.chat_storage.get_chats_for_user(user)
        return sorted(chats, key=lambda c: c.created_at)

class MessageService:
    def __init__(self, user_storage: UserStorage, chat_storage: ChatStorage, message_storage: MessageStorage):
        self.user_storage = user_storage
        self.chat_storage = chat_storage
        self.message_storage = message_storage
    
    def send_message(self, from_user_id: int, to_chat_id: int, text: str):
        user = self.user_storage.get_user(from_user_id)
        chat = self.chat_storage.get_chat(to_chat_id)
        assert user in chat.users, "User is not a member in chat"
        self.message_storage.add_message(chat, user, text)
    
    def get_messages_in_chat(self, chat_id: int):
        chat = self.chat_storage.get_chat(chat_id)
        messages = self.message_storage.get_messages_in_chat(chat)
        return sorted(messages, key=lambda m: m.created_at, reverse=True)
