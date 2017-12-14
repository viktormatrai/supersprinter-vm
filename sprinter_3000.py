from flask import *

app = Flask(__name__)


def read():
    table = []
    with open('user_data.csv', "r") as data:
        for line in data:
            lines = line.replace("\n", "")
            words = lines.split(',')
            table.append(words)
    return table


def add_ID(table):
    ID = len(table) + 1
    for story in table:
        if ID == story[0]:
            ID += 1
    return str(ID)


@app.route('/list')
@app.route('/')
def root():
    table = read()
    return render_template('list.html', stories=table)


@app.route('/story/', methods=['GET', 'POST'])
def add_new():
    return render_template('form.html')


@app.route('/add_new', methods=['GET', 'POST'])
def new_story():
    table = read()
    new_id = add_ID(table)
    name = request.args.get('name')
    story = request.args.get('story')
    criteria = request.args.get('criteria')
    value = request.args.get('value')
    estimation = request.args.get('estimation')
    status = request.args.get('status')
    storylist = [new_id, name, story, criteria, value, estimation, status]
    with open('user_data.csv', 'a') as f:
        for word in storylist:
            f.writelines(word + ",")
        f.write('\n')
    fresh_table = read()
    return render_template('list.html', stories=fresh_table)


@app.route('/story/<story_id>/del', methods=['POST'])
def delete(story_id):
    table = read()
    with open('user_data.csv', 'w') as f:
        for line in table:
            if line[0] == story_id:
                del line
            else:
                for word in line:
                    f.writelines(word + ",")
                f.write("\n")
    updated_table = read()
    return redirect("/", )


if __name__ == "__main__":
    app.run(debug=True)
