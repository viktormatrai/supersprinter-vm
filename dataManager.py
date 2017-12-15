

def write_data(user_stories):
    # name of textarea
    list_of_names = ["id", "story_title", "user_story", "acceptance_criteria",
                     "business_value", "estimation", "status"]
    with open("user_data.csv", "w") as file:
        for user_story in user_stories:
            for name in list_of_names:
                file.write(str(user_story[name]).replace("\r\n", "it_is_enter") + "\t")
            file.write("\n")
    return user_stories


def read_data():

    # read all item from user_data.csv and create a list of lists
    with open("user_data.csv", "r") as file:
        read = file.read().splitlines()
        data = [line.split("\t") for line in read]
    # create a list of dictionary and return that
    user_stories = []
    list_of_names = ["id", "story_title", "user_story", "acceptance_criteria",
                     "business_value", "estimation", "status"]
    for row in data:
        create_dict = {}
        for index, name in enumerate(list_of_names):
            create_dict[name] = row[index].replace("it_is_enter", " \r\n ")
        user_stories.append(create_dict)
    return user_stories
