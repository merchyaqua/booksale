import os
import requests
import urllib.parse
import decimal
from flask import redirect, render_template, request, session, flash
from functools import wraps


def apology(message, code=400):
    """Render message as an apology to user."""
    def escape(s):
        """
        Escape special characters.

        https://github.com/jacebrowning/memegen#special-characters
        """
        for old, new in [("-", "--"), (" ", "-"), ("_", "__"), ("?", "~q"),
                         ("%", "~p"), ("#", "~h"), ("/", "~s"), ("\"", "''")]:
            s = s.replace(old, new)
        return s
    return render_template("apology.html", code=code, message=message)


def login_required(f):
    """
    Decorate routes to require login.

    http://flask.pocoo.org/docs/1.0/patterns/viewdecorators/
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function


def usd(value):
    """Format value as USD."""
    return f"${value:,.2f}"

#!/usr/bin/env python
# from website
def ordinal(value):
    """
    Converts zero or a *postive* integer (or their string
    representations) to an ordinal value.

    >>> for i in range(1,13):
    ...     ordinal(i)
    ...
    u'1st'
    u'2nd'
    u'3rd'
    u'4th'
    u'5th'
    u'6th'
    u'7th'
    u'8th'
    u'9th'
    u'10th'
    u'11th'
    u'12th'

    >>> for i in (100, '111', '112',1011):
    ...     ordinal(i)
    ...
    u'100th'
    u'111th'
    u'112th'
    u'1011th'

    """
    try:
        value = int(value)
    except ValueError:
        return value

    if value % 100//10 != 1:
        if value % 10 == 1:
            ordval = u"%d%s" % (value, "st")
        elif value % 10 == 2:
            ordval = u"%d%s" % (value, "nd")
        elif value % 10 == 3:
            ordval = u"%d%s" % (value, "rd")
        else:
            ordval = u"%d%s" % (value, "th")
    else:
        ordval = u"%d%s" % (value, "th")

    return ordval

# Converts a list of SQL Alchemy RowProxy objects into a list of dictionary objects with the column name as the key (https://github.com/cs50/python-cs50/blob/develop/src/cs50/sql.py#L328)
# Used for SQL SELECT .fetchall() results
def convertSQLToDict(listOfRowProxy):
    # Coerce types
    rows = [dict(row) for row in listOfRowProxy]
    for row in rows:
        for column in row:

            # Coerce decimal.Decimal objects to float objects
            # https://groups.google.com/d/msg/sqlalchemy/0qXMYJvq8SA/oqtvMD9Uw-kJ
            if type(row[column]) is decimal.Decimal:
                row[column] = float(row[column])

            # Coerce memoryview objects (as from PostgreSQL's bytea columns) to bytes
            elif type(row[column]) is memoryview:
                row[column] = bytes(row[column])

    return rows



if __name__ == '__main__':
    import doctest
    doctest.testmod()

