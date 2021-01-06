import random
import string
import mysql.connector

# Start DataBaseConnector
mydb = mysql.connector.connect(host="localhost", user="root", password="ggwp",database="COAP")
# mydb.close()

# Debug #
def insertRandomHistory(user_id, data_value): # Use Only for debug
    mycursor = mydb.cursor()
    sql = "INSERT INTO Hist (user_id, data_value) VALUES (%s, %s)"
    val = (user_id, data_value)
    mycursor.execute(sql, val)
    mydb.commit()
    mycursor.close()

# Release #
def createToken(length):
    return ''.join(random.choice(string.ascii_lowercase) for i in range(length))
def checkEmailExist(email):
    checkemail = False
    mycursor = mydb.cursor()
    query = "SELECT email FROM Users WHERE email = '" + email + "'"
    mycursor.execute(query)
    myresult = mycursor.fetchall()
    if len(myresult)  > 0:
        checkemail = True
    mycursor.close()
    return checkemail

def createUser(email, password):
    if checkEmailExist(email):
        return False
    else:
        token = createToken(20)
        mycursor = mydb.cursor()
        sql = "INSERT INTO Users (email, pass, token) VALUES (%s, %s, %s)"
        val = (email, password, token)
        mycursor.execute(sql, val)
        mydb.commit()
        mycursor.close()
        return True
def loginUser(email, password):
    isLogin = False
    mycursor = mydb.cursor()
    token = createToken(20)
    sql = "UPDATE Users SET token = '" + token + "' WHERE email = '" + email + "' and pass = '" + password + "'"
    mycursor.execute(sql)
    mydb.commit()
    if mycursor.rowcount > 0:
        isLogin = True
    mycursor.close()
    return isLogin, token

def getHistory(user_id):
    mycursor = mydb.cursor()
    sql = "SELECT data_value, date_value FROM Hist WHERE user_id = '" + user_id + "'"
    mycursor.execute(sql)
    myresult = mycursor.fetchall()
    mycursor.close()

    vec_hist = "["
    for obj in myresult:
        vec_hist = vec_hist + "{\"value\": \"" + str(obj[0]) + "\", \"date\": \"" + str(obj[1]) + "\"}"
        if myresult[-1] != obj:
            vec_hist = vec_hist + ","
    vec_hist = vec_hist + "]"
    return vec_hist
def checkToken(token):
    user_id = -1
    mycursor = mydb.cursor()
    sql = "SELECT id FROM Users WHERE token = '" + token + "'"
    mycursor.execute(sql)
    myresult = mycursor.fetchone()
    if myresult != None:
        user_id = myresult[0]
    return user_id

def insertInHistory(user_id, data_value):
    mycursor = mydb.cursor()
    sql = "INSERT INTO Hist (user_id, data_value) VALUES (%s, %s)"
    val = (user_id, data_value)
    mycursor.execute(sql, val)
    mydb.commit()
    mycursor.close()

# insertRandomHistory(1, 23.1) # use only for debug