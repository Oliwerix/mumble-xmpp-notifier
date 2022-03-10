# mumble-xmpp-notifier
A small python script to notify users over xmpp if a person joins a mumble server

## Installation
1. clone this repo `git clone https://github.com/Oliwerix/mumble-xmpp-notifier.git`
2. install required packages `pip3 install -r requirements.txt`
3. copy config.example.yaml `cp config.example.yaml config.yaml`
4. fill out config.yaml
5. run `python3 app.py`

### Example config
    xmpp_jid: bot@example.net 
    xmpp_password: hackme123
    mumble_server: mumble.example.net 
    mumble_port: 64738
    polling_rate: 30 # delay in seconds
    subscribers: # subscriber jids
      - person@example.net
      - john.doe@example.net
## Running as a service
There is a provided systemd service file, copy it to your systemd directory (`/etc/systemd/system/`), and modify the working directory and executable path. Then run `systemctl daemon-reload` and `systemctl enable --now mumble-xmpp-notifier`
