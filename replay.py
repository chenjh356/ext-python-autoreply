import websocket
import requests
import json
import asyncio
import websockets
import config

try:
    import thread
except ImportError:
    import _thread as thread
import time

qun = {}


async def get_qun(uri):
    async with websockets.connect(uri) as temp:
        bookjson = {
            "method": "getUser",
            "pid": 0
        }
        await temp.send(json.dumps(bookjson))
        res = await temp.recv()
        # print(res)
        for i in json.loads(res)['data']:
            if '@chatroom' in i['wxid']:
                qun[i['wxid']] = i['nickName']
        # print(qun)


def on_message(ws, message):

    # print(message)
    a = json.loads(message)
    if a['method'] == 'newmsg':
        # print(a['data'])
        # 处理群
        data = a['data']
        if '@chatroom' in data['fromid']:
            if qun.get(data['fromid'], 'none') in config.reply_qun:
                if '在群聊中@了你' in data['des']:
                    fromid = data['fromid']
                    memid = data['memid']
                    memname = data['memname']
                    nick = qun.get(fromid, '未命名群')
                    print(nick, ':', data['msg'])
                    msg = {
                        "method": "sendText",
                        "wxid": fromid,
                        "msg": "@%s 收到" % memname,
                        "atid": memid,
                        "pid": 0
                    }
                    ws.send(json.dumps(msg))
        else:
            if data['nickName'] not in ['Ealeo', '文件传输助手'] and 'gh' not in data['fromid']:
                fromid = data['fromid']
                from replay_time import re_time
                num = re_time.get(fromid, 0)
                if num < config.reply_max:
                    if fromid != 'wxid_ki1umk2cj36t21':
                        msg = {
                            "method": "sendText",
                            "wxid": fromid,
                            "msg": config.reply_text,
                            "atid": "",
                            "pid": 0
                        }
                        ws.send(json.dumps(msg))
                        num += 1
                        re_time[fromid] = num
                        with open('replay_time.py', 'w') as f:
                            f.write('re_time = '+str(re_time))



def on_error(ws, error):
    print(error)


def on_close(ws):
    print("### closed ###")


def on_open(ws):
    def run(*args):
        bookjson = {
            "method": "getUser",
            "pid": 0
        }
        ws.send(json.dumps(bookjson))





if __name__ == "__main__":
    websocket.enableTrace(False)
    with open('replay_time.py', 'w') as f:
        f.write('re_time = {}')
    key = requests.get('http://127.0.0.1:8203/ext/www/key.ini').json()['key']
    uri = "ws://127.0.0.1:8202/wx?name=www&key=" + key
    loop = asyncio.get_event_loop()
    loop.run_until_complete(get_qun(uri))
    loop.close()
    ws = websocket.WebSocketApp("ws://127.0.0.1:8202/wx?name=www&key=" + key,
                                on_message=on_message,
                                on_error=on_error,
                                on_close=on_close)

    ws.run_forever()


