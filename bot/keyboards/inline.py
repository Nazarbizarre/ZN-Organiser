from telethon import Button as button

login = [
    [button.inline("Login", b'login')]
]


main = [
    [button.inline("All tasks", b'all_tasks')],
    [button.inline("Themes", b'themes')],
    [button.inline("Filter by date", b'filter')]
]


themes = [
    [button.inline("Education", b'theme_Education')],
    [button.inline("Fun", b'theme_Fun')],
    [button.inline("Chores", b'theme_Chores')]
]
