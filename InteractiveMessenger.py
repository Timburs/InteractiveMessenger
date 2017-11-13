import fbchat
from fbchat.models import *
import os
from getpass import getpass


class fbContainer(object):
    """Class that holds information on FB account"""
    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.client = fbchat.Client(username, password)
        self.chats = []  # Stores 10 most recent conversations

    def getRecentChats(self):
        """ This function grabs a users' most recent conversations.
        :returns: List containing 10 recent chats
        """

        self.chats = self.client.fetchThreadList(offset=0, limit=10)
        return self.chats

    def interact(self, uid, index):
        """ Allows a user to converse with a specified user.
        :uid: The ID of the user to converse with
        :returns: None
        """

        thread_type = ThreadType.USER
        msg = ''
        while (True):
            os.system('clear')
            print "You are interacting with %s.  \
                   Type 'q' to quit" % (self.chats[index].name)
            messages = self.client.fetchThreadMessages(thread_id=uid, limit=10)
            messages.reverse()  # Put messages in correct order

            for message in messages:
                print '- ' + message.text
            msg = raw_input(">> ")
            if msg == 'q':
                break
            self.client.send(Message(text=msg), thread_id=uid,
                                    thread_type=thread_type)

    def logout(self):
        """ Logs the user out """

        self.client.logout()
        print "Logout successful\n"


def main():

    username = "timmyn7@gmail.com"
    password = getpass()
    fb = fbContainer(username, password)

    os.system('clear')
    choice = ''
    chats = fb.getRecentChats()  # Grab chats to pre-populate array
    printHeader()

    while choice != '2':
        printChoices()
        choice = raw_input(">> ")

        if ' ' in choice:
            choice, index = choice.split(' ', 1)

        if choice == 'v':
            os.system('clear')
            chats = fb.getRecentChats()
            for i in range(len(chats)):
                print "%d) %s" % (i, chats[i].name)

        elif choice == 'i':
            fb.interact(int(fb.chats[int(index)].uid), int(index))

        elif choice == 'q':
            print "Logging out of %s..\n" % (username)
            fb.logout()
            break


def printChoices():
    """ This function prints the menu for choices. """

    print "\n'v' :  View Recent Chats\n" \
          "'i' : Interact with specified user \n" \
          "'q' : Quit \n"


def printHeader():
    """ This function prints the header. """

    print "Welcome to FB for Terminal. \n" \
          "To interact, type i + n, where n is index of user listed in 'v'\n"


main()
