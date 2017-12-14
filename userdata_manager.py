import csv


def read_csv(file_name):
    table = []
    with open(file_name, "r") as data_table:
        for row in data_table:
            row_to_cut = row.replace("\n", "")
            words = row_to_cut.split(',')
            table.append(words)
    return table


def write_csv(file_name, table):
    with open(file_name, "w") as add_to_table:
        for item in table:
            write_story = ','.join(item)
            add_to_table.write(write_story + "\n")

"""def update_csv(file_name, table):
    with open(file_name, 'a') as f:"""


def generate_id(table):

    new_id = []
    for row in table:
        new_id.append(int(row[0]))
        new_id = max(new_id) + 1

    return str(new_id)
