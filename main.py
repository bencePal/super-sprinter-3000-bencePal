from flask import Flask, render_template, request, redirect, url_for
from common import read_data, write_data, generate_data_id
app = Flask(__name__)


@app.route("/")
@app.route("/list")
def page_home():
    file_name = "story_data.csv"
    all_data = read_data(file_name)
    current_data_id = request.args.get('delete_id')
    del_data = []

    # remove data
    for data in all_data:
        if data[0] == current_data_id:
            del_data = data

    if del_data != []:
        all_data.remove(del_data)
        write_data(file_name, all_data)

        return redirect(url_for('page_home'))

    return render_template("list.html", user_stories=all_data)


@app.route("/story", methods=['GET', 'POST'])
def page_add_story():
    title = "Super Sprinter 3000 - Add new Story"
    button_name = "create"
    file_name = "story_data.csv"
    all_data = read_data(file_name)
    data = []

    if request.method == "POST":
        data.append(str(generate_data_id(file_name)))
        data.append(request.form['story_title'])
        data.append(request.form['user_story'])
        data.append(request.form['acceptance_criteria'])
        data.append(request.form['business_value'])
        data.append(request.form['estimation'])
        data.append(request.form['status'])

        all_data.append(data)

        write_data(file_name, all_data)

        return redirect(url_for('page_home'))

    return render_template("form.html", title=title, button_name=button_name)


@app.route('/story/<story_id>', methods=['GET', 'POST'])
def page_update_story(story_id):
    title = "Super Sprinter 3000 - Edit Story"
    button_name = "update"
    file_name = "story_data.csv"
    all_data = read_data(file_name)
    current_data_id = story_id

    # get the current updating data index
    for data in all_data:
        if data[0] == current_data_id:
            current_data = data

    current_data_index = all_data.index(current_data)

    if request.method == "POST":
        update_data = [
            current_data_id,
            request.form['story_title'],
            request.form['user_story'],
            request.form['acceptance_criteria'],
            request.form['business_value'],
            request.form['estimation'],
            request.form['status']
            ]

        all_data[current_data_index] = update_data

        write_data(file_name, all_data)

        return redirect(url_for('page_home'))

    return render_template(
        "form.html",
        story_title=all_data[current_data_index][1],
        user_story=all_data[current_data_index][2],
        acceptance_criteria=all_data[current_data_index][3],
        business_value=all_data[current_data_index][4],
        estimation=all_data[current_data_index][5],
        status=all_data[current_data_index][6],
        title=title,
        button_name=button_name
        )

if __name__ == "__main__":
    app.run()
