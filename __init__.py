# -*- coding: utf-8 -*-
import json
from naomi import plugin


class VersionChecker(plugin.SpeechHandlerPlugin):
    def intents(self):
        return {
            'VersionIntent': {
                'locale': {
                    'en-US': {
                        'templates': [
                            'CHECK VERSION',
                            'WHAT VERSION ARE YOU RUNNING',
                            'IS AUTO UPDATE ENABLED',
                            'IS AUTO UPDATE DISABLED',
                            'IS AUTO UPDATE ENABLED OR DISABLED',
                            'IS AUTO UPDATE DISABLED OR ENABLED',
                            'ENABLE AUTO UPDATE',
                            'DISABLE AUTO UPDATE'
                        ]
                    }
                },
                'action': self.handle
            }
        }

    def handle(self, intent, mic):
        transcript = intent['input']

        with open('~/.config/naomi/configs/.naomi_options.json' 'r') as optionsFile:
            data = json.load(optionsFile)

            if "VERSION" in transcript:
                mic.say(data['version'])

            if "IS AUTO UPDATE" in transcript:
                auto = data['auto_update']
                if "false" in auto:
                    mic.say("AUTO UPDATE IS DISABLED")
                else "true" in auto:
                    mic.say("AUTO UPDATE IS ENABLED")
        
            if "ENABLE AUTO UPDATE" in transcript:
                auto = data['auto_update']
                if "false" in auto:
                    data['auto_update'] = "true"
                    with open('~/.config/naomi/configs/.naomi_options.json', "w") as optionsFile:
                        json.dump(data, optionsFile)
                    mic.say("ENABLED AUTO UPDATE")
                else "true" in auto:
                    mic.say("AUTO UPDATE IS ALREADY ENABLED")

            if "DISABLE AUTO UPDATE" in transcript:
                auto = data['auto_update']
                if "true" in auto:
                    data['auto_update'] = "false"
                    with open('~/.config/naomi/configs/.naomi_options.json', "w") as optionsFile:
                        json.dump(data, optionsFile)
                    mic.say("DISABLED AUTO UPDATE")
                else "false" in auto:
                    mic.say("AUTO UPDATE IS ALREADY DISABLED")