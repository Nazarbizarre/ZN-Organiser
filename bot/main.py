from telethon import TelegramClient, events
from sqlalchemy import select
from flask_login import login_user
from frontend.db import User, Session
from .keyboards import inline
from requests import get

api_hash = "460dbd52a66709679d8d65950720fe22"
api_id = "29195129"
bot_token = '7015782041:AAEBUp1JAx592RrIE517EbKIqucUUaGBznU'
BACKEND_URL = "http://127.0.0.1:8000"

client = TelegramClient('bot', api_id, api_hash).start(bot_token=bot_token)

user_states = {}

@client.on(events.NewMessage(pattern='/start'))
async def start_message(event):
    sender = await event.get_sender()
    name = sender.first_name
    await event.respond(f"Hello, {name}!\nYou can login by clicking on the button below.", buttons=inline.login)

@client.on(events.CallbackQuery(pattern=b'login'))
async def handle_login_query(event):
    user_id = event.sender_id
    user_states[user_id] = {'state': 'awaiting_email', 'attempts': 0}
    await event.respond('Please enter your email:')


@client.on(events.NewMessage)
async def handle_message(event):
    user_id = event.sender_id
    user_state = user_states.get(user_id)
    
    if user_state:
        state = user_state.get('state')
        attempts = user_state.get('attempts', 0)
        
        if state == 'awaiting_email':
            user_state['email'] = event.text.lower()
            user_state['state'] = 'awaiting_password'
            await event.respond('Please enter your password:')
        
        elif state == 'awaiting_password':
            password = event.text
            email = user_state.get('email')
            user_state['attempts'] = attempts + 1
            
            if user_state['attempts'] > 3:
                user_states.pop(user_id, None)
                await event.respond('Too many failed attempts. Please try again later.')
                return
            
            with Session.begin() as session:
                user = session.scalar(select(User).where(User.email == email))
                if user and user.password == password:
                    user_states[user_id] = {'state': 'logged_in', 'email': email}
                    await event.respond(f'Registration successful, welcome {user.email}!', buttons=inline.main)
                else:
                    user_state['state'] = 'awaiting_email'
                    await event.respond(f'Invalid email or password. Attempts left: {3 - user_state["attempts"]}. Please enter your email again:')



async def display_tasks(event, email: str):
    tasks = get_tasks(email)
    if tasks:
        tasks_message = "\n".join([
            f"Title: {task.get('title')}\nContent: {task.get('content')}\nCreated: {task.get('published')}\nDeadline - {task.get('deadline')}\n"
            for task in tasks
        ])
        await event.respond(f"Your tasks:\n{tasks_message}")
    else:
        await event.respond("You have no tasks.")

def get_tasks(email: str):
    data = {
        "email": email
    }
    response = get(f"{BACKEND_URL}/get_tasks", json=data)
    if response.status_code == 200:
        tasks = response.json()
        return tasks
    else:
        return []

@client.on(events.CallbackQuery(pattern=b'all_tasks'))
async def all_tasks(event):
    user_id = event.sender_id
    user_state = user_states.get(user_id)
    
    if user_state:
        email = user_state.get('email')
        await display_tasks(event, email)
    else:
        await event.respond("Please log in first.")



async def main():
    await client.start()
    await client.run_until_disconnected()

if __name__ == "__main__":
    client.loop.run_until_complete(main())
