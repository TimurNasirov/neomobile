from firebase_admin import credentials, messaging, initialize_app
from firebase_admin.firestore import client
from requests import get
from schedule import every, run_pending

cred = credentials.Certificate("key.json")
initialize_app(cred)
db = client()

def get_users(get_type):
    docs = (db.collection('users').stream())

    doc_list = []
    for doc in docs:
        doc_list.append(doc._data[get_type])
    return doc_list


def send_push(token, title, body):
    message = messaging.Message(
        notification=messaging.Notification(
            title=title,
            body=body,
        ),
        token=token,
    )

    # Отправка сообщения
    response = messaging.send(message)
    print('Successfully sent message:', response)



def main():
    db_users = get_users('us_id')
    db_users_id = get_users('token')
    st_users = get('https://testus.neotelecom.kg/api.php?key=aspergilus&cat=customer&action=get_customers_id&state_id=2&balance_to=61').json()['data']

    for i in st_users:
        if i in db_users:
            send_push(db_users_id[db_users.index(i)], 'Neomobile', 'Ваш баланс меньше 30! Пополните баланс')

every().day.at("18:00").do(main)

while True:
    run_pending()