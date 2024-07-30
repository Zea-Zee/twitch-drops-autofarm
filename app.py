import inspect

from datetime import datetime
import database
import auth
import user_generator


def main():
    # args = [True] * len(inspect.getfullargspec(database.reset_database).args)
    # database.reset_database(*args)
    # database.create_tables()
    # database.add_skin_package("Global Warfare", 31, datetime.strptime("07/27/24 02:00:00", "%m/%d/%y %H:%M:%S"), datetime.strptime("08/03/24 07:00:00", "%m/%d/%y %H:%M:%S"))

    # database.add_skin("ROCK", None, 1)
    # database.add_skin("HAMMER", None, 1)
    # database.add_skin("ARMORED DOUBLE DOOR", None, 1)
    # database.add_skin("LARGE WOOD BOX", None, 1)
    # database.add_skin("GARAGE DOOR", None, 1)
    # database.add_skin("M249", None, 1)

    # user_generator.create_users_in_database(1)
    # database.update_email_status(["thed.arknessprince1997@gmail.com", "the.darknessprince1997@gmail.com"])
    # database.reset_database(drop_users=True)


if __name__ == '__main__':
    main()
