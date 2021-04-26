import requests
import datetime
import time
import json
from send_sms import send_sms
from random import randint
from add_last_drop import add_last_drop
from playsound import playsound

if_twilio_number = False #set to true to receive SMS or false to not receive
your_phone_number = '+15144206969'
your_twilio_number = '+12533439473' #set up a twilio account

def bestbuy():

    headers = {
        "Accept": "*/*",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "en-US,en;q=0.5",
        "Cache-Control": "max-age=0",
        "Connection": "keep-alive",
        "Host": "www.bestbuy.ca",
        "Referer": "https://www.bestbuy.ca/en-ca/product/nvidia-geforce-rtx-3070-8gb-gddr6-video-card-only-at-best-buy/15078017",
        "TE": "Trailers",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:72.0) Gecko/20100101 Firefox/72.0"
    }

    #products that will be researched
    SKUS = [
        ['RTX3070', 15078017],
        ['RTX3070_VENTUS', 15038016],
        ['RTX3060Ti', 15166285],
        ['RTX3080_ASUS', 14953248],
        ['RTX3080_ROG', 14954116],
        ['RTX3070_ASUS', 15053087],
        ['RTX3060Ti_EVGA', 15229237],
        ['RTX3080_Ventus', 14950588],
        ['RTX3090_ASUS', 14953247],
        ['RTX3060_EVGA', 15318940],
        ['RTX3080_ZOTAC', 14953249],
        ['RTX3090_ROG', 14954117],
        ['RTX3090_EVGA', 14967857],
        ['RTX3090_MSI', 14966477],
        ['RTX3070_ZOTAC', 15000079],
        ['RTX3070_ZOTAC_OC', 15000078],
        ['RTX3080_ZOTAC_OC', 15000077],
        ['RTX3090_ZOTAC', 14953250],
        ['RTX3070_ASUS_OC', 15053086],
        ['RTX3070_ROG_OC', 15053085],
        ['RTX3060_MSI', 15324508],
        ['PS5_Digi', 14962184],
        ['PS5', 14962185],
    ]

    URL = []
    for i in range(len(SKUS)):
        URL.append(
            f'https://www.bestbuy.ca/ecomm-api/availability/products?accept=application%2Fvnd.bestbuy.standardproduct.v1%2Bjson&accept-language=en-CA&locations=977%7C203%7C931%7C62%7C617%7C927%7C965%7C57%7C938%7C237%7C943%7C932%7C956%7C202%7C200%7C937%7C926%7C795%7C916%7C544%7C910%7C954%7C207%7C233%7C930%7C622%7C223%7C245%7C925%7C985%7C990%7C959%7C949%7C942&postalCode=M5G2C3&skus={str(SKUS[i][1])}')

    #setting the lists with the correct length
    quantity = [0] * len(SKUS)
    response = [0] * len(SKUS)
    response_formatted = [0] * len(SKUS)
    status = [0] * len(SKUS)
    is_in_stock = [0] * len(SKUS)
    attempts = 0
    data = {}
    data['BBdrops'] = []


    while True:
        try:
            if 17 >= int(datetime.datetime.now().strftime('%H')) >= 7 and datetime.datetime.today().weekday() <= 4:     #active from 7am to 6pm on weekdays
                for i in range(len(SKUS)):
                    response[i] = requests.get(URL[i], headers=headers)
                    response_formatted[i] = json.loads(response[i].content.decode('utf-8-sig').encode('utf-8'))
                    status[i] = {SKUS[i][0]: response_formatted[i]['availabilities'][0]['shipping']['status'],
                                 'Qty': response_formatted[i]['availabilities'][0]['shipping']['quantityRemaining']}

                    quantity[i] = status[i]['Qty']

                    if quantity[i] < 1:
                        now = datetime.datetime.now()
                        is_in_stock[i] = 0


                    #printing availability and sending sms through twilio
                    if quantity[i] >= 1 and is_in_stock[i] < 1:
                        if if_twilio_number == True:
                            send_sms('IN STOCKKKK!!!!!! BESTBUY', your_twilio_number, your_phone_number)
                            time.sleep(0.1)
                            send_sms(SKUS[i][0], your_twilio_number, your_phone_number)
                            time.sleep(1)
                            print('IN STOCK! Quantity = ' + str(quantity[i]))
                        playsound('BOMB_SIREN.MP3', block=False)

                        is_in_stock[i] = 1
                        add_last_drop(SKUS[i][0],str(now.strftime("%Y-%m-%d %H:%M:%S"),quantity[i]))

                        #adding the drop to a json file to record drop history
                        data['BBdrops'].append({
                            'Article Name':str(SKUS[i][0]),
                            'Article SKU':str(SKUS[i][1]),
                            'Time of drop':str(now.strftime("%Y-%m-%d %H:%M:%S")),
                            'Quantity':{str(quantity[i])},
                        })

                print('Time : ' + str(now.strftime("%Y-%m-%d %H:%M:%S")) + '  /  Attempts : ' + str(attempts))
                attempts += 1

                for i in range(len(SKUS)):
                    print(SKUS[i][0] + str(" " * (20 - len(SKUS[i][0])) + "STATUS : " + str(status[i][SKUS[i][0]]) + " " * (18 - len(status[i][SKUS[i][0]])) + " QTY : " + str(quantity[i]) + "   STORE : BestBuy"))
                time.sleep(randint(7, 12))

            else:
                print('The time is ', datetime.datetime.now().strftime('%H:%M'))
                print('The program will start running at 8:00 am on the next weekday')
                time.sleep(60)

        except Exception:
            print(
                'FILE ERROR ' + 'Time : ' + str(now.strftime("%Y-%m-%d %H:%M:%S")) + '  /  Attempts : ' + str(attempts))
            pass


if __name__ == "__main__":
    bestbuy()
