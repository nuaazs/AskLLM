import os
import time
import torch
import gradio as gr
import pandas as pd
from argparse import ArgumentParser
from flask import Flask, request, jsonify

# utils
import cfg
from bots.common import Bot
bot = Bot()


def chatchat():
    print(cfg.start_text)
    Q = input("你：")
    bot.history.append((cfg.start_text,Q))
    bot.init_chat(Q,bot.history)

if __name__ == "__main__":
    r = chatchat()