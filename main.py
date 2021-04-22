# EVERY 5 API REQUESTS SIMULTANEOUSLY, COOLDOWN INCREASES

import os, random, string, requests, json, time, math

webhook_url = ""

try:
    from discord_webhook import DiscordWebhook
except ImportError:
    print("discord_webhook modules isn't installed!")
    exit()

def fetchProxies():
    # PROXY NYA MATI
    proxy_url = "https://api.proxyscrape.com/v2/?request=getproxies&protocol=http&timeout=10000&country=all&ssl=all&anonymity=all"
    reqs = requests.get(proxy_url)
    with open('proxies.txt', 'wb') as proxyFile:
        proxyFile.write(reqs.content)

def generateCode(iterations):
    with open('random_codes.txt', 'w') as codeFile:
        for i in range(0, iterations):
            if (i < iterations - 1):
                codeFile.write("%s\n" % ("".join(random.choices(string.ascii_letters + string.digits, k=16))))
            else:
                codeFile.write("%s" % ("".join(random.choices(string.ascii_letters + string.digits, k=16))))

    checkPrompt = input("Do you wanna check the code validity? (Y/N) : ")
    if (checkPrompt.lower() == 'y'):
        checkCode()
    elif (checkPrompt.lower() == 'n'):
        pass

def checkCode():
    with open('random_codes.txt', 'r') as codeFile:
        randCodes = codeFile.read().split('\n')

    codeLen = len(randCodes)
    codeIndex = 0
    while (codeIndex < codeLen):
        base_url = "https://discordapp.com/api/v6/entitlements/gift-codes/"
        url_request = f"{base_url}{randCodes[codeIndex]}"

        request = requests.get(url_request)

        if (request.status_code == 200):
            appData = request.json()
            nitro = {
                'name' : appData['store_listing']['sku']['name'],
                'max_use' : appData['max_uses'],
                'current_use' : appData['uses']
            }
            if ((nitro['max_use'] - nitro['current_use']) > 0):
                canBeClaimed_stringConst = "**THIS CODE IS UNCLAIMED OR CLAIM-ABLE, GO REDEEM NOW!**"
            else:
                canBeClaimed_stringConst = "**THIS CODE HAS BEEN CLAIMED!**"

            finalCodeFound = f"""**--------- CODE FOUND ---------**
            
            **Gift code link : https://discord.gift/{randCodes[codeIndex]}**
            Type : {nitro['name']}
            Current Uses : {nitro['current_use']}
            Max Uses : {nitro['max_use']}
            
            {canBeClaimed_stringConst} @everyone"""

            print(f"Code found, {randCodes[codeIndex]}, sending to the binded webhook")
            
            theWebhook = DiscordWebhook(url=webhook_url, content=finalCodeFound)
            theWebhook.execute()
            codeIndex += 1

        elif (request.status_code == 429):
            delay = math.ceil(request.json()['retry_after'] / 1000)
            print("Rate limited, delaying on %d seconds" % delay)
            time.sleep(delay)

        else:
            print(f"Invalid | https://discord.gift/{randCodes[codeIndex]}")
            codeIndex += 1

if __name__ == '__main__':
    iters = int(input("Input how many codes will be generated : "))
    # save = input("Wanna save to the random_codes.txt file (NOTE : Existing files will be overwritten) [Y/N] : ")
    webhook_url = r"https://discord.com/api/webhooks/833567160890425365/rPR308UwFUq3BiN9htEGoSq6_eO7qei0TH3ZR715SEAs7wZlYs8NHA_y8IS4-lmcwUDD"

    generateCode(iters)