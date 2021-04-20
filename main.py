# EVERY 5 API REQUESTS SIMULTANEOUSLY, COOLDOWN INCREASES

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

    def fetchProxies(self):
        # PROXY NYA MATI
        self.proxy_url = "https://api.proxyscrape.com/v2/?request=getproxies&protocol=http&timeout=50&country=all&ssl=all&anonymity=all&simplified=true"
        self.reqs = requests.get(self.proxy_url)
        with open('proxies.txt', 'wb') as proxyFile:
            proxyFile.write(self.reqs.content)

    def generateCode(self):
        
        self.fetchProxies()
        with open('proxies.txt', 'rb') as proxyFile:
            self.proxy_lists = proxyFile.read().decode().split('\r\n')
        
        self.proxy_lists_amount = len(self.proxy_lists)
        # self.proxy_lists_amount = 1

        self.iter = 0
            
        while (self.iter < self.proxy_lists_amount):
            try:
                self.randomNitroCode = "".join(random.choices(string.ascii_uppercase + string.digits + string.ascii_lowercase, k=16))
                print(f"Checking code https://discord.gift/{self.randomNitroCode}")
                self.base_url = "https://discordapp.com/api/v6/entitlements/gift-codes/"
                self.url_request = f"{self.base_url}{self.randomNitroCode}"

                # PROXY SELECT
                proxy_query = { 
                    "http" : f"http://{self.proxy_lists[self.iter]}",
                    "https" : f"http://{self.proxy_lists[self.iter]}"
                }

                request = requests.get(self.url_request, proxies=proxy_query)

                if (request.status_code == 200):
                    appData = request.json()
                    self.nitro = {
                        'name' : appData['store_listing']['sku']['name'],
                        'max_use' : appData['max_uses'],
                        'current_use' : appData['uses']
                    }
                    if ((self.nitro['max_use'] - self.nitro['current_use']) > 0):
                        self.canBeClaimed_stringConst = "**THIS CODE IS UNCLAIMED, GO REDEEM NOW!**"
                    else:
                        self.canBeClaimed_stringConst = "**THIS CODE HAS BEEN CLAIMED!**"

                    finalCodeFound = f"**--------- CODE FOUND ---------**\n\n**Gift code link : https://discord.gift/{self.randomNitroCode}**\nType : {self.nitro['name']}\nCurrent Uses : {self.nitro['current_use']}\nMax Uses : {self.nitro['max_use']}\n\n{self.canBeClaimed_stringConst} @everyone\n"

                    print(f"Code found, {self.randomNitroCode}, sending to the binded webhook")
                    
                    theWebhook = DiscordWebhook(url=self.webhooks, content=finalCodeFound)
                    theWebhook.execute()

                elif (request.status_code == 429):
                    self.iter += 1
                    
                    if (self.iter < self.proxy_lists_amount):
                        print(f"Rate Limited, changing proxy to {self.proxy_lists[self.iter]}...")
                    else:
                        print("Rate Limited, EOF proxy lists, terminating...")

                else:
                    print(f"Invalid | https://discord.gift/{self.randomNitroCode}")
            except:
                print("Proxy error, next proxy...")
                self.iter += 1
                continue


# CONST
webhook_url = r"https://discord.com/api/webhooks/833567160890425365/rPR308UwFUq3BiN9htEGoSq6_eO7qei0TH3ZR715SEAs7wZlYs8NHA_y8IS4-lmcwUDD"

Gens = Generator(100, webhook_url)
Gens.generateCode()