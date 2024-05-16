import uvicorn
from fastapi import FastAPI, HTTPException, Header,Request
from pydantic import BaseModel
import random
import string
import pymysql
app = FastAPI()

#todo data base connection
connection = pymysql.connect(host='192.168.1.84', user='root', password='xbyte', database='dataname', autocommit=True)
cursor = connection.cursor()

#
class UserCreate(BaseModel):
    # user_id: int
    token: str

#todo Function to generate token
def generate_token(name):
    token = ''.join(random.choices(string.ascii_letters + string.digits, k=16))

    # TODO :: Check Name Avalable or not....
    result_dic = {}
    try:
        query = f"SELECT `name` FROM tokens WHERE name = '{name}'"
        cursor.execute(query)
        result = cursor.fetchone()
        if result:
            print("Name is available...")
            query = f"update tokens set `token`='{token}' where `name`='{name}'"
            cursor.execute(query)
            connection.commit()
            result_dic['Token']= token
        else:
            result_dic['Message']= "Name is not available..."
            print("Name is not available...")
    except Exception as e:
        print(e)
    return result_dic

#todo Function to get data
def get_data(token):

    result_dic = {}
    try:
        query = f"SELECT * FROM tokens WHERE token = '{token}'"
        cursor.execute(query)
        result = cursor.fetchone()
        if result:
            result_dic['result'] = result
        else:
            result_dic['Message'] = "token is not available..."
            print("token is not available...")
    except Exception as e:
        print(e)
    return result_dic

@app.get("/generate-token")
async def generate_auth_token(request: Request):
    params = request.query_params
    name = params.get('name')
    token = generate_token(name)
    return token

@app.get("/get-data")
async def get_data_auth_token(request: Request):
    params = request.query_params
    token = params.get('token')
    token = get_data(token)
    return token

@app.post("/get_user/")
async def get_user(user_data: UserCreate):
    # user_id = user_data.user_id
    token = user_data.token
    data = get_data(token)
    return data


if __name__ == "__main__":
    uvicorn.run(app, host="192.168.1.84", port=5553)