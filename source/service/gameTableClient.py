#import boto3
import json
import logging
import mysql.connector

from collections import defaultdict

def getAllGames():
    mydb = mysql.connector.connect(
        host="gamecollector.cezxpakqpxwm.us-east-2.rds.amazonaws.com",
        user="admin",
        password="mypassword",
        database="gamecollector"
    )
    
    cursor = mydb.cursor()
    query = 'select * from Game;'
    cursor.execute(query)

    gameList = []
    
    columns = [col[0] for col in cursor.description]
    rows = [dict(zip(columns, row)) for row in cursor.fetchall()]
    
    i = 1
    for row in rows:
        game = {}
        game['GameID'] = row['GameID']
        game['Title'] = row['Title']
        game['Developer'] = row['Developer']
        game['Publisher'] = row['Publisher']
        game['Genre'] = row['Genre']
        game['Description'] = row['Description']
        game['Rank'] = row['Rank']
        game['Image'] = row['Image']
        
        #gameDict[i].append(game)
        gameList.append(game)
        #i = i+1
    
    #for item in gameList:
    #    print(item)
    
    cursor.close()
    mydb.close()
    
    return json.dumps(gameList)
    
def getGame(gameID):
    mydb = mysql.connector.connect(
        host="gamecollector.cezxpakqpxwm.us-east-2.rds.amazonaws.com",
        user="admin",
        password="mypassword",
        database="gamecollector"
    )
    
    cursor = mydb.cursor()
    query = "select * from Game where GameID = {id}".format(id=gameID)
    cursor.execute(query)

    columns = [col[0] for col in cursor.description]
    rows = [dict(zip(columns, row)) for row in cursor.fetchall()]

    game = {}
    game['GameID'] = rows[0]['GameID']
    game['Title'] = rows[0]['Title']
    game['Developer'] = rows[0]['Developer']
    game['Publisher'] = rows[0]['Publisher']
    game['Genre'] = rows[0]['Genre']
    game['Description'] = rows[0]['Description']
    game['Rank'] = rows[0]['Rank']
    game['Image'] = rows[0]['Image']
    game['ProfileID'] = rows[0]['ProfileID']
    
    cursor.close()
    mydb.close()
    
    return json.dumps(game)
    
def addGame(gameData):

    mydb = mysql.connector.connect(
        host="gamecollector.cezxpakqpxwm.us-east-2.rds.amazonaws.com",
        user="admin",
        password="mypassword",
        database="gamecollector"
    )
        
    #aList = json.dumps(gameData)
    
    cursor = mydb.cursor()
    query = """INSERT INTO Game (`Title`, `Developer`, `Publisher`, `Genre`, `Description`, `Rank`, `ProfileID`) VALUES (%s, %s, %s, %s, %s, %s, %s)"""
    
    #.format(aList[0], aList[1], aList[2], aList[3], aList[4], aList[5], aList[6])
    
    result = cursor.execute(query, (gameData['title'] , gameData['developer'], gameData['publisher'], gameData['genre'], gameData['description'], gameData['rank'], gameData['profileid']))
    mydb.commit()
    
    cursor.close()
    mydb.close()
    
    return json.dumps(result)

def deleteGame(gameID):
    mydb = mysql.connector.connect(
        host="gamecollector.cezxpakqpxwm.us-east-2.rds.amazonaws.com",
        user="admin",
        password="mypassword",
        database="gamecollector"
    )
    
    cursor = mydb.cursor()
    query = """DELETE FROM Game WHERE GameID = %s"""
    
    result = cursor.execute(query, (gameID,))
    mydb.commit()
    
    cursor.close()
    mydb.close()
    
    return json.dumps(result)
    
def updateGame(gameData):
    mydb = mysql.connector.connect(
        host="gamecollector.cezxpakqpxwm.us-east-2.rds.amazonaws.com",
        user="admin",
        password="mypassword",
        database="gamecollector"
    )
    
    cursor = mydb.cursor()
    query = """UPDATE Game SET `Title` = %s, `Developer` = %s, `Publisher` = %s, `Genre` = %s, `Description` = %s, `Rank` = %s WHERE GameID = %s"""
    
    result = cursor.execute(query, (gameData['title'] , gameData['developer'], gameData['publisher'], gameData['genre'], gameData['description'], gameData['rank'], gameData['gameid']))
    mydb.commit()
    
    cursor.close()
    mydb.close()
    
    return json.dumps(result)
    
def registerUser(email):

    mydb = mysql.connector.connect(
        host="gamecollector.cezxpakqpxwm.us-east-2.rds.amazonaws.com",
        user="admin",
        password="mypassword",
        database="gamecollector"
    )
    
    cursor = mydb.cursor()
    query = """INSERT INTO Profile (`EmailAddress`) VALUES (%s)"""
    
    result = cursor.execute(query, (email,))
    mydb.commit()
    
    id = cursor.lastrowid
    
    cursor.close()
    mydb.close()
    
    return json.dumps(id)
    
def getProfileID(email):
    mydb = mysql.connector.connect(
        host="gamecollector.cezxpakqpxwm.us-east-2.rds.amazonaws.com",
        user="admin",
        password="mypassword",
        database="gamecollector"
    )
    
    cursor = mydb.cursor(buffered=True)
    query = "select ProfileID from Profile where EmailAddress = {}".format(email)
    
    print(query)
    
    cursor.execute(query)
    
    columns = [col[0] for col in cursor.description]
    rows = [dict(zip(columns, row)) for row in cursor.fetchall()]

    profileID = rows[0]['ProfileID']
    
    cursor.close()
    mydb.close()

    return json.dumps(profileID)
    
def getOwnedGames(profileID):
    mydb = mysql.connector.connect(
        host="gamecollector.cezxpakqpxwm.us-east-2.rds.amazonaws.com",
        user="admin",
        password="mypassword",
        database="gamecollector"
    )
    
    cursor = mydb.cursor()
    query = "select * from Game where ProfileID = {id} ORDER BY `Rank` DESC".format(id=profileID)
    cursor.execute(query)

    gameList = []
    
    columns = [col[0] for col in cursor.description]
    rows = [dict(zip(columns, row)) for row in cursor.fetchall()]
    
    for row in rows:
        game = {}
        game['GameID'] = row['GameID']
        game['Title'] = row['Title']
        game['Developer'] = row['Developer']
        game['Publisher'] = row['Publisher']
        game['Genre'] = row['Genre']
        game['Description'] = row['Description']
        game['Rank'] = row['Rank']
        
        #gameDict[i].append(game)
        gameList.append(game)
    
    for item in gameList:
        print(item)
    
    cursor.close()
    mydb.close()
    
    return json.dumps(gameList)