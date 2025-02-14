#!/usr/bin/env python3
# Simple Discord faucetbot
# Created By Viloid ( github.com/vsec7 ) modified by fauzi69
# Use At Your Own Risk

import requests, random, sys, yaml, time

class Discord:

    def __init__(self, t):
        self.base = "https://discord.com/api/v9"
        self.auth = { 'authorization': t }
        
    def getMe(self):
        u = requests.get(self.base + "/users/@me", headers=self.auth).json()
        return u
        
    def getMessage(self, cid, l):
        u = requests.get(self.base + "/channels/" + str(cid) + "/messages?limit=" + str(l), headers=self.auth).json()
        return u
        
    def sendMessage(self, cid, txt):    
        u = requests.post(self.base + "/channels/" + str(cid) + "/messages", headers=self.auth, json={ 'content': txt }).json()
        return u

    def replyMessage(self, cid, mid, txt):    
        u = requests.post(self.base + "/channels/" + str(cid) + "/messages", headers=self.auth, json={ 'content': txt, 'message_reference': { 'message_id': str(mid) } }).json()
        return u

    def deleteMessage(self, cid, mid):
        u = requests.delete(self.base + "/channels/" + str(cid) + "/messages/" + str(mid), headers=self.auth)
        return u

def convert_to_seconds(days, hours, minutes):
    """Convert days, hours, and minutes into total seconds."""
    total_seconds = (days * 86400) + (hours * 3600) + (minutes * 60)
    return total_seconds

def main():
    with open('config.yaml') as cfg:
        conf = yaml.load(cfg, Loader=yaml.FullLoader)

    if not conf['BOT_TOKEN']:
        print("[!] Please provide discord token at config.yaml!")
        sys.exit()

    if not conf['CHANNEL_ID']:
        print("[!] Please provide channel id at config.yaml!")
        sys.exit()

    # Get delay configuration (in minutes, hours, and days)
    delay_days = conf['DELAY_DAYS']
    delay_hours = conf['DELAY_HOURS']
    delay_minutes = conf['DELAY_MINUTES']

    # Convert delay to total seconds
    delay = convert_to_seconds(delay_days, delay_hours, delay_minutes)

    while True:
        for token_index, token in enumerate(conf['BOT_TOKEN']):
            try:
                for chan in conf['CHANNEL_ID']:
                    Bot = Discord(token)
                    me = Bot.getMe()['username'] + "#" + Bot.getMe()['discriminator']
                    
                    with open("faucet.txt", "r") as file:
                        faucet_lines = file.readlines()
                    
                    if faucet_lines:  # Ensure faucet.txt is not empty
                        # Get the message based on the token index
                        if token_index < len(faucet_lines):
                            message = faucet_lines[token_index].strip()
                            send = Bot.sendMessage(chan, message)
                            print("[{}][{}][FAUCET] {}".format(me, chan, message))            

            except Exception as e:
                print(f"[Error] {token} : {str(e)}")

        print("-------[ Delay for {} seconds ]-------".format(delay))
        time.sleep(delay)

if __name__ == '__main__':
    try:
        main()
    except Exception as err:
        print(f"{type(err).__name__} : {err}")
