from flask import Flask
from github import Github

from config import TOKEN

g = Github(TOKEN)
app = Flask(__name__)

from pages import *

if __name__ == '__main__':
  app.run()