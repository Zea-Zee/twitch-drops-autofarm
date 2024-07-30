import inspect

from datetime import datetime
import database
import automation_service
import firefox_automation
import user_generator


def main():
    # args = [True] * len(inspect.getfullargspec(database.reset_database).args)
    # database.reset_database(*args)
    # database.drop_tables(drop_users=True)
    # database.create_tables()
    # database.add_skin_package("Global Warfare", 31, datetime.strptime("07/27/24 02:00:00", "%m/%d/%y %H:%M:%S"), datetime.strptime("08/03/24 07:00:00", "%m/%d/%y %H:%M:%S"))

    # database.add_skin("ROCK", None, 1)
    # database.add_skin("HAMMER", None, 1)
    # database.add_skin("ARMORED DOUBLE DOOR", None, 1)
    # database.add_skin("LARGE WOOD BOX", None, 1)
    # database.add_skin("GARAGE DOOR", None, 1)
    # database.add_skin("M249", None, 1)

    # database.update_email_status(["thed.arknessprince1997@gmail.com", "the.darknessprince1997@gmail.com"])
    # database.reset_database(drop_users=True)

    user_generator.create_users_in_database(1)
    user = database.get_first_free_user()
    print(user)
    # automation_service.register(*(user[1], user[2], user[4], user[8]))
    # automation_service.watch_stream()

    firefox_automation.register(*(user[1], user[2], user[4], user[8]))
    firefox_automation.watch_stream()


if __name__ == '__main__':
    main()
