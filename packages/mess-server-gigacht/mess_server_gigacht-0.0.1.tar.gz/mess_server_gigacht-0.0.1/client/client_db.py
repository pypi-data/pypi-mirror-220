from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.sql import default_comparator


class ClientStorage:
    '''
    Declares clients database and methods to work with it.
    Uses SQLite and SQLAlchemy ORM.
    '''

    Base = declarative_base()

    class MessageHistory(Base):
        '''Table to store message history.'''
        __tablename__ = 'message_history'
        id = Column(Integer, primary_key=True)
        sender_name = Column(String)
        receiver_name = Column(String)
        message = Column(String)

        def __init__(self, sender_name, receiver_name, message):
            self.sender_name = sender_name
            self.receiver_name = receiver_name
            self.message = message

        def __repr__(self):
            return f'Message #{self.id}. User {self.sender_name} wrote to {self.receiver_name } {self.message}'

    class Contacts(Base):
        '''Table to store user's contacts.'''
        __tablename__ = 'contacts'
        name = Column(String, primary_key=True)

        def __init__(self, name):
            self.name = name

        def __repr__(self):
            return f'Contact {self.name}.'

    def __init__(self):
        '''Initialyzes database and creates tables'''
        self.engine = create_engine(
            'sqlite:///:memory:',
            echo=False,
            pool_recycle=7200,
            connect_args={
                'check_same_thread': False})
        Session = sessionmaker(bind=self.engine)
        self.session = Session()
        # Create tables
        self.Base.metadata.create_all(self.engine)

    def save_message(self, sendername, receivername, message):
        '''Saves message with sender and receiver names to MessageHistory table'''
        new_message = self.MessageHistory(sendername, receivername, message)
        self.session.add(new_message)
        self.session.commit()

    def save_contact(self, name):
        '''Add new contacts to Contacts table'''
        rez = self.session.query(self.Contacts).filter_by(name=name)
        if not rez.count():
            new_contact = self.Contacts(name)
            self.session.add(new_contact)
            self.session.commit()

    def get_contacts(self):
        '''Returns list of contacts from Contacts table'''
        rez = self.session.query(self.Contacts)
        contacts = []
        for i in rez:
            contacts.append(i.name)
        return contacts

    def get_history(self):
        '''Returns message history as list of tuples'''
        rez = self.session.query(self.MessageHistory)
        messages = []
        for i in rez:
            messages.append((i.id, i.sender_name, i.receiver_name, i.message))
        return messages


if __name__ == '__main__':
    storage = ClientStorage()
    storage.save_message('vasia', "petia", "I love you")
    storage.save_contact('petia')
    storage.save_message('petia', "vasia", "I love you too")
    storage.save_contact('igor')
    print(storage.get_contacts())
    print(storage.get_history())
