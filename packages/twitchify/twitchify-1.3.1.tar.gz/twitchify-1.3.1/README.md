# Twitchify

[![Discord](https://img.shields.io/discord/938786168592547880)](https://discord.gg/hH4ZkNg6cA)
[![PyPI Version](https://img.shields.io/pypi/v/twitchify)](https://pypi.org/project/twitchify)
[![Python versions](https://img.shields.io/pypi/pyversions/twitchify)](https://pypi.org/project/twitchify)

Python library for Twitch's WebSocket **EventSub** integration.

## Features
- Comprehensive support for WebSocket EventSub, providing real-time Twitch event notifications.
- User-friendly interfaces for seamless integration.
- Built-in support for type hinting, ensuring code clarity and maintainability.

## Installation
You can install Twitchify using pip:

```shell
# Windows
py -3 -m pip install -U twitchify

# Linux/macOS
python3 -m pip install -U twitchify
```

## Quick Example
```python
from twitch import Client
from twitch.user import Follower

client = Client(client_id="YOUR_CLIENT_ID")

@client.event
async def on_ready():
    """
    Event handler triggered when the client is ready to start processing events.
    """
    print("Ready as %s" % client.user.display_name)


@client.event
async def on_follow(user: Follower):
    """
    Event handler triggered when a user follows the channel.
    """
    print("%s just followed you!" % user.display_name)

# Run the client with your user access token.
client.run(access_token="YOUR_ACCESS_TOKEN")
```

### With built-in Authorization

```python
from twitch import Client
from twitch.user import Follower

client = Client(client_id="YOUR_CLIENT_ID", client_secret="YOUR_CLIENT_SECRET")

@client.event
async def on_ready():
    """
    Event handler triggered when the client is ready to start processing events.
    """
    print("Ready as %s" % client.user.display_name)
    
@client.event
async def on_follow(user: Follower):
    """
    Event handler triggered when a user follows the channel.
    """
    print("%s just followed you!" % user.display_name)

@client.event
async def on_auth(access_token: str, refresh_token: str):
    """
    Event handler triggered when the user authorized to the app.
    """
    # Store those for future use.
    print('Received access token:', access_token)
    print('Received refresh token:', refresh_token)
    
# Generate the authorization URL for the Twitch client.
# The user should visit the provided URL to authorize the app.
client.run()
```

Please refer to the [Documentation](https://github.com/MrSniFo/Twitchify/blob/main/docs) or [Examples](https://github.com/MrSniFo/Twitchify/tree/main/examples) for more details.
