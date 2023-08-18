# test env.py

import env

# bot's discord token (it's a secret ;-))
def test_discord_token():
    assert env.get('DISCORD_TOKEN')
