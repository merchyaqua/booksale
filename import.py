import csv
import re
from sys import argv
from cs50 import SQL

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

with open("csvdump/u.csv") as csvfile:
    csvf = csv.DictReader(csvfile)
    engine = create_engine("postgres://sumjznccdlzznq:3f1d52a46872bf40a37c9f7a775a6596e4a04c1e3da8be50ab9ef09647cf0ede@ec2-35-175-155-248.compute-1.amazonaws.com:5432/dc6vvaofgcagpo")
    db = scoped_session(sessionmaker(bind=engine))

    for row in csvf:
        # email
        sid = row["Email address"]
        if re.search(sid, '@mcs.edu.hk'):
            sid = sid.strip("s@mcs.edu.hk")
        else:
            row.update({"Class/Group": '/', "Number": "/"})

        exist = db.execute("SELECT * FROM users WHERE id = :i", {"i": sid}).fetchall()
        if exist:
            next
        else:
            db.execute("INSERT INTO users (id, class, number, first, last, trade) VALUES (:i, :c, :n, :f, :l, :t)", {"i": sid, "f": row["First name"], "l": row["Last name"], "c": row["Class/Group"].upper(), "n": row["Number"], "t": row['Buy or Sell']})
    db.commit()
    exit(0)