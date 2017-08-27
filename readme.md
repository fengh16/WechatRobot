## 用法说明：将exe文件与settings.txt文件放到同一目录下，运行exe即可对所有好友发过来的信息进行自动回复。
## 给出一个可用的key： 30e5b3fa112e408a91bec1b3ff78c3ca
### 如果需要修改配置，可以删除settings.txt后运行exe文件，根据提示操作。或者按照如下说明修改，可参照“几个示例settings.txt”：
### 如果需要在某个群中接收消息并且回复，请将<grouplist>群名1</grouplist>部分进行修改，一个<grouplist>XXX</grouplist>中写一个群名
### 如果需要屏蔽某些人，请修改<blocklist>被屏蔽的好友备注1</blocklist>，将需要屏蔽的好友备注写在其中
### 如果只对某些好友进行回复，请修改<notblockAll>1</notblockAll>为<notblockAll>0</notblockAll>，并且将需要回复的好友名写在<friendlist>要回复的好友备注1</friendlist>中