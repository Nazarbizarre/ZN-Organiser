from os import getenv
from datetime import datetime 
from datetime import timedelta, datetime
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from telethon import TelegramClient, events
from sqlalchemy import select
from flask_login import login_user
from frontend.db import User, Session
from requests import get
from .keyboards import inline


API_ID = getenv("API_ID")
API_HASH = getenv("API_HASH")
BOT_TOKEN = getenv("BOT_TOKEN")
BACKEND_URL = getenv("BACKEND_URL")


client = TelegramClient('bot', API_ID, API_HASH).start(bot_token=BOT_TOKEN)
scheduler = AsyncIOScheduler()

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
        "email": email,
        "completed": False
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



@client.on(events.CallbackQuery(pattern=b'themes'))
async def themes(event):
    await event.respond("Choose theme: ", buttons=inline.themes)

@client.on(events.CallbackQuery(pattern=b'theme_.*'))
async def all_tasks_by_theme(event):
    user_id = event.sender_id
    user_state = user_states.get(user_id)
    email = user_state.get('email')
    theme = event.data.split(b'_')[1]
    
    data = {
        "email": email,
        "theme": theme.decode()
    }

    response = get(f"{BACKEND_URL}/themes", json=data)
    if response.status_code == 200:
        tasks = response.json()
        theme = event.data.split(b'_')[1].decode()
        if not tasks:
            message = f"Selected theme: {theme}\n\nNo tasks available for this theme."
        else:
            message = f"Selected theme: {theme}\n\n"
            for task in tasks:
                title = task.get('title')
                content = task.get('content')
                published = task.get('published')
                deadline = task.get('deadline')
                message += (f"""Title: {title}\n
Content: {content}
Published: {published}
Deadline: {deadline}\n\n""")
        await event.respond(message)
    else:
        await event.respond(f"Error {response.status_code}")


user_data = {}

def is_valid_date(date_str):
    try:
        datetime.strptime(date_str, "%Y-%m-%d")
        return True
    except ValueError:
        return False

@client.on(events.CallbackQuery(pattern=b'filter'))
async def filter_by_date(event):
    user_id = event.sender_id
    if user_id not in user_data:
        user_data[user_id] = {'step': 'start_date'}
    
    await event.respond("Enter start date (yyyy-mm-dd):")

@client.on(events.NewMessage)
async def handle_filter_message(event):
    user_id = event.sender_id
    
    data = user_data.get(user_id)
    if data:
        step = data.get('step')
        date_text = event.text
        
        if not is_valid_date(date_text):
            await event.respond("Invalid date format. Please use yyyy-mm-dd.")
            return

        match step:
            case 'start_date':
                data['start_date'] = date_text
                data['step'] = 'end_date'
                await event.respond("Enter end date (yyyy-mm-dd):")
            
            case 'end_date':
                start_date = data.get('start_date')
                end_date = date_text

                if start_date is None:
                    await event.respond("Start date not set. Please start over.")
                    return

                if datetime.strptime(end_date, "%Y-%m-%d") < datetime.strptime(start_date, "%Y-%m-%d"):
                    await event.respond("End date cannot be earlier than start date.")
                    return

                data['end_date'] = end_date
                del user_data[user_id]
                
                message = f"Filtering tasks from {start_date} to {end_date}"
                
                user_state = user_states.get(user_id)
                email = user_state.get('email') if user_state else None

                data = {
                    "email": email,
                    "start_date": start_date,
                    "end_date": end_date
                }
                response = get(f'{BACKEND_URL}/filters', json=data).json()

                if isinstance(response, list) and response:
                    for item in response:
                        title = item.get('title', 'No Title')
                        content = item.get('content', 'No Content')
                        published = item.get('published', 'No Published Date')
                        deadline = item.get('deadline', 'No Deadline')

                        message += (
                            f"""\n<b>Title:</b> {title}\n\n
Content: {content}
Published: {published}
Deadline: {deadline}""")
                    await event.respond(message, parse_mode='html')
                else:
                    await event.respond("No tasks found or unexpected response format.")



@client.on(events.NewMessage(pattern='/set_time'))
async def set_time(event):
    user_input = event.text.split()
    if len(user_input) == 2:
        time_parts = user_input[1].split(':')
        if len(time_parts) == 2 and time_parts[0].isdigit() and time_parts[1].isdigit():
            hours = int(time_parts[0])
            minutes = int(time_parts[1])


            hours = (hours - 0) % 24

            if 0 <= hours < 24 and 0 <= minutes < 60:
                global user_id
                user_id = event.sender_id
                user_state = user_states.get(user_id)
                if user_state:
                    email = user_state.get('email')
                    if email:
                        reminder_time = f'{hours:02d}:{minutes:02d}'

                with Session.begin() as session:
                    user = session.query(User).filter(User.email == email).first()
                    if user:
                        user.reminder_time = reminder_time


                job_id = f'reminder_{user_id}'
                if scheduler.get_job(job_id):
                    scheduler.remove_job(job_id)

                scheduler.add_job(
                    send_user_reminder,
                    CronTrigger(hour=hours, minute=minutes),
                    args=[email],
                    id=job_id
                )

                await event.respond(f'Час нагадування встановлено корректно')
            else:
                await event.respond("Некоректний час. Переконайтеся, що години від 0 до 23, а хвилини від 0 до 59")
        else:
            await event.respond("Введіть час у форматі ГГ:ХХ, наприклад /set_time 14:30")
    else:
        await event.respond("Введіть команду у форматі /set_time ГГ:ХХ, наприклад /set_time 14:30")




async def send_user_reminder(email):
    global user_id
    now = datetime.now().date()
    previous_day = now - timedelta(days=1)

    with Session() as session:
        user = session.query(User).filter(User.email == email).first()
        if user:
                await client.send_message(
                    user_id,
                    "Не забудьте перевірити свої завдання!"
                )


scheduler.start()
client.run_until_disconnected()