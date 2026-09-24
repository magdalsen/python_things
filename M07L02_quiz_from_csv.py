# # This program is a simple quiz that runs in the terminal. It reads questions from a CSV file, asks the user the questions, and finally displays the number of correct answers.

from dataclasses import dataclass
import sys
import csv
import click

@dataclass
class QuestionList:
    id: int
    description: str
    answer: bool

def display_questions(filename):
    try:
        with open(filename, 'r',  encoding='utf-8') as stream:
            reader = csv.DictReader(stream)
            counter = 0
            counter_good_ans = 0
            for row in reader:
                description = row['description']
                answer = row['answer']

                counter += 1
                user_ans = input(f'Pytanie {counter}. {description}')

                match user_ans:
                    case 'skip' | 'Skip':
                        continue
                    case 'exit' | 'Exit':
                        break
                    case _:
                        if user_ans == answer:
                            counter_good_ans += 1
    except FileNotFoundError:
        print(f'Nie znaleziono pliku: {filename}')
        sys.exit(1)

    print(f'Poprawnych odpowiedzi było: {counter_good_ans}')

@click.group()
def cli():
    pass

@cli.command()
@click.argument('filename')
def main(filename):
    print('QUIZ')
    display_questions(filename)

if __name__ == "__main__":
    cli()
