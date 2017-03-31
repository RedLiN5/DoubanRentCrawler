# -*- coding: utf-8 -*-

import requests
from lxml import etree
import re
import datetime
import pandas as pd
import numpy as np
import glob
import os
import sys

def start(urls=None, max_page=50):
    if urls is None:
        raise ValueError('"urls" cannot be empty')

    if isinstance(urls, type):
        pass
    elif isinstance(urls, str):
        pass

def _crawler(url):
    pass

