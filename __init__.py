# -*- coding: utf-8 -*-
import json
from naomi import paths
from naomi import plugin


CONFIG_FILE = paths.config('.naomi_options.json')

class VersionChecker(plugin.SpeechHandlerPlugin):
    def intents(self):
        return {
            'VersionIntent': {
                'locale': {
                    'en-US': {
                        'templates': [
                            'CHECK VERSION',
                            'WHAT VERSION ARE YOU RUNNING'
                        ]
                    }
                },
                'action': self.handleCheckVersion
            },
            'CheckAutoUpdateIntent': {
                'locale': {
                    'en-US': {
                        'templates': [
                            'IS AUTO UPDATE ENABLED',
                            'IS AUTO UPDATE DISABLED',
                            'IS AUTO UPDATE ENABLED OR DISABLED',
                            'IS AUTO UPDATE DISABLED OR ENABLED'
                        ]
                    }
                },
                'action': self.handleCheckAutoUpdate
            },
            'ControlAutoUpdateIntent':{
                'locale': {
                    'en-US': {
                        'keywords': {
                            'ActionKeyword': [
                                'ENABLE',
                                'DISABLE'
                            ]
                        },
                        'templates': [
                            '{ActionKeyword} AUTO UPDATE'
                        ]
                    }
                },
                'action': self.handleControlAutoUpdate
            }
        }

    def handleCheckVersion(self, intent, mic):
        with open(CONFIG_FILE, 'r') as optionsFile:
            data = json.load(optionsFile)
        mic.say(data['version'])
        return True

    def handleCheckAutoUpdate(self, intent, mic):
        with open(CONFIG_FILE, 'r') as optionsFile:
            data = json.load(optionsFile)
        auto = data['auto_update']
        if 'true' in auto:
            mic.say(self.gettext("AUTO UPDATE IS ENABLED"))
        elif 'false' in auto:
            mic.say(self.gettext("AUTO UPDATE IS DISABLED"))
        return True
    
    def handleControlAutoUpdate(self, intent, mic):
        with open(CONFIG_FILE, 'r') as optionsFile:
            data = json.load(optionsFile)
        auto = 'true' in data['auto_update']
        if 'ActionKeyword' in intent['matches']:
            for action in intent['matches']['ActionKeyword']:
                if action == 'ENABLE':
                    if auto:
                        mic.say(self.gettext('AUTO UPDATE IS ALREADY ENABLED'))
                    else:
                        mic.say(self.gettext('ENABLING AUTO UPDATE'))
                        data['auto_update'] = "true"
                elif action == 'DISABLE':
                    if auto:
                        mic.say(self.gettext('DISABLING AUTO UPDATE'))
                        data['auto_update'] = "false"
                    else:
                        mic.say(self.gettext('AUTO UPDATE IS ALREADY DISABLED'))
                else:
                    mic.say(self.gettext('PARDON?'))
            with open(CONFIG_FILE, "w") as optionsFile:
                json.dump(data, optionsFile)
        return True

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
                elif "true" in auto:
                    mic.say("AUTO UPDATE IS ENABLED")
        
            if "ENABLE AUTO UPDATE" in transcript:
                auto = data['auto_update']
                if "false" in auto:
                    data['auto_update'] = "true"
                    with open('~/.config/naomi/configs/.naomi_options.json', "w") as optionsFile:
                        json.dump(data, optionsFile)
                    mic.say("ENABLED AUTO UPDATE")
                elif "true" in auto:
                    mic.say("AUTO UPDATE IS ALREADY ENABLED")

            if "DISABLE AUTO UPDATE" in transcript:
                auto = data['auto_update']
                if "true" in auto:
                    data['auto_update'] = "false"
                    with open('~/.config/naomi/configs/.naomi_options.json', "w") as optionsFile:
                        json.dump(data, optionsFile)
                    mic.say("DISABLED AUTO UPDATE")
                elif "false" in auto:
                    mic.say("AUTO UPDATE IS ALREADY DISABLED")
