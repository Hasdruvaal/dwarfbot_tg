# TODO:
1. Cover all interface and managers functions by unit-test
2. Merge `info` and `my` commands in one (from private `info` should work like an `my` at the moment). Delete `my` command.
3. Write a `help` command and show this after `auth`
4. As a curator i want to manage players-list and session (delete players from list, set status to other player)
5. As a player i want to skip my step without sending a save (now only curator have possibility)
6. As a admin i want to have a instrument to manage database. I find is good idea to have a django-grappelli or smt like that. 
7. Remove hardcode in 7-days step time. Ideally each session must have it like an option.

# About
It's telegram bot for sucession game managment. Created by the idea of [russian df community](https://t.me/DwarfFortressRus)-members. You can find telegram developers [here](https://t.me/dfbotsetup).

# Set up
## Installing:
 1. Clone repository
 2. Install docker and docker-compose
 3. Make `.env` file from `env.example` (look below)
 5. Start `docker-compose up -d`

## Env-file:
1. Get bot token from [@BotFather](https://t.me/botfather)
2. Get google-secret from [google developer console](https://console.developers.google.com/apis/credentials)
3. Get imgur api-keys. Read more: [imgur api doc](https://apidocs.imgur.com/#authorization-and-oauth)
4. Create google-drive folder through web-interface and extract folder-id from url: https://drive.google.com/drive/folders/YOUR_ID
5. Set up user/password/dbname/host/port
6. Fill up `.env` with your data like `env.example`

# Usage
## Users
1. `auth` - Authorise user

Note: each player or/and curator __must__ be authorised by a bot!

## Session managment
1. `create [arg]` - create session. If `[arg]` is empty it will be `Utitled`.
2. `delete` - delete session. Your must be sure, you can't cancel or undone this operation. Available only for new-sessions without any status.
3. `name [arg]` - (Re)name game. If `[arg]` is empty, it return session name. If not, it set `[arg]` as a name
4. `description [arg]` - Set or show description. If `[arg]` is not empty, `[arg]` be a new description.
5. `embark` or `start` - Set session status to a active. It means game is started by curator. Can't be undone.
6. `abandon` or `stop` - Stop session. It means game is stoped (not deleted!) by curator. Can't be undode. You can't start a deleted session.

## Player managment
1. `toggle` - Add or delete initiator to player-list
2. `shuffle` - Shuffle players in the list. Only for new-sessions, need to be a curator of this session.
3. `skip` - Skip current player step. Only for new-sessions, need to be a curator of this session.
4. `add` - Add player to tail of the list. Need to be a curator of this session.
5. `round [arg]` - Repeat players list. If `[arg]` is not empy, repeated part be shuffled.

## Info
1. `info [arg]` - Show info about current or `[arg]` session. `[arg]` can be a name of any session, or session id. You can get session id and name by `my` (look below)
2. `my` - Show info about all your sessions
3. `players` - Show player list of current session

## Game
1. `retire` or `next` - Close you step and send save to the cloud and to the next player. Private only.
2. `fact` - Add information about your game into the gooogle document. Can be use for images so you need to set command as a caption

Note: Any step will be closed after 7-days automatically. You can't change that time, it's hardcoded.
