import requests
import json


def auto_send(message, *args, **kwargs):
    if kwargs.get("platform", None):
        platform = kwargs["platform"]
    elif len(args) > 0:
        args = list(args)
        platform = args.pop(0).lower()
    else:
        raise ValueError(f"API Platform Not Found.")
    if platform in globals() and callable(globals()[platform]):
        return globals()[platform](message, *args, **kwargs)
    raise ValueError(f"Not Support API Platform {platform}")


def dingding(text, key: str = "", **kwargs):
    url = 'https://oapi.dingtalk.com/robot/send?access_token=' + key
    if ':' not in text and "." not in text and "," not in text and "。" not in text:
        text += "."
    data = {
        "msgtype": "text",
        "text": {
            "content": text
        },
    }
    headers = {"Content-Type": "application/json ;charset=utf-8 "}
    html = requests.post(url, data=json.dumps(data), headers=headers)
    return html.ok


def wechat(text, key: str = "", **kwargs):
    url = 'https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=' + key
    data = {
        "msgtype": "text",
        "text": {
            "content": text
        },
    }
    headers = {"Content-Type": "application/json ;charset=utf-8 "}
    html = requests.post(url, data=json.dumps(data), headers=headers)
    return html.ok


def qq(text, key: str = ""):
    url = "https://qmsg.zendee.cn/send/" + key
    data = {'msg': text}
    html = requests.post(url, data=data)
    return html.ok


def mi(text, key: str = "", title="bot", **kwargs):
    url = "https://tdtt.top/send"
    data = {"title": title, "content": text, "alias": key}
    response = requests.post(url, data=data)
    return response.ok


def telegram(text: str, token: str, chat: str, host="api.telegram.org", mono=False, **kwargs):
    url = f"https://{host}/bot{token}/sendMessage"
    # 设置字体为等宽字体
    if mono and "parse_mode" not in kwargs:
        text = f"<pre>{text}</pre>"
        kwargs["parse_mode"] = "HTML"

    data = {
        "chat_id": chat,
        "text": text,
        **kwargs,
    }
    return requests.get(url, data=data).json()


def pushplus(message, token, title="default", template="html", **kwargs):
    url = f'http://www.pushplus.plus/send?token={token}&title={title}&content={message}&template={template}'
    resq = requests.get(url=url)
    return resq.text
