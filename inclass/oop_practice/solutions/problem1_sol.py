""" A practice problem for object-oriented programming """

class Date(object):
    """ Represents a particular day on the calendar """
    def __init__(self, month, day, year):
        """ Initializes a Date object

            month: the month (represented as an integer in [1,12])
            day: the day of the month (represented as an integer)
            year: the year (represented as an integer)
            This method will not validate whether a given date is invalid
            (e.g. April 31, 2000) """
        self.month = month
        self.day = day
        self.year = year

    def is_before(self,other_date):
        """ Returns true if and only if self occurs before other_date

            >>> d1 = Date(4,20,1981)
            >>> d2 = Date(5,31,1995)
            >>> d1.is_before(d2)
            True
        """
        if self.year < other_date.year:
            return True
        elif self.month < other_date.month:
            return True
        else:
            return self.day < other_date.day

    def __str__(self):
        """ Converts the date to a string in the following format:
            Month, Day Year (where Month is the name of the month, e.g. January)

        >>> print Date(3,26,2015)
        March, 26th 2015
        """
        month_map = {1 : "January",
                     2 : "February",
                     3 : "March",
                     4 : "April",
                     5 : "May",
                     6 : "June",
                     7 : "July",
                     8 : "August",
                     9 : "September",
                     10 : "October",
                     11 : "November",
                     12 : "December"}
        last_digit_suffix = {0 : "th",
                             1 : "st",
                             2 : "nd",
                             3 : "rd",
                             4 : "th",
                             5 : "th",
                             6 : "th",
                             7 : "th",
                             8 : "th",
                             9 : "th"}
        return "%s, %i%s %i" % (month_map[self.month],
                                self.day,
                                last_digit_suffix[self.day % 10],
                                self.year)

    def increment_year(self):
        """ Modifies the Date object self so that it represents a date of the
            same month and day but for the following year. """
        self.year += 1

    def is_leap_year(self):
        """ Returns true if the year that this date falls in is a leap year
            see: http://en.wikipedia.org/wiki/Leap_year

            >>> Date(3,5,2000).is_leap_year()
            True
            >>> Date(5,4,1999).is_leap_year()
            False
            >>> Date(5,1,1900).is_leap_year()
            False
        """
        if self.year % 4 != 0:
            return False
        if self.year % 100 != 0:
            return True
        return self.year % 400 == 0

if __name__ == '__main__':
    import doctest
    doctest.testmod()