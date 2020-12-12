import sys
import requests as r
import json
import telepot

tele_enable=False
sc_enable=False
sign='https://n.cg.163.com/api/v2/sign-today'
current='https://n.cg.163.com/api/v2/client-settings/@current'

cookies=sys.argv[1].split('#')
teleid="" #sys.argv[2]
teletoken="" #sys.argv[3]
sckey=sys.argv[4]
if cookies=="":
    print('[网易云游戏自动签到]未设置cookie，正在退出……')
    sys.exit()
if teleid!="" and teletoken!="":
    tele_enable=True
    bot=telepot.Bot(teletoken)
if sckey!="":
    sc_enable=True

class Error(Exception):
    pass

def signin(url,cookie):
    header={
        'Accept': 'application/json, text/plain, */*',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7,ja-JP;q=0.6,ja;q=0.5',
        'Authorization': str(cookie),
        'Connection': 'keep-alive',
        'Content-Length': '0',
        'Host': 'n.cg.163.com',
        'Origin': 'https://cg.163.com',
        'Referer': 'https://cg.163.com/',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-site',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36',
        'X-Platform': '0'
    }

    result=r.post(url=url,headers=header)
    return result

def getme(url,cookie):
    header={
        'Host': 'n.cg.163.com',
        'Connection': 'keep-alive',
        'Accept': 'application/json, text/plain, */*',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36',
        'X-Platform': '0',
        'Authorization': str(cookie),
        'Origin': 'https://cg.163.com',
        'Sec-Fetch-Site': 'same-site',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Dest': 'empty',
        'Referer': 'https://cg.163.com/',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7,ja-JP;q=0.6,ja;q=0.5'  
    }
    result=r.get(url=url,headers=header)
    return result

def send(id,message):
    if tele_enable:
        bot.sendMessage(id, message, parse_mode=None, disable_web_page_preview=None, disable_notification=None, reply_to_message_id=None, reply_markup=None)

def scsend(SCKEY,message):
    sc_url='http://sc.ftqq.com/{}.send?text=网易云游戏自动签到脚本&desp={}'.format(SCKEY,message)
    if sc_enable:
        r.get(url=sc_url)

if __name__ == "__main__":
    success=[]
    failure=[]
    msg=[]
    print(len(cookies))
    for i in cookies:
        print(i)
        cookie=i
        autherror=False
        signerror=False
        try:
            me=getme(current,cookie)
        except:
            message='第{}个账号验证失败！请检查Cookie是否过期！或者附上报错信息到 https://github.com/GamerNoTitle/wyycg-autosignin/issues 发起issue'.format(cookies.index(i)+1)
            failure.append(cookie)
            msg.append(message)
            autherror=True

        if(me.status_code!=200 and autherror!=True):
            message='第{}个账号验证失败！请检查Cookie是否过期！或者附上报错信息到 https://github.com/GamerNoTitle/wyycg-autosignin/issues 发起issue'.format(cookies.index(i)+1)
            failure.append(cookie)
            msg.append(message)

        try:
            sign=signin(sign,cookie)
        except:
            message='第{}个账号签到失败，回显状态码为{}\n具体错误信息如下：\n{}'.format(cookies.index(i)+1,sign.status_code,sign.text)
            failure.append(cookie)
            msg.append(message)
            signerror=True

        if(sign.status_code==200):
            message='第{}个账号签到成功！'.format(cookies.index(i)+1)
            success.append(cookie)
            msg.append(message)
        elif(signerror!=True):
            message='第{}个账号签到失败，回显状态码为{}\n具体错误信息如下：\n{}'.format(cookies.index(i)+1,sign.status_code,sign.text)
            failure.append(cookie)
            msg.append(message)
    outputmsg=str(msg).replace("[",'').replace(']','').replace(',','<br>').replace('\'','')
    infomsg='''
    感谢使用来自<a herf='https://bili33.top'>GamerNoTitle</a>的<a herf='https://github.com/GamerNoTitle/wyycg-autocheckin'>网易云游戏自动签到脚本</a>！<br>
    今日签到结果如下：<br>
    成功数量：{0}/{2}<br>
    失败数量：{1}/{2}<br>
    具体情况如下：<br>
    {3}
    '''.format(len(success),len(failure),len(cookies),outputmsg)
    scsend(sckey,infomsg)
    send(teleid,infomsg)
    print(infomsg)
    if(len(msg)!=0):
        raise Error