# Quickly Start
**Step 1:**
> Install Discohooker in Shell.
> 
> ```pip install discohooker```


**Step 2:**
> Get your Webhook link in [Discord](https://discord.com/channels/@me).


**Step 3:**
> Import Discohooker.
>
> ```py
> import discohooker
> ```


**Step 4:**
> Setup Webhook.
>
> ```py
> webhook=discohooker.Webhook(
>     weburl="YOUR DISCORD WEBHOOK URL",
>     name="DISCORD WEBHOOK NAME(IF YOU HAVE SET IN DISCORD ALREADY, YOU MUST NOT ENTER.)",
>     avatar_url="DISCORD WEBHOOK AVATAR URL(IF YOU HAVE SET IN DISCORD ALREADY, YOU MUST NOT ENTER.)"
> )
>
> webhook.send_message("I am made by Discohooker!")
> ```


**Step 5:**
> Done!