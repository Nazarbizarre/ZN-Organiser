from telethon import Button as button

login = [
    [button.inline("Login", b'login')]
]


main = [
    [button.inline("All tasks", b'all_tasks')],
    [button.inline("Themes", b'themes')]
]


themes = [
    [button.inline("Hobby", b'theme_Hobby')],
    [button.inline("Games", b'theme_Games')],
    [button.inline("Sports", b'theme_Sports')]
]
