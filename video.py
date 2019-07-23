import pandas as pd
import flask
import requests
from flask import Flask
from firebase import firebase

firebase = firebase.FirebaseApplication('https://saath-health.firebaseio.com', None)

userList = pd.read_csv('users.csv')
userIds = userList['User ID']
rows_list = []

video_list = firebase.get("/videos",None)
col_list = []
for col in video_list.items():
    col_list.append(str(col[0]))
column = col_list
column.insert(0,'User ID')
column.append("Count")



def video_extract(request):
    #return 'Hello World!!!'
    for user in userIds[0:]:
        print(str(user))
        
        user_dict = { "User ID" : str(int(user)) }
        user_cc = firebase.get("/users/"+ str(int(user)) +"/content_consumed/video", None)
        count = 0
        if (type(user_cc) == dict):
            for quiz in user_cc.items():
                count += 1
                #print(quiz)
    #             print(quiz)
                try:
                  user_dict.update({ str(quiz[0]) : str(quiz[1]["first_at"]) })
                except:
                  print("Error")
                #print (user_dict[video[0]])
    #else:
       # print ("No Video Consumed")
        user_dict.update({ "Count" : str(count) })
        rows_list.append(user_dict)
        #rows_list.append(user_cc)
        df = pd.DataFrame(rows_list, columns = column)
    #user_cc = user_cc['results'][0]
    #print(df)
    #return (df)
    resp = flask.make_response(df.to_csv())
    resp.headers["Content-Disposition"] = "attachment; filename=video.csv"
    resp.headers["Content-Type"] = "text/csv"
    return resp


    
    
if __name__ == "__main__":
    
    app = Flask(__name__)

    @app.route('/')
    def index():
        return video_extract(requests)

    app.run('127.0.0.1', 8000, debug=True)

