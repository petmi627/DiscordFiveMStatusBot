import os, discord, sys, logging, requests, json

version = "1.0.0"
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

    async def on_message(self, message):
        if message.author == client.user:
            return

        if "help" in message.content.lower() and client.user in message.mentions:
            logger.info("Message from {} in {} contains {}".format(str(message.author), message.channel, message.content))
            await message.channel.send(self.config["help_text"])
        if "version" in message.content.lower() and client.user in message.mentions:
            logger.info("Message from {} in {} contains {}".format(str(message.author), message.channel, message.content))
            await message.channel.send('The bot version is {}'.format(version))
        if ("creator" in message.content.lower() or "master" in message.content.lower() or "developer" in message.content.lower()) \
                and client.user in message.mentions:
            logger.info("Message from {} in {} contains {}".format(str(message.author), message.channel, message.content))
            await message.channel.send('I was created by {}'.format(developed_by))

        if "$status" in message.content:
            msg = await message.channel.send("Fetching data, please wait")
            logger.info(
                "Message from {} in {} contains {}".format(str(message.author), message.channel, message.content))
            server = message.content.split(" ")[-1].lower()
            if server in self.config["servers"].keys():
                await message.channel.send(self.getServerInfo(self.config["servers"][server]))
            else:
                for server in self.config["servers"]:
                    print(self.config["servers"][server])
                    await message.channel.send(self.getServerInfo(self.config["servers"][server]))
            await msg.delete()
        if "$players" in message.content:
            msg = await message.channel.send("Fetching data, please wait")
            logger.info(
                "Message from {} in {} contains {}".format(str(message.author), message.channel, message.content))
            server = message.content.split(" ")[-1].lower()
            if server in self.config["servers"].keys():
                await message.channel.send(self.getPlayerInfo(self.config["servers"][server]))
            else:
                await message.channel.send(self.getPlayerInfo(self.config["servers"]["main"]))
            await msg.delete()

        if message.content in self.config['cmd'].keys():
            await message.channel.send(self.config['cmd'][message.content])

    def getServerInfo(self, ip):
        status = self.getJson(self.config['http_info'].format(ip))
        if type(status) == dict:
            logger.info("Server is online")
            return "{} The Server is online. Server IP {}".format(self.config["icon_success"], ip)
        else:
            return status

    def getPlayerInfo(self, ip):
        status = self.getJson(self.config['http_info'].format(ip))
        players = self.getJson(self.config['http_players'].format(ip))

        if type(players) == list and type(status) == dict:
            logger.info("fetching players")
            msg = "There are currently {} of {} players online. Server IP {}\n```".format(len(players), status["vars"]["sv_maxClients"], ip)
            index = 1
            for player in players:
                msg += "#{} - [{}] \"{}\" has a ping of {}\n".format(index, player['id'], player['name'], player['ping'])
                index += 1
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
            return "{} The Server is currently offline".format(self.config["icon_failed"])


if '__main__' == __name__:
    with open('config.json', 'r') as file:
        config = json.load(file)

    client = FiveMStatusClient()
    client.set_config(config)
    client.run(os.environ['token'])