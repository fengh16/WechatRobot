import itchat
import requests
from itchat.content import *
from bs4 import BeautifulSoup

notblockAll = True
blocklist = []
grouplist = []
friendlist = []
key = ""

def getSettings():
    global blocklist, grouplist, notblockAll, friendlist, key
    try:
        m = open("settings.txt", encoding="utf-8")
        soup = BeautifulSoup(m.read(), "html.parser")
        # 这里不能写成大写的！不能写成
        if soup.find_all("notblockall")[0].text == "1":
            notblockAll = True
        else:
            notblockAll = False
        block = soup.find_all("blocklist")
        group = soup.find_all("grouplist")
        friend = soup.find_all("friendlist")
        for i in range(block.__len__()):
            blocklist.append(block[i].text)
        for i in range(group.__len__()):
            grouplist.append(group[i].text)
        for i in range(friend.__len__()):
            friendlist.append(friend[i].text)
        key = soup.find_all("key")[0].text
        if key == "":
            key = input("请输入key！\n")
            saveNewSettings()
        m.close()
    except:
        print("无法正确读取设置，将刷新并重新导入设置！")
        setNewSettings()

def setNewSettings():
    global blocklist, grouplist, notblockAll, friendlist, key
    key = input("请输入从图灵机器人页面获取的key：\n")
    t = input('要默认回复所有好友的消息吗？是请输入Y或者y并回车，否则直接回车\n')
    if t == "y" or t == "Y":
        notblockAll = True
        while True:
            SetInput = input("请输入你·不想·让机器人回复的 好友 的·备注名·并回车，若输入完毕请直接按下回车！\n")
            if not SetInput == "":
                blocklist.append(SetInput)
                print("已经读入" + SetInput)
            else:
                print("输入完毕")
                break
    else:
        notblockAll = False
        while True:
            SetInput = input("请输入你·想·让机器人回复的 好友 的·备注名·并回车，若输入完毕请直接按下回车！\n")
            if not SetInput == "":
                friendlist.append(SetInput)
                print("已经读入" + SetInput)
            else:
                print("输入完毕")
                break
    while True:
        SetInput = input("请输入你·想·让机器人回复的 群名 并回车，若输入完毕请直接按下回车！\n")
        if not SetInput == "":
            grouplist.append(SetInput)
            print("已经读入" + SetInput)
        else:
            print("输入完毕")
            break
    saveNewSettings()

def saveNewSettings():
    global blocklist, grouplist, notblockAll, friendlist, key
    p = open("settings.txt", 'w', encoding="utf-8")
    p.write('''下面这一个notblockAll里面设置是否默认回复所有好友聊天
如果设置为1，则在blocklist里面的好友 不会 被机器人自动回复，friendlist不起作用
设置为0，则只有在friendlist里面的好友 会 被机器人自动回复，blocklist不起作用\n''')
    if notblockAll == True:
        p.write("<notblockAll>1</notblockAll>\n")
    else:
        p.write("<notblockAll>0</notblockAll>\n")
    p.write('''\n以下在notblockAll为1时起作用\n''')
    for block in blocklist:
        p.write("<blocklist>")
        p.write(block)
        p.write("</blocklist>\n")
    p.write('''\n以下在notblockAll为0时起作用\n''')
    for friend in friendlist:
        p.write("<friendlist>")
        p.write(friend)
        p.write("</friendlist>\n")
    p.write('''\n以下为要回复别人的@事件的群的设置\n''')
    for group in grouplist:
        p.write("<grouplist>")
        p.write(group)
        p.write("</grouplist>\n")
    p.write('''\n以下为从图灵机器人网上获取的key
进入http://www.tuling123.com/
注册、登陆之后进入个人中心（http://www.tuling123.com/member/robot/index.jhtml）
选择我的机器人--创建机器人
创建完成后点击首页，即可看到APIkey\n''')
    p.write("<key>" + key + "</key>")
    p.close()

# 收到文本信息（图片语音视频什么的得付费orz）
@itchat.msg_register([TEXT], isFriendChat=True, isGroupChat=True, isMpChat=False)
def reply(msg):
    global blocklist, grouplist, notblockAll, friendlist, key
    # print("Received")
    try:
        # 如果是自己发的就略过
        if msg['FromUserName'] != itchat.search_friends()['UserName']:
            # 找找好友名单，如果没有找到的话会让friend变为None
            friend = itchat.search_friends(userName=msg['FromUserName'])
            group = itchat.search_chatrooms(userName=msg['FromUserName'])
            # 不在黑名单里面并且是好友 或者 是群消息并且在群列表里面并且接收到了@自己
            if ((not friend is None) and (((not friend['RemarkName'] in blocklist) and notblockAll) or ((friend['RemarkName'] in friendlist) and not notblockAll))) or \
                    (friend is None and msg['IsAt'] and (not group is None) and (group['NickName'] in grouplist)):
                # 获取对方发过来的信息
                info = msg['Text'].encode('UTF-8')
                url = 'http://www.tuling123.com/openapi/api'
                data = {"key": key, "info": info}
                # 获取机器人的回复
                r = requests.post(url, data).text
                print("收到消息：" + msg['Text'] + "，获取的回复为：")
                print(r)
                # 如果正常返回
                if r[:22] == "{\"code\":100000,\"text\":":
                    print(r[23:r.__len__() - 2])
                    # 发回去
                    itchat.send(r[23:r.__len__() - 2], toUserName=msg['FromUserName'])
    except:
        print("Error!")

getSettings()
print("请扫描即将出现的二维码登陆微信：")
try:
    itchat.auto_login(hotReload=True)
except:
    itchat.auto_login(hotReload=False)
itchat.run()