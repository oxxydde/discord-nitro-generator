# EVERY 5 API REQUESTS SIMULTANEOUSLY, COOLDOWN INCREASES

import os, random, string, requests, json, time, math, os

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

def checkCode(char_length):
    codeIndex = 0
    valids = 0
    with open('valid_codes.txt', 'w') as validFile:
        while True:
            randCode = "".join(random.choices(string.ascii_letters + string.digits, k=char_length))
            base_url = "https://discordapp.com/api/v6/entitlements/gift-codes/"
            url_request = f"{base_url}{randCode}"

            request = requests.get(url_request)

            if (request.status_code == 200):
                appData = request.json()
                nitro = {
                    'name' : appData['store_listing']['sku']['name'],
                    'max_use' : appData['max_uses'],
                    'current_use' : appData['uses']
                }

                output_str = f"VALID CODE NO. {valids + 1}\nApp name : {nitro['name']}\nCurrent uses : {nitro['uses']}\nMax uses : {nitro['max_uses']}\n-----------------------------------"
                validFile.write(f"\n{output_str}")

                valids += 1
                codeIndex += 1

            elif (request.status_code == 429):
                delay = math.ceil(request.json()['retry_after'] / 1000)
                print("Rate limited, delaying on %d seconds | Valids = %d" % (delay, valids))
                time.sleep(delay)

            else:
                print(f"{codeIndex + 1} | Invalid | https://discord.gift/{randCode} | Valids = {valids}")
                codeIndex += 1

def welcomingMessage():
    print("---- DISCORD NITRO GENERATOR by oxx\n---- Version : 0.01 beta 1\n")
    print("Select length of Nitro Code :\n1. 16 characters (Classic)\n2. 24 characters (Nitro + Boost)\n")
    len_char = int(input("INPUT : "))
    if (len_char == 1):
        return 16
    elif (len_char == 2):
        return 24
    else:
        return -1

if __name__ == '__main__':
    if (os.name == 'nt'):
        os.system('cls')
    elif (os.name == 'posix'):
        os.system('clear')

    lengg = welcomingMessage()
    if (lengg > 0):
        checkCode(lengg)
    else:
        print("Wrong input!")
    print('--- END ---')