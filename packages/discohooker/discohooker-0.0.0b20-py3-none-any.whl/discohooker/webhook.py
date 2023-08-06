from .errors import Errors
from .embed import Embed
import asyncio
import requests


class Webhook:
    def __init__(self, weburl: str, name: str=None, avatar_url: str=None):
        if not weburl.startswith("https://discord.com/api/webhooks/"):
            raise Errors.WebhookURLError("This is not Discord Webhook URL! Please check your URL and change the URL to the correct URL!")
        response=requests.get(weburl).json()
        if avatar_url == None:
            self.avatar_url=response["avatar"]
        elif not avatar_url.startswith("https://"):
            raise Errors.URLError("This is not URL! Please check and change your URL!")
        else:
            self.avatar_url=avatar_url
        self.weburl=weburl
        if name == None:
            self.name=response["name"]
        else:
            self.name=name
        self.id=response["id"]
        self.mention=f"<@{self.id}>"
        self.token=response["token"]
        if response["application_id"] == None:
            self.application_id=0
        else:
            self.application_id=response["application_id"]
        self.channel_id=response["channel_id"]
        self.guild_id=response["guild_id"]
        self.json=response


    @property
    def url(self):
        return self.weburl


    def edit(self, channel_id: int, name: str, avatar_url: str=None):
        if not avatar_url.startswith("https!//") and avatar_url != None:
            raise Errors.URLError("This is not URL! Please check and change your URL!")
        _jdata={"name": name, "channel_id": channel_id, "avatar": avatar_url}
        return requests.patch(self.weburl, data=_jdata)


    def get_message(self, message_id: int):
        from .message import Message
        return Message(self, message_id)

    
    async def send_message(self, content: str=None, embeds: list[Embed]=[], delete_after: int=None):
        _embeds=[]
        for embed in embeds:
            _embeds.append(embed._to_dict)
        if content == None:
            _content=""
        else:
            _content=content
        _jdata={"content": _content, "embeds": _embeds}
        response=requests.post(self.weburl, data=_jdata)
        if delete_after == None:
            from .message import Message
            return Message(self, response.json()["id"])
        message_id=response.json()["id"]
        await asyncio.sleep(delete_after)
        return requests.delete(f"{self.weburl}/messages/{message_id}/")