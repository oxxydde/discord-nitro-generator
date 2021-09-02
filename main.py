# EVERY 5 API REQUESTS SIMULTANEOUSLY, COOLDOWN INCREASES

import os, random, string, requests, json, time, math, os

def fetchProxies():
    # SEVERAL PROXY ARE ACTIVE
    proxy_url = "https://proxylist.geonode.com/api/proxy-list?limit=50&page=1&sort_by=lastChecked&sort_type=desc&filterLastChecked=3&speed=medium"
    reqs = requests.get(proxy_url)
    with open('proxies.json', 'wb') as proxyFile:
        proxyFile.write(reqs.content)

# DEPRECATED
# def generateCode(iterations):
#     with open('random_codes.txt', 'w') as codeFile:
#         for i in range(0, iterations):
#             if (i < iterations - 1):
#                 codeFile.write("%s\n" % ("".join(random.choices(string.ascii_letters + string.digits, k=16))))
#             else:
#                 codeFile.write("%s" % ("".join(random.choices(string.ascii_letters + string.digits, k=16))))

#     checkPrompt = input("Do you wanna check the code validity? (Y/N) : ")
#     if (checkPrompt.lower() == 'y'):
#         checkCode()
#     elif (checkPrompt.lower() == 'n'):
#         pass

def checkCode(char_length):
    with open('proxies.json', 'r') as proxyFile:
        proxyLists = (json.loads(proxyFile.read()))['data']
    codeIndex = 0
    valids = 0

    proxyListsLength = len(proxyLists)
    proxyListsIndex = 0

    with open('valid_codes.txt', 'w') as validFile:
        while True:
            try:
                randCode = "".join(random.choices(string.ascii_letters + string.digits, k=char_length))
                base_url = "https://discordapp.com/api/v6/entitlements/gift-codes/"
                url_request = f"{base_url}{randCode}"

                proxyreq = {
                    'http': f"{proxyLists[proxyListsIndex]['protocols'][0]}://{proxyLists[proxyListsIndex]['ip']}:{proxyLists[proxyListsIndex]['port']}",
                    'https': f"{proxyLists[proxyListsIndex]['protocols'][0]}://{proxyLists[proxyListsIndex]['ip']}:{proxyLists[proxyListsIndex]['port']}"
                }

                request = requests.get(url_request, proxies=proxyreq)

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
                    print("RATE LIMITED, CHANGING PROXY...")
                    proxyListsIndex += 1
                    if (proxyListsIndex >= proxyListsLength):
                        proxyListsIndex = 0
                    # delay = math.ceil(request.json()['retry_after'] / 1000)
                    # print("Rate limited, delaying on %d seconds | Valids = %d" % (delay, valids))
                    # time.sleep(delay)

                else:
                    print(f"{codeIndex + 1} | Invalid | https://discord.gift/{randCode} | Valids = {valids}")
                    codeIndex += 1
            except (requests.exceptions.ConnectionError, requests.exceptions.SSLError, requests.exceptions.ChunkedEncodingError):
                print("PROXY ERROR, CHANGING PROXY...")
                proxyListsIndex += 1
                if (proxyListsIndex >= proxyListsLength):
                    proxyListsIndex = 0


def welcomingMessage():
    print("---- DISCORD NITRO GENERATOR by oxx\n---- Version : 1.1b1\n")
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
        fetchProxies()
        checkCode(lengg)
    else:
        print("Wrong input!")
    print('--- END ---')