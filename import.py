import csv
from sys import argv
from cs50 import SQL

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

if len(argv) == 2:
    with open(argv[1]) as csvfile:
        csvf = csv.DictReader(csvfile)
        engine = create_engine("postgres://sumjznccdlzznq:3f1d52a46872bf40a37c9f7a775a6596e4a04c1e3da8be50ab9ef09647cf0ede@ec2-35-175-155-248.compute-1.amazonaws.com:5432/dc6vvaofgcagpo")
        db = scoped_session(sessionmaker(bind=engine))

        for row in csvf:
            # email
            sid = row["email"]
            sid = sid.strip("s@mcs.edu.hk")
            db.execute("INSERT INTO users (id, class, number, first, last, trade) VALUES (:i, :c, :n, :f, :l, :t)",
            {"i": sid, "f": row["first"], "l": row["last"], "c": row["class/group"], "n": row["number"], "t": row['trade']})
            db.commit()
        exit(0)
# error code
print("Usage: python import.py users.csv")
exit(1)