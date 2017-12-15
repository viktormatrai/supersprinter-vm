from flask import Flask, render_template, request, redirect
import dataManager

app = Flask(__name__)


@app.errorhandler(404)
def error(error):
    return redirect("/")


@app.route("/")
def table():
    sort_by = request.args.get("sort_by", "id")
    direction = request.args.get("direction", "up")
    list_of_names = ["id", "story_title", "user_story", "acceptance_criteria",
                     "business_value", "estimation", "status"]
    status_names = ["Planning", "TODO", "In Progress", "Review", "Done"]
    title = ["ID", "Story Title", "User Story", "Acceptance criteria",
             "Business Value", "Estimation", "Status"]
    try:
        assert direction == "up" or direction == "down"
        assert sort_by in list_of_names
    except AssertionError:
        direction = "up"
        sort_by = "id"

    title_and_list_of_names = list(zip(list_of_names, title))
    user_stories = dataManager.read_data() 
    sorted_user_stories = sort(user_stories, sort_by, direction)
    return render_template('list.html', data=sorted_user_stories, list_of_names=list_of_names,
                           status_names=status_names, title_and_list_of_names=title_and_list_of_names,
                           sort_by=sort_by, direction=direction)


@app.route("/", methods=['POST'])
def action_from_table():
    return redirect('form')


@app.route("/form")
def add_new_item():
    the_dict = {}
    status_names = ["Planning", "TODO", "In Progress", "Review", "Done"]
    list_of_names = ["id", "story_title", "user_story", "acceptance_criteria",
                     "business_value", "estimation", "status"]
    return render_template('form.html', task="add_new_item",
                           user_story=the_dict, list_of_names=list_of_names,
                           status_names=status_names)


@app.route('/form', methods=['POST'])
def action_add_new_item():
    user_story = {}
    list_of_names = ["story_title", "user_story", "acceptance_criteria",
                     "business_value", "estimation", "status"]
    for name in list_of_names:
        user_story[name] = request.form[name]
    user_stories = dataManager.read_data()
    user_story["id"] = new_id(user_stories)
    user_stories.append(user_story)
    dataManager.write_data(user_stories)
    return redirect("/")


def new_id(user_stories):
    max_id = 0
    for user_story in user_stories:
        id = int(user_story["id"])
        if id > max_id:
            max_id = id
    return max_id + 1


@app.route("/form/<int:id>")
def edit_item(id):
    user_stories = dataManager.read_data()
    id_is_in_user_stories = False
    for user_story in user_stories:
        if int(user_story["id"]) == id:
            the_dict = user_story
            id_is_in_user_stories = True
    status_names = ["Planning", "TODO", "In Progress", "Review", "Done"]
    list_of_names = ["id", "story_title", "user_story", "acceptance_criteria",
                     "business_value", "estimation", "status"]
    if id_is_in_user_stories:
        return render_template("form.html", task="edit_item", user_story=the_dict,
                               list_of_names=list_of_names, id=id, status_names=status_names)
    else:
        return redirect("/")


@app.route("/form/<int:id>", methods=['POST'])
def update_post(id):
    user_story = {}
    list_of_names = ["story_title", "user_story", "acceptance_criteria", "business_value",
                     "estimation", "status"]
    for name in list_of_names:
        user_story[name] = request.form[name]
    user_stories = dataManager.read_data()
    for user_story_ in user_stories:
        if int(user_story_["id"]) == id:
            for name in list_of_names:
                user_story_[name] = user_story[name]
    dataManager.write_data(user_stories)
    return redirect("/")


@app.route("/form/<int:id>/delete")
def delete_item(id):
    user_stories = dataManager.read_data()
    for index, user_story in enumerate(user_stories):
        if int(user_story["id"]) == id:
            user_stories.remove(user_stories[index])
            break
    dataManager.write_data(user_stories)
    return redirect("/")


def sort(user_stories, sort_by, direction):
    try:
        user_stories = sorted(user_stories, key=lambda x: int(x[sort_by]), reverse=direction == "down")
    except:
        user_stories = sorted(user_stories, key=lambda x: x[sort_by], reverse=direction == "down")
    return user_stories


if __name__ == "__main__":
    app.run(debug=True)