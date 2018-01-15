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
    
    session.attributes['peopleDict'] = peopleDict
    groupResponse = render_template('groupResponse', peopleList=peopleList)

    return question(groupResponse)

@ask.intent("ItemInputIntent", convert={'drink': int, 'costDollars': int, 'costCents': int})
def get_item_input(drink, costDollars, costCents):
    itemDict = {}
    if costDollars != None and costCents != None:
        price = costDollars + "." + costCents
        price = float(price)
    else:
        return question('I didnt understand your price, please try again. For example say bud light cost 5 dollars and 50 cents.')
    if drink != None:
        itemDict[drink] = price
    else:
        return question('I didnt get your drink name, please try again. For example say bud light cost 5 dollars and 50 cents.')
    session.attributes['itemDict'] = itemDict
    return question(render_template('inputsResponse'))

@ask.intent("CostInputIntent", convert={'tax': int, 'tip': int})
def get_cost_inputs(beerPrice, tax, tip):
    if tax == None or tip == None:
        return question('I missed that, say tax percent and tip percent.')
    tip = tip/100
    tax = tax/100
    session.attributes['tax'] = tax
    session.attributes['tip'] = tip
        
    return question(render_template('inputsResponse'))


@ask.intent("PersonEntryIntent", convert={'drinkCount': int})
def get_beer_per_person(person, drinkCount, drinkName):
    itemDict = session.attributes['itemDict']
    tip = session.attributes['tip']
    tax = session.attributes['tax']
    peopleDict = session.attributes['peopleDict']   
    # if person exists in dictionary
    if person in peopleDict:
        # if beerCount is not zero
        if drinkCount != 0:
            if drinkName in itemDict:
               # get price of drink, get current person's total,
               # add them together and put back in dict
               price = itemDict[drinkName]
               amount = round(((drinkCount * price * (1 + tax)) * (1 + tip)), 2)
               currentTotal = peopleDict[person]
               amount += currentTotal
               peopleDict.update(({person:amount}))
            else:
                return question('I dont know the price of that drink. Please add it.')
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