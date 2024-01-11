import csv

from parse_website import parse_with_pagination
from config import FILE_NAME


ex_list = parse_with_pagination()


def write_to_csv():
    with open(FILE_NAME, "w", newline="", encoding="utf-8") as file:
        fields = [
            "title",
            "description",
            "location",
            "experience",
            "english",
            "technologies"
        ]
        writer = csv.writer(file)
        writer.writerow(fields)
        for vacancy in ex_list:
            writer.writerow(
                [
                    vacancy.title,
                    vacancy.description,
                    vacancy.location,
                    vacancy.experience,
                    vacancy.english,
                    vacancy.technologies
                ]
            )


if __name__ == '__main__':
    write_to_csv()
