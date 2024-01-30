import pyrebase
from hashlib import sha256
import json

f = open("config.json")
config = json.load(f)

firebase = pyrebase.initialize_app(config)
auth = firebase.auth()
db = firebase.database()
storage = firebase.storage()


def encode(var: str):
    return sha256(var.encode("utf-8")).hexdigest()


def register(email: str, password: str):
    try:
        user = auth.create_user_with_email_and_password(email, password)
        auth.send_email_verification(user["idToken"])
        return "Verfication link has been sent to your Email"
    except:
        return "There's an error occured"

def login(email: str, password: str):
    try:
        user = auth.sign_in_with_email_and_password(email,password)
        user = auth.refresh(user["refreshToken"])
        return (auth.get_account_info(user["idToken"])["users"][0]["emailVerified"], user["idToken"])
    except:
        return "Email or Password not found"

def set_user(email: str, password: str, name: str, born: int, interest: str):
    data = {
        encode(email): {
            "email": email,
            "password": encode(password),
            "data": {
                "name": name,
                "born": born,
                "interest": interest,
            },
        }
    }
    db.child("users").update(data)


def get_user(email: str):
    return db.child("users").child(encode(email)).get().val()


def update_user(email: str, data: dict):
    db.child("users").child(encode(email)).child("data").update(data)


def set_court(court: str, location: str, type: str, phone:str, embed:str, image_filename: str):
    data = {
        encode(court): {
            "name": court,
            "location": location,
            "type": type,
            "phone": phone,
            "embed": embed,
            "image": image_filename,
        }
    }
    db.child("courts").update(data)


def get_court():
    courts = db.child("courts").get().val()
    res = []
    if courts:
        for x in courts.values():
            res.append(x)
    return res


def update_court(court: str, data: dict):
    db.child("courts").child(encode(court)).update(data)


def set_timeslot(court: str, data:dict):
    db.child("courts").child(encode(court)).child("timeslot").update(data)

# print(get_court()[0]["image"])
# set_court("Kharisma","Kalideres","null","Badminton","None")
# set_timeslot("Kharisma")
# print(get_court("Kharisma"))
# def get_user(email:str)

# user = register("nkangdra@gmail.com","aaaaaa")
# print(user)
# auth.send_email_verification(user['idToken'])
# user = auth.sign_in_with_email_and_password("nk@gmail.com", "aaaaaa")
# p = auth.get_account_info(user["idToken"])
# print(p['users'][0]['emailVerified'])
# try:
#     urls = storage.child("images/slide.jpg").get_url(user['idToken'])
#     print(urls)
# except:
#     print("Ndak ada")