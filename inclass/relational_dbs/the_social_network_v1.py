""" Experimenting (again) with Social Networks.  Gonna strike it rich! """
import sys


class SocialNetworkModel(object):
    """ Represents all of the data in our social networking App """
    def __init__(self):
        self.users = []

    def add_user(self, user):
        """ Add the specified user to the network.
            If a user with the same first and last name already exists
            an error message is printed and the user is not added. """
        if self.lookup_user(user.first_name, user.last_name) != None:
            print "Tried to add duplicate user"
            return
        self.users.append(user)

    def make_friends(self, user_1, user_2):
        """ Create a friendship between the two specified users """
        user_1.friends.append(user_2)
        user_2.friends.append(user_1)

    def post(self, user, text):
        """ Add a post from the specified user with the specified text """
        user.posts.append(Post(text))

    def lookup_user(self, first_name, last_name):
        """ Return the user with the specified first and last name
            or None if no such user exists """
        for u in self.users:
            if (u.first_name == first_name and
                u.last_name == last_name):
                return u
        return None


class User(object):
    """ Represents a user in our social network """
    def __init__(self,
                 first_name,
                 last_name,
                 job,
                 favorite_algorithm):
        """ Initializes a user with the specified information """
        self.first_name = first_name
        self.last_name = last_name
        self.job = job
        self.favorite_algorithm = favorite_algorithm
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


if __name__ == "__main__":
    model = SocialNetworkModel()
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
