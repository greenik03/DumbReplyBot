# DumbReplyBot (DRB)
A simple bot for AT Protocol (Bluesky) that replies to any post/reply in which it's tagged/mentioned. \
Uses the [atproto SDK](https://github.com/MarshalX/atproto). Written in Python 3.14. \
Powers [rbtestbot.bsky.social](https://bsky.app/profile/rbtestbot.bsky.social).

[//]: # (TODO: Change account link after handle change)
[//]: # (TODO: Add section for building/self-hosting)

# Console commands
The bot has a few commands you can give it in a terminal/command line while it's operating:
- `info` - Prints client and listener info on screen.
- `cache-reset` - Re-reads `phrases.txt` from the data folder and stores the phrases in memory.
- `quit, stop, exit, logout` - Shut down the bot. Just `q` will also do the job.

# Data disclosure
The bot will analyze a user's profile when tagged to look for labels added by Bluesky (for scams, hate speech, harassment, etc.) to avoid suspension. Other than that, no user data is being stored.

# Contributing
[See the contributing guidelines here](CONTRIBUTING.md) for more info.

# License
[MIT](LICENSE)