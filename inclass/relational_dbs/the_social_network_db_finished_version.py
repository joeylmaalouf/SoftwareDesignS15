""" Experimenting again with Social Networks """
import sys
import pickle
from os.path import isfile
import MySQLdb as mdb


class SocialNetworkModel(object):
    """ Represents all of the data in our social networking App """
    def __init__(self, con):
        self.con = con
        self.users = []

    def add_user(self, user):
        """ Add the specified user to the network.
            If a user with the same first and last name already exists
            an error message is printed and the user is not added. """
        if self.lookup_user(user.first_name, user.last_name) != None:
            print "Tried to add duplicate user"
            return
        if self.con:
            if user.posts or user.friends:
                print "WARNING: ignoring posts and friends added before adding user"
            with self.con:
                cur = self.con.cursor()
                cur.execute("INSERT INTO Users(First_Name, Last_Name, Job, Favorite_Algorithm) VALUES('%s', '%s', '%s', '%s')" % (user.first_name,
                                                                                                                                  user.last_name,
                                                                                                                                  user.job,
                                                                                                                                  user.favorite_algorithm))
                cur.execute('SELECT LAST_INSERT_ID()')
                new_id = cur.fetchone()
                user.db_id = new_id[0]
        self.users.append(user)

    def make_friends(self, user_1, user_2):
        """ Create a friendship between the two specified users """
        if self.con:
            with self.con:
                cur = self.con.cursor()
                cur.execute("INSERT INTO Friends(User_1, User_2) VALUES(%i, %i)"% (user_1.db_id, user_2.db_id))
                cur.execute("INSERT INTO Friends(User_1, User_2) VALUES(%i, %i)"% (user_2.db_id, user_1.db_id))

        user_1.friends.append(user_2)
        user_2.friends.append(user_1)

    def post(self, user, text):
        """ Add a new post """
        if self.con:
            with self.con:
                cur = self.con.cursor()
                cur.execute("INSERT INTO Posts(User, Text) VALUES(%i, '%s')" % (user.db_id, text))
        user.posts.append(Post(text))

    def lookup_user(self, first_name, last_name):
        """ Return the user with the specified firt and last first
            or None if no such user exists """
        for u in self.users:
            if (u.first_name == first_name and
                u.last_name == last_name):
                return u
        return None

    def lookup_user_by_id(self, id):
        for u in self.users:
            if u.db_id == id:
                return u
        return None


class User(object):
    """ Represents a user in our social network """
    def __init__(self,
                 first_name,
                 last_name,
                 job,
                 favorite_algorithm,
                 db_id=None):
        """ Initializes a user with the specified information """
        self.first_name = first_name
        self.last_name = last_name
        self.job = job
        self.favorite_algorithm = favorite_algorithm
        self.db_id = db_id
        self.con = None
        self.posts = []
        self.friends = []

    def __str__(self):
        """ Returns the user object and all of their posts as a string """
        return_val = "%s %s (%s) really likes %s\n" % (self.first_name,
                                                       self.last_name,
                                                       self.job,
                                                       self.favorite_algorithm)
        return_val += "Posts:\n"
        for p in self.posts:
            return_val += "  " + str(p) + "\n"
        return_val += "Friends:"
        for f in self.friends:
            return_val += "\n  %s %s" %(f.first_name, f.last_name)
        return return_val


class Post(object):
    """ Represents a post that a user has made on our network """
    def __init__(self, text):
        """ Initialize a post object with the specified text """
        self.text = text

    def __str__(self):
        """ Return a Post as a string containing the post text """
        return self.text

class SocialNetworkTextView(object):
    """ A text-based view for our network """
    def __init__(self, model):
        """ Initialize the text view with the specified model """
        self.model = model

    def render(self):
        """ Render the view to the terminal """
        for i,u in enumerate(self.model.users):
            print "User %i: %s" % (i, u)


def reset_db(con):
    with con:
        cur = con.cursor()
        cur.execute("DROP TABLE IF EXISTS Users")
        cur.execute("DROP TABLE IF EXISTS Friends")
        cur.execute("DROP TABLE IF EXISTS Posts")
        cur.execute("CREATE TABLE Users(Id INT PRIMARY KEY AUTO_INCREMENT, \
                                        First_Name VARCHAR(25), \
                                        Last_Name VARCHAR(25), \
                                        Job VARCHAR(25), \
                                        Favorite_Algorithm VARCHAR(25))")
        cur.execute("CREATE TABLE Friends(Id INT PRIMARY KEY AUTO_INCREMENT, \
                                          User_1 INT, \
                                          User_2 INT)")
        cur.execute("CREATE TABLE Posts(Id INT PRIMARY KEY AUTO_INCREMENT, \
                                        User INT, \
                                        Text VARCHAR(255))")


def load_model(con):
    """ Load a model from the connected database """
    model = SocialNetworkModel(con)
    with con:
        cur = con.cursor(mdb.cursors.DictCursor)
        cur.execute("SELECT * FROM Users")
        users = cur.fetchall()
        for u in users:
            new_user = User(u['First_Name'],
                            u['Last_Name'],
                            u['Job'],
                            u['Favorite_Algorithm'],
                            u['Id'])
            model.users.append(new_user)

        cur.execute("SELECT * FROM Friends")
        friends = cur.fetchall()
        for f in friends:
            f_1 = model.lookup_user_by_id(f['User_1'])
            f_2 = model.lookup_user_by_id(f['User_2'])
            f_1.friends.append(f_2)

        cur.execute("SELECT * FROM Posts")
        posts = cur.fetchall()
        for p in posts:
            user = model.lookup_user_by_id(p['User'])
            user.posts.append(Post(p['Text']))

    return model


def save_model(pickle_filename, model):
    """ Save the model to the file 'pickle_filename' """
    pickle_file = open(pickle_filename, 'wt')
    pickle.dump(model, pickle_file)
    pickle_file.close()


if __name__ == "__main__":
    db_name = None
    overwrite_db = False

    if len(sys.argv) > 1:
        db_name = sys.argv[1]
    if len(sys.argv) > 2:
        overwrite_db = sys.argv[2] == "True"

    if db_name:
        con = mdb.connect('127.0.0.1', 'testuser', 'test623', db_name);
        if overwrite_db:
            reset_db(con)
        model = load_model(con)
    else:
        con = None
        model = SocialNetworkModel(con)

    if overwrite_db or not(db_name):
        paul = User("Paul", "Ruvolo", "Professor", "Policy Iteration")
        ben = User("Ben", "Hill", "Professor", "A-star")
        model.add_user(paul)
        model.add_user(ben)
        model.make_friends(paul, ben)
        model.post(paul, "Yay!")
        model.post(ben, "Sweet!")

    paul = model.lookup_user("Paul", "Ruvolo")
    model.post(paul, "post2")
    view = SocialNetworkTextView(model)
    view.render()
