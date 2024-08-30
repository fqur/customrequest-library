from requestlibrary import *

url = "https://discord.com/api/webhooks/1278943876593483817/PflFMmBz56LLHmj61SsUwOQ8Ua4kIL_V-QFeUpkMgT00nV2SvjRar_NciCfX-5XWAgwO"
payload = {
    "content": "hi",
    "username": "hi"
}

response = post_request(url, data=payload, random_ua=True)
