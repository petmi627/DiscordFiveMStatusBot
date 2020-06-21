import os, discord, sys, logging, requests, json, random, time

version = "1.1.1"
developed_by = "KywoSkylake: https://github.com/petmi627"

logger = logging.getLogger()
logger.setLevel(logging.INFO)
handler = logging.StreamHandler(sys.stdout)
handler.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s [%(levelname)s] - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)

class FiveMStatusClient(discord.Client):

    config = None

    def set_config(self, config):
        self.config = config

    async def on_ready(self):
        """
        The Bot started
        :return:
        """
        logger.info("I started up. Beep Bop")
        await self.change_presence(activity=discord.Game(name="mention me with a message containing the word help"))

    async def on_message(self, message):
        if message.author == client.user:
            return

        if client.user in message.mentions:
            self.logUserMessage(message)
            if "help" in message.content.lower():
                await message.channel.send(self.config["help_text"])
            if "version" in message.content.lower():
                await message.channel.send('The bot version is {}'.format(version))
            if "creator" in message.content.lower() or "master" in message.content.lower() \
                or "developer" in message.content.lower() or "created" in message.content.lower():
                await message.channel.send('I was created by my master {}'.format(developed_by))

        if self.startsWith(message.content.lower(), ["$", "?", "!", "/"]):
            self.logUserMessage(message)
            message_received = message.content.lower()[1:]
            if message_received in self.config['cmd'].keys():
                await message.channel.send(self.config['cmd'][message_received])
            elif self.startsWith(message_received, ["players", "status"]):
                server = message.content.split(" ")[-1].lower()
                fetching = await message.channel.send(self.getRandomMessages('loading'))
                time.sleep(1)
                if message_received.startswith("status"):
                    resp = self.retrivingServerInfo(server)
                    if type(resp) == list:
                        for msg in self.retrivingServerInfo(server):
                            await message.channel.send(msg)
                    else:
                        await message.channel.send(resp)
                if message_received.startswith("players"):
                    await message.channel.send(self.retrivingPlayerlist(server))
                await fetching.delete()

    def logUserMessage(self, message):
        logger.info(
            "Message from {} in {} contains {}".format(str(message.author), message.channel, message.content))

    def retrivingServerInfo(self, server):
        if server in self.config["servers"].keys():
            return self.getServerInfo(server, self.config["servers"][server])
        msg = []
        for server in self.config["servers"]:
            msg.append(self.getServerInfo(server, self.config["servers"][server]))
        return msg

    def retrivingPlayerlist(self, server):
        if server in self.config["servers"].keys():
            return self.getPlayerInfo(server, self.config["servers"][server])
        if len(self.config["servers"]) == 1:
            for server in self.config["servers"]:
                return self.getServerInfo(server, self.config["servers"][server])

        return self.getPlayerInfo('main', self.config["servers"]["main"])

    def getServerInfo(self, server, ip):
        status = self.getJson(self.config['http_info'].format(ip))
        if type(status) == dict:
            logger.info("Server is online")
            return "{} {} server with IP {}:  {}".format(self.config["icon_success"], server, ip, self.getRandomMessages("online"))
        else:
            return status

    def getPlayerInfo(self, server, ip):
        status = self.getJson(self.config['http_info'].format(ip))
        players = self.getJson(self.config['http_players'].format(ip))
        if type(players) == list and type(status) == dict:
            logger.info("fetching players")
            msg = "{}, {} server IP {}\n".format(self.getRandomMessages('players').format(len(players), status["vars"]["sv_maxClients"]), server, ip)
            if len(players) > 0:
                msg+="```python\n"
            index = 1
            for player in players:
                msg += "Nr. {} - [{}] \"{}\" has a ping of {}\n".format(index, player['id'], player['name'], player['ping'])
                index += 1
                if len(players) == index-1:
                    msg += "```"
            return msg
        else:
            return players

    def getJson(self, url):
        try:
            r = requests.get(url)
            if r.status_code == 200:
                return r.json()
            else:
                logger.error("Got an {} status code from".format(r.status_code, url))
                return "{} I'm sorry an error occurred, I cannot get the status of the Server".format(self.config["icon_failed"])
        except BaseException as e:
            logger.error("Cannot reach page {} fallow error message {}".format(url, e), exc_info=True)
            return "{} {}".format(self.config["icon_failed"], self.getRandomMessages("offline"))

    def getRandomMessages(self, pool):
        return random.choice(self.config["messages"][pool])

    def startsWith(self, message, list):
        for item in list:
            if str(message).startswith(item):
                return True
        return False

if '__main__' == __name__:
    with open('config.json', 'r') as file:
        config = json.load(file)
    client = FiveMStatusClient()
    client.set_config(config)
    client.run(os.environ['token'])