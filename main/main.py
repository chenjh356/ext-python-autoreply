import sys
import time
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
myself = []


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
            if 'chatroom' in i['wxid']:
                qun[i['wxid']] = i['nickName']
        # print(qun)

async def get_myself(uri):
    async with websockets.connect(uri) as temp:
        my = {
            "method": "getInfo",
            "pid": 0
        }
        await temp.send(json.dumps(my))
        res = await temp.recv()
        # print(res)
        myid = json.loads(res)['myid']
        myself.append(myid)


def on_message(ws, message):

    # print(message)
    a = json.loads(message)
    if a['method'] == 'newmsg':
        print(a['data'])
        # 处理群
        data = a['data']
        if 'chatroom' in data['fromid']:

            if qun.get(data['fromid'], 'none') in config.reply_qun:

                if '在群聊中@了你' in data['des']:
                    fromid = data['fromid']
                    memid = data['memid']
                    memname = data['memname']
                    # nick = qun.get(fromid, '未命名群')
                    # time.sleep(1)
                    # with open('qun.txt', 'w') as f:
                    #     f.write(nick + ':' + data['msg'])
                    #
                    msg = {
                        "method": "sendText",
                        "wxid": fromid,
                        "msg": "@%s 收到" % memname,
                        "atid": memid,
                        "pid": 0
                    }
                    with open('data.txt', 'w') as f:
                        f.write(str(msg))

                    ws.send(json.dumps(msg))
        elif 'wxid_' in data['fromid']:
            if data['nickName'] not in ['悟道', '文件传输助手'] and 'gh' not in data['fromid'] and 'weixin' not in data['fromid']:
                fromid = data['fromid']
                from replay_time import re_time
                num = re_time.get(fromid, 0)
                if num < config.reply_max:
                    if fromid not in myself:
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
    data = sys.argv
    name = data[data.index('--name') + 1]
    key = data[data.index('--key') + 1]
    uri = "ws://127.0.0.1:8202/wx?name=" + name + "&key=" + key
    with open('uri.txt', 'w') as f:
        f.write(uri)
    loop = asyncio.get_event_loop()
    loop.run_until_complete(get_qun(uri))
    loop.run_until_complete(get_myself(uri))
    loop.close()
    ws = websocket.WebSocketApp(uri,
                                on_message=on_message,
                                on_error=on_error,
                                on_close=on_close)

    ws.run_forever()
