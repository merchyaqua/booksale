from sys import argv
from werkzeug.security import generate_password_hash
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

i = argv[1]
if not i:
    print('Usage: python reset.py [user id]')
    exit(1)
engine = create_engine("postgres://sumjznccdlzznq:3f1d52a46872bf40a37c9f7a775a6596e4a04c1e3da8be50ab9ef09647cf0ede@ec2-35-175-155-248.compute-1.amazonaws.com:5432/dc6vvaofgcagpo")
db = scoped_session(sessionmaker(bind=engine))

exist = db.execute("SELECT hash FROM users WHERE id = :i", {"i": i}).fetchone()[0]
if not exist:
    print('User does not exist.')
else:
    db.execute("UPDATE users SET hash = :h WHERE id = :i", {"i": i, "h": generate_password_hash("iwillremember")})
db.commit()
exit(0)