import requests
import json

class Embed:
    def __init__(self):
        self.title = ""
        self.description = ""
        self.url = ""
        self.color = 0
        self.timestamp = ""
        self.fields = []

    def set_title(self, title):
        self.title = title
        return self
    
    def set_description(self, description):
        self.description = description
        return self

    def set_url(self, url):
        self.url = url
        return self
    
    def set_color(self, color):
        self.color = color
        return self
    
    def set_timestamp(self, timestamp):
        self.timestamp = timestamp
        return self
    
    def add_field(self, name, value, inline):
        self.fields.append({"name": name, "value": value, "inline": inline})
        return self
    
    def get_embed(self):
        return {
            "title": self.title,
            "description": self.description,
            "url": self.url,
            "color": self.color,
            "timestamp": self.timestamp,
            "fields": self.fields
        }

class DiscordHook:
    def __init__(self, url):
        self.url = url
        self.content = ""
        self.username = ""
        self.avatar_url = ""
        self.tts = False
        self.embeds = []

    def set_content(self, content):
        self.content = content
        return self
    
    def set_username(self, username):
        self.username = username
        return self
    
    def set_avatar_url(self, avatar_url):
        self.avatar_url = avatar_url
        return self
    
    def set_tts(self, tts):
        self.tts = tts
        return self
    
    def add_embed(self, embed: Embed):
        self.embeds.append(embed.get_embed())
        return self
    
    def send(self):
        data = {
            "content": self.content,
            "username": self.username,
            "avatar_url": self.avatar_url,
            "tts": self.tts,
            "embeds": self.embeds
        }
        headers = {
            "Content-Type": "application/json"
        }
        requests.post(self.url, data=json.dumps(data), headers=headers)
        return self