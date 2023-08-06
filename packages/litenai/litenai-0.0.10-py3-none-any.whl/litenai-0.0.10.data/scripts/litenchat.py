
import panel as pn
import hvplot.pandas
import pandas as pd
import numpy as np

import sys

import liten

import litendemo
from litendemo import DemoFiles

class ChatApp():
    def start(self, config_file : str = 'liten.yaml', data_dir : str = 'data'):
        """
        Start chat app
        """
        pn.extension(design='material')
        session = liten.Session.get_or_create('liten', config_file)
        demofiles = DemoFiles(session.spark, liten_data_dir=data_dir)
        demofiles.init()
        chatbot = liten.ChatBot(session)
        chat_panel = chatbot.start()
        chat_panel.servable()

def print_usage():
    print(f"""
Usage: python chatapp.py <config_file> <data_dir>
Example: python chatapp.py liten.yaml data
Received: f{sys.argv}
""")

config_file = 'liten.yaml'
data_dir = 'data'

if len(sys.argv)==3:
    config_file = sys.argv[1]
    data_dir = sys.argv[2]
    ChatApp().start(config_file=config_file, data_dir=data_dir)
else:
    print_usage()
