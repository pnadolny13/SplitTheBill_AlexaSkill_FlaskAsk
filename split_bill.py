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

    hour = int(datetime.now().strftime('%H'))
    if hour > 12:
        hour = hour - 12
    hour = str(hour)
    minute = datetime.now().strftime('%M')
    split_welcome = render_template('welcomeSplit', hour=hour, minute=minute)

    return question(split_welcome)


@ask.intent("YesIntent")

def get_names():

    group = render_template('groupNames')
    
    return question(group)


@ask.intent("GroupNamesIntent")
def get_beer_count(firstPerson, secondPerson, thirdPerson, forthPerson, fifthPerson, sixthPerson, seventhPerson, eigthPerson, ninthPerson):
    
    peopleList = [firstPerson,secondPerson]
    peopleDict = {firstPerson:0, secondPerson:0}    
    if thirdPerson != None and thirdPerson not in peopleDict:
        peopleList.append(thirdPerson)
        peopleDict[thirdPerson] = 0
    if forthPerson != None and forthPerson not in peopleDict:
        peopleList.append(forthPerson)
        peopleDict[forthPerson] = 0 
    if fifthPerson != None and fifthPerson not in peopleDict:
        peopleList.append(fifthPerson)
        peopleDict[fifthPerson] = 0 
    if sixthPerson != None and sixthPerson not in peopleDict:
        peopleList.append(sixthPerson)
        peopleDict[sixthPerson] = 0 
    if seventhPerson != None and seventhPerson not in peopleDict:
        peopleList.append(seventhPerson)
        peopleDict[seventhPerson] = 0 
    if eigthPerson != None and eigthPerson not in peopleDict:
        peopleList.append(eigthPerson)
        peopleDict[eigthPerson] = 0 
    if ninthPerson != None and ninthPerson not in peopleDict:
        peopleList.append(ninthPerson)
        peopleDict[ninthPerson] = 0         
        
    session.attributes['peopleList'] = peopleList
    session.attributes['peopleDict'] = peopleDict
    groupResponse = render_template('groupResponse', peopleList=peopleList)

    return question(groupResponse)

@ask.intent("CostInputIntent", convert={'beerPrice': int, 'tax': int, 'tip': int})
def get_cost_inputs(beerPrice, tax, tip):
    if beerPrice == None or tax == None or tip == None:
        return question('I missed that, say beer price tax and tip.')
    tip = tip/100
    tax = tax/100
    session.attributes['beerPrice'] = beerPrice
    session.attributes['tax'] = tax
    session.attributes['tip'] = tip
        
    return question(render_template('inputsResponse'))


@ask.intent("PersonEntryIntent", convert={'beerCount': int})
def get_beer_per_person(person, beerCount):
    beerPrice = session.attributes['beerPrice']
    tip = session.attributes['tip']
    tax = session.attributes['tax']
    session.attributes['peopleList']
    peopleDict = session.attributes['peopleDict']   
    # if person exists in dictionary
    if person in peopleDict:
        # if beerCount is not zero
        if beerCount != 0:
            amount = round(((beerCount * beerPrice * (1 + tax)) * (1 + tip)), 2)
            # add beer count to total
            peopleDict.update(({person:amount}))
        else:
            return question('Loser. Anything else? If not, say done.')
    # else respond with doesnt exist template
    else:
        return question('I dont know that person. Anything else? If not, say done.')
    return question('Anything else to add? If not, say done.')


@ask.intent("DoneIntent", convert={'beerCount': int})
def done():
    peopleDict = session.attributes['peopleDict']
    total = 0
    for person in peopleDict:
        total += peopleDict[person]
    totals = render_template('totals', peopleDict=peopleDict, total=total)
    
    return statement(totals)



if __name__ == '__main__':

    app.run(debug=True)