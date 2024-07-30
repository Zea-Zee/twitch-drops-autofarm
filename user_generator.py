import string
import random
import database
from faker import Faker


def random_uppercase(s: str, probability: float = 0.5) -> str:
    result = ''.join([char.upper() if random.random() < probability else char for char in s])
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
    year = random.randint(1950, 2024)
    month = random.randint(1, 12)
    day = random.randint(1, 28)

    username = generate_username(year)

    characters = string.ascii_letters + string.digits
    password = ''.join(random.choices(characters, k=10))

    birthdate = f"%{year}-%{month}-%{day}"

    phone_number = None
    country_code = None
    country = None

    email = "bebra"
    proxy_id = None

    return (username, password, birthdate, phone_number, country_code, country, email, proxy_id)


def generate_users(n):
    for _ in range(n):
        user = generate_random_user()
        database.add_user(*user)


def faker_tester():
    for _ in range(10):
        print(generate_random_user())


if __name__ == '__main__':
    # database.create_tables()
    # generate_users(10)

    faker_tester()
