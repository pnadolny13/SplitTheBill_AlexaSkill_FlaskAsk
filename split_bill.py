# -*- coding: utf-8 -*-

"""
Created on Fri Jan 12 20:39:02 2018

@author: pnadolny
"""

import logging

from flask import Flask, render_template

from flask_ask import Ask, statement, question, session

from datetime import datetime

app = Flask(__name__)

ask = Ask(app, "/")

logging.getLogger("flask_ask").setLevel(logging.DEBUG)


@ask.launch

def new_split():

    hour = 5
    #datetime.now().strftime('%-H')
    minute = 30
    #datetime.now().strftime('%-M')
    split_welcome = render_template('welcomeSplit', hour=hour, minute=minute)

    return question(split_welcome)


@ask.intent("YesIntent")

def get_names():

    group = render_template('groupNames')
    
    return question(group)


@ask.intent("GroupNamesIntent")
            #, mapping={'firstPerson': 'firstPerson', 'secondPerson': 'secondPerson','thirdPerson': 'thirdPerson'})

def get_beer_count(firstPerson, secondPerson, thirdPerson):
    
    peopleList = [firstPerson,secondPerson]
    peopleDict = {firstPerson:0, secondPerson:0}    
    if thirdPerson != None:
        peopleList.append(thirdPerson)
        peopleDict[thirdPerson] = 0
    else:
        print ("only 2 people")       
        
    session.attributes['peopleList'] = peopleList
    session.attributes['peopleDict'] = peopleDict
    groupResponse = render_template('groupResponse', peopleList=peopleList)

    return statement(groupResponse)


if __name__ == '__main__':

    app.run(debug=True)