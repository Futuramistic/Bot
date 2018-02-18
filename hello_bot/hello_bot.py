#!/usr/bin/env python
#  -*- coding: utf-8 -*-
import csv
import random
# 3rd party imports ------------------------------------------------------------
from flask import Flask, request
from ciscosparkapi import CiscoSparkAPI, Webhook
from collections import defaultdict

# local imports ----------------------------------------------------------------
from helpers import (read_yaml_data,
                     get_ngrok_url,
                     find_webhook_by_name,
                     delete_webhook, create_webhook)

flask_app = Flask(__name__)
spark_api = None
interaction = defaultdict(list)
response = defaultdict(list)
used = []
query = []
type = []
with open('interactions.csv') as csvfile:
    readCSV = csv.reader(csvfile, delimiter=',')
    for row in readCSV:
        key = row[0]
        action = row[1]
        solution = row[2]
        interaction[key].append(action)
        response[action].append(solution)

@flask_app.route('/sparkwebhook', methods=['POST'])
def sparkwebhook():
    if request.method == 'POST':

        json_data = request.json
        print("\n")
        print("WEBHOOK POST RECEIVED:")
        print(json_data)
        print("\n")

        webhook_obj = Webhook(json_data)
        # Details of the message created
        room = spark_api.rooms.get(webhook_obj.data.roomId)
        message = spark_api.messages.get(webhook_obj.data.id)
        person = spark_api.people.get(message.personId)
        email = person.emails[0]

        print("NEW MESSAGE IN ROOM '{}'".format(room.title))
        print("FROM '{}'".format(person.displayName))
        print("MESSAGE '{}'\n".format(message.text))

        # Message was sent by the bot, do not respond.
        # At the moment there is no way to filter this out, there will be in the future
        me = spark_api.people.me()
        if message.personId == me.id:
            return 'OK'
        else:
            string = message.text.replace(',', '')
            string = string.replace('.', '')
            string = string.lower()
            words = string.split(' ')
            x=0
            i=0
            while (i<len(words) and x==0):
                word = words[i]
                if(type != []):
                    if(word == 'yes'):
                        type.remove(1)
                        spark_api.messages.create(room.id, text=random.choice(interaction['another']))
                        x=1
                    elif(word == 'no'):
                        spark_api.messages.create(room.id, text=random.choice(interaction['goodbye']))
                        sys.exit(0)
                else:
                    if(word == 'yes'):
                        if(interaction[word]!=[]):
                            s=str(random.choice(interaction[word]))
                            interaction[word].remove(s)
                            x=str(random.choice(interaction[used[-1]]))
                            query.append(x)
                            interaction[used[-1]].remove(x)
                            s=s+x
                            spark_api.messages.create(room.id, text=s)
                            x=1
                    elif(word == 'no'):
                            r = str(response[query[-1]])
                            r = r.replace('[','')
                            r = r.replace(']','')
                            r = str(r[1:-1])
                            r = r + ' '
                            w = str(interaction['nextquery'])
                            w = w.replace('[','')
                            w = w.replace(']','')
                            w = str(w[1:-1])
                            r=r+w
                            type.append(1)
                            x=1
                            spark_api.messages.create(room.id, text=r)
                    elif(word in interaction):
                        used.append(word)
                        if(interaction[word]!=[]):
                            s=random.choice(interaction[word])
                            query.append(s)
                            spark_api.messages.create(room.id, text=s)
                            interaction[word].remove(s)
                            x=1
                    i=i+1
            if(x==0):
                spark_api.messages.create(room.id, text=random.choice(interaction['generic']))

    else:
        print('received none post request, not handled!')


if __name__ == '__main__':
    config = read_yaml_data('/opt/config/config.yaml')['hello_bot']
    spark_api = CiscoSparkAPI(access_token=config['spark_access_token'])

    ngrok_url = get_ngrok_url()
    webhook_name = 'hello-bot-wb-hook'
    dev_webhook = find_webhook_by_name(spark_api, webhook_name)
    if dev_webhook:
        delete_webhook(spark_api, dev_webhook)
    create_webhook(spark_api, webhook_name, ngrok_url + '/sparkwebhook')

    flask_app.run(host='0.0.0.0', port=5000)
