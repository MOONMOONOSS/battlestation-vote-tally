# -*- coding: utf-8 -*-

# Copyright (C) 2019 Moonmoon 

import yaml
import re
import os

OS_ENVIRON_PREFIX = 'MOONMOON_VOTE_COUNT_'

bot_config = dict()

with open("config.yaml", "r") as config_file:
    bot_config = yaml.safe_load(config_file)

bot_config['bot_token'] = os.environ.get(OS_ENVIRON_PREFIX + 'TOKEN', None)

if __name__ == '__main__':
  print(os.environ.get(OS_ENVIRON_PREFIX + 'TOKEN')) ## discord token loaded in enviroment
