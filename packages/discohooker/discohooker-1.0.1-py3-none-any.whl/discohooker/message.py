from .errors import Errors
from .embed import Embed
from .webhook import Webhook
import requests


class Message:
    def __init__(self, webhook: Webhook, message_id: int):
        self.webhook=webhook
        response=requests.get(f"{self.webhook.weburl}/messages/{message_id}").json()
        if response["author"]["id"] == self.webhook.id:
            self.is_sent_by_webhook=True
        else:
            self.is_sent_by_webhook=False
        self.id=response["id"]
        self.content=response["content"]
        self.is_pinned=response["pinned"]
        self.embeds=[]
        for embed in response["embeds"]:
            _embed=Embed()
            _embed._to_dict=embed
            self.embeds.appead(_embed)
        self.timestamp=response["timestamp"]
        self.mentions_id=[]
        for user in response["mentions"]:
            self.memtions_id.appead(user["id"])
        self.channel_id=response["channel_id"]

    
    async def edit(self, content: str=None, embeds: list[Embed]=[]):
        if self.is_sent_by_webhook == False:
            raise Errors.MessageError("This message is not sent by this Webhook!")
        message_id=self.id
        _embeds=[]
        for embed in embeds:
            _embeds.append(embed._to_dict)
        if content == None:
            _content=""
        else:
            _content=content
        _jdata={"content": _content, "embeds": _embeds}
        response=requests.patch(f"{self.weburl}/messages/{message_id}", data=_jdata)
        if response.status_code == 204:
            raise Errors.APIError("No message's content and embeds have been given by you!")
        else:
            return response


    async def delete(self):
        if self.is_sent_by_webhook == False:
            raise Errors.MessageErro("This message is not sent by this Webhook!")
        message_id=self.id
        response=requests.delete(f"{self.weburl}/messages/{message_id}")
        if response.status_code != 204:
            raise Errors.MessageNotFound("This message was not sent by this Webhook! Please make sure your message id is correct!")
        else:
            return response