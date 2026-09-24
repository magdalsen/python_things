# Budget CLI

# A command-line budget management application written in Python.

# The application allows users to add expenses, generate reports, import expenses from CSV files, and store data between program runs.

# Features
    # add — adds a new expense with an amount and description.
    # report — displays all expenses in a formatted table, including:
        # expense ID
        # amount
        # an indicator for large expenses (≥ 1000)
        # description
        # completion status
        # total amount of all expenses
    # export-python — displays all stored expenses as Python objects.
    # import-csv — imports expenses from a CSV file.
    # Automatically assigns the first available ID to each new expense.
    # Stores the expense database in budget.db using Python's pickle module, allowing data to persist between program runs.
    # Automatically creates an empty database when the database file does not exist.
    # Validates expense amounts and prevents non-positive values.
    # Validates expense descriptions and prevents empty descriptions.
    # Handles invalid input, missing files, and other errors using exception handling.

from dataclasses import dataclass
import click
import pickle
import sys
import csv

FILENAME_DB = 'budget.db'

@dataclass
class TodoItem:
    id: int
    price: float
    big: str
    description: str
    done: bool

    def __post_init__(self):
        if not self.description:
            raise ValueError("Opis nie może być pusty!")

        if self.price <= 0:
            raise ValueError("Kwota musi być dodatnia!")

def load_database():
    try:
         with open(FILENAME_DB, 'rb') as stream:
            return pickle.load(stream)
    except FileNotFoundError:
        return []

def find_next_id(file):
    ids = {todo.id for todo in file}
    counter = 1
    while counter in ids:
        counter += 1
    return counter

def calculate_big_expense(price):
    if price >= 1000:
        return '✓'
    return ''

def calculate_column_size(obj_restored):
    id_width = max(len("ID"), max(len(str(obj.id)) for obj in obj_restored))
    price_width = max(len("PRICE"), max(len(str(obj.price)) for obj in obj_restored))
    big_width = max(len("BIG?"), max(len(obj.big) for obj in obj_restored))
    desc_width = max(len("DESC"), max(len(obj.description) for obj in obj_restored))
    return id_width, price_width, big_width, desc_width

def todo_item_element(file, description, price):
    return TodoItem(
                id=find_next_id(file),
                price=price,
                description=description,
                big=calculate_big_expense(price),
                done=False,
            )

def table_print(id_width, price_width, big_width, desc_width, file):
    print(f'{"ID":<{id_width}} {"PRICE":<{price_width}} {"BIG?":<{big_width}} {"DESC":<{desc_width}} {"DONE?"}')

    counter = 0
    for todo in file:
        counter += todo.price
        print(
            f'{todo.id:<{id_width}} '
            f'{todo.price:<{price_width}} '
            f'{todo.big:<{big_width}} '
            f'{todo.description:<{desc_width}} '
            f'{"YES" if todo.done else "NO"}'
        )
    print(f"Sum: {counter}")

def save_database(file):
    with open(FILENAME_DB, "wb") as stream:
            pickle.dump(file, stream)

@click.group()
def cli():
    pass

@cli.command()
@click.argument('price', type=float)
@click.argument('description')
def add(price, description):
    file = load_database()

    try:
        file.append(
            todo_item_element(file, description, price)
        )
    except ValueError as e:
        print(f'Błąd: {e.args[0]}')
        sys.exit(1)

    save_database(file)

    id_width, price_width, big_width, desc_width = calculate_column_size(file)
    table_print(id_width, price_width, big_width, desc_width, file)

@cli.command()
def report():
    file = load_database()

    id_width, price_width, big_width, desc_width = calculate_column_size(file)

    table_print(id_width, price_width, big_width, desc_width, file)

@cli.command()
def export_python():
    file = load_database()

    print(file)

@cli.command()
@click.argument('filename')
def import_csv(filename):
    # Wczytanie istniejącej bazy
    file = load_database()

    # Wczytanie danych z CSV
    try:
        with open(filename, 'r', encoding='utf-8') as stream:
            reader = csv.DictReader(stream)

            for row in reader:
                price = float(row['amount'])
                description = row['description']

                file.append(
                    todo_item_element(file, description, price)
                )

    except FileNotFoundError:
        print(f'Nie znaleziono pliku: {filename}')
        sys.exit(1)

    except ValueError as e:
        print(f'Błąd: {e}')
        sys.exit(1)

    # Zapisanie powiększonej bazy
    save_database(file)
    print('Poprawnie zaimportowano plik csv.')

if __name__ == "__main__":
    cli()
