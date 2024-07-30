from datetime import datetime
import string
import random
import database
from faker import Faker


def random_uppercase(s: str, probability: float = 0.5) -> str:
    result = ''.join([char.upper() if random.random() <
                     probability else char for char in s])
    return ''.join(result)


def generate_username(year: int) -> str:
    faker = Faker()
    while True:
        username = faker.user_name()
        username_without_numbers = ''.join(
            [char for char in username if not char.isdigit()])
        if username_without_numbers:
            break

    username = random_uppercase(username_without_numbers)
    username += str(year)
    return username


def generate_random_user():
    year = random.randint(1980, 2008)
    month = random.randint(1, 12)
    day = random.randint(1, 28)

    username = generate_username(year)

    characters = string.ascii_letters + string.digits
    password = ''.join(random.choices(characters, k=10))

    birthdate = datetime.strptime(f"{year}-{month}-{day}", '%Y-%m-%d').date()

    phone_number = None
    country_code = None
    country = None

    email = "bebra"
    proxy_id = None

    return (username, password, birthdate, phone_number, country_code, country, email, proxy_id)


def create_users_in_database(n: int) -> None:
    for _ in range(n):
        user = generate_random_user()
        database.add_user(*user)


def faker_tester():
    for _ in range(10):
        print(generate_random_user())


def email_generator(original_email: str) -> list[str]:
    # base, domain = original_email.split('@', 1)
    new_emails = set()

    def recursive_insert(s: str, pos: int) -> None:
        if original_email[pos] == '@':
            return
        new_emails.add(s + original_email[pos:])
        recursive_insert(s + original_email[pos], pos + 1)

        new_emails.add(s + '.' + original_email[pos:])
        recursive_insert(s + '.' + original_email[pos], pos + 1)

    recursive_insert(original_email[0], 1)
    return list(new_emails)
    # print(len(list(new_emails)))
    # for el in list(new_emails)[:10]:
    #     print(el)


def create_emails_in_database(email: str) -> None:
    emails = email_generator(email)
    database.add_emails(emails)


if __name__ == '__main__':
    # database.create_tables()
    # generate_users(10)
    # faker_tester()
    # email_generator("thedarknessprince1997@gmail.com")
    # email_generator("yolo@gmail.com")
    create_emails_in_database("thedarknessprince1997@gmail.com")
