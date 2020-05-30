from flask import Flask, render_template, request
from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer
from chatterbot.trainers import ListTrainer
import pandas as pd
import numpy as np

app = Flask(__name__)

# load in dataset
# df  = pd.read_excel('C://Users//hicom//Documents//Side Projects//MovingBot//bevoelkerung.xlsx', sheet_name='bevoelkerung', encoding='latin1')

# get array with average age per stadtteil
# age = df['mean']
# mean_array = np.asarray(age)

@app.route("/")
def home():
    return render_template("home.html")

mode = 'x'
bot = ChatBot('MovingBot', logic_adapters=[{'import_path': 'logic_adapt.MyLogicAdapter'}]) 
  
# conversation = [
#     "Hello",
#     "Hi there!",
#     "How are you doing?",
#     "I'm doing great.",
#     "That is good to hear",
#     "Thank you.",
#     "You're welcome."
# ] 
# trainer = ListTrainer(bot)

# trainer.train(conversation)


@app.route("/get")
def get_bot_response():
    # get age of user
    userText = request.args.get('msg')
    
    # # check university
    # if ('goethe' or 'göthe') in userText:
     #    return ('Thanks, that information will make it easier for me to find the perfect area for you! How do you plan to commute to uni? By car, bike or walking?')
    
    # # check for commuting type
    # if ('car' or 'auto' or 'drive' or 'driving') in userText:
    #     mode = 'car'
    #     return('Alright. Got it. How long would you maximum be willing to commute?')
    # if ('bike' or 'cycle' or 'rad') in UserText:
    #     mode = 'bike'
    #     return('Alright. Got it. How long would you maximum be willing to commute?')
    # if ('walk' or 'gehen' or 'laufen' or 'foot' or 'feet') in userText:
    #     mode = 'walk'
    #     return('Alright. Got it. How long would you maximum be willing to commute?')
    
    # #if(mode != 'x') and (userText != 'x'):
    # else:
    #     mode_time = [mode, int(userText)]
    #     return(str('So to check: You would like to commute by ' + mode + 'and not take longer than' + str(userText) +'?'))
    
    userText = request.args.get('msg')    
    return str(bot.get_response(userText)) 
    
    # user_age = int(userText)
    
    # # find most fitting stadtteil
    # index_age = (np.abs(mean_array-user_age)).argmin()
    # stadtteil = df.loc[index_age,'Stadtteil']
    # stadteil_average = df.loc[index_age,'mean']

    # give recommendation
    

    
    #return str('I would recommend you to move to '+ stadtteil + '. There the average age is ' + str(stadteil_average))

if __name__ == "__main__":
    app.run()