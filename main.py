import os, random, string, requests, json


try:
    from discord_webhook import DiscordWebhook
except ImportError:
    print("discord_webhook modules isn't installed!")
    exit()
    
class Generator:
    def __init__(self, iterations, webhook = ""):
        self.iter = iterations
        self.webhooks = webhook

    def generateCode(self):
        for i in range(0, self.iter):
            self.randomNitroCode = "".join(random.choices(string.ascii_uppercase + string.digits + string.ascii_lowercase, k=16))
            print(f"Checking code {self.randomNitroCode}")
            self.base_url = "https://discordapp.com/api/v6/entitlements/gift-codes/"
            self.url_request = f"{self.base_url}{self.randomNitroCode}"

            request = requests.get(self.url_request)

            if (request.status_code == 200):
                finalCodeFound = f"Code founded, https://discord.gift/{self.randomNitroCode}"
                print(f"{finalCodeFound}, sending to the binded webhook")
                theWebhook = DiscordWebhook(url=self.webhooks, content=finalCodeFound)
                theWebhook.execute()
            else:
                print(f"Invalid | https://discord.gift/{self.randomNitroCode}")


Gens = Generator(9999, r"https://discord.com/api/webhooks/832796099991437312/aObkC2lZbouttvNuj6NZI900_Wt-V2RQpTGdXCbeZVixDt4w7SKx-5Fmo1NoNEEOLG3Y")
Gens.generateCode()