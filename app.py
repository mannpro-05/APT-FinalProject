import time

from flask import Flask, render_template, request
import pandas as pd
import main

app = Flask(__name__)

'''
Route for the home page.
Using the Jinja - 2 template passing a list of video names to the front-end 
which will be displayed in dropdown list.
'''


@app.route('/')
def hello_world():  # put application's code here
    data = pd.read_csv("pose-output.csv")
    video_name = data.values[:, 0]
    return render_template("index.html", video_list=video_name)


'''
This route will handle the incoming post request form the front-end and will get the information 
out of the json data which is sent form the front-end via Ajax.
'''


@app.route('/getVideoName', methods=["POST"])
def get_video_name():
    if request.method == "POST":
        video_request = request.get_json()
        print(video_request)
        pose_data = pd.read_csv("pose-output.csv")
        video_list = list(pose_data.values[:, 0])
        start = time.time()
        video_name = main.parsing_csv(video_list.index(video_request[0]['value']), video_request[0]['value'])
        print(time.time() - start)
        pose_data = pd.read_csv("pose-output.csv")
        video_name_list = pose_data.values[:, 0]
        video_message = "This is the video for " + video_name.split('.')[0]
        return render_template("index.html", video_list=video_name_list, video_name=video_name,
                               video_message=video_message)
    return render_template("index.html")


if __name__ == '__main__':
    app.run(debug=True)
