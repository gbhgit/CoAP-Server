import random
import string
import mysql.connector

# Start DataBaseConnector
mydb = mysql.connector.connect(host="localhost", user="root", password="ggwp",database="COAP")
# mydb.close()

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
