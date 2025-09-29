# Noita-DGLab
一种基于Noita中受伤数值的DGLab游玩方式, 有点邪门的搭配, 不知道受众在哪, 但既然已经写了几行代码就发出来了.

手机APP扫码链接, 触发方式很简单(~~不知道更好的~~), 都在配置文件`config.hjson`中, 简单说就是受到伤害越高, 通道强度越高, 时间越长, 但是都有上限:

```c
{
    // 本机内网ip地址
    ip: 192.168.1.5
    // ip: 10.0.0.2
    // 由于太低了没感觉, 所以需要设定一个起步强度百分比
    // 例如0.82表示82%, 也就是受到伤害时通道强度从上限的82%开始增加到100%
    percent_minimum: 0.84
    // 同理, 输出时长的最小值和最大值(秒)
    time_minimum: 0.5
    time_maximum: 3.0
    // 受到的伤害达到多少时, 输出强度百分比和输出时长达到最大值
    damage_maximum: 30
    // 受到的伤害 < damage_maximum时: 
    //      输出的强度百分比 = percent_minimum + (1 - percent_minimum) * (受到的伤害 / damage_maximum)
    //      输出时长 = time_minimum + (time_maximum - time_minimum) * (受到的伤害 / damage_maximum)
    // 受到的伤害 >= damage_maximum时:
    //      输出的强度百分比 = 1.0
    //      输出时长 = time_maximum
}
```

稍微长线一些或者刷完血着火都是相当刺激x

# 安装方式及原理

借用了cheat-gui模组的[github版本](https://github.com/probable-basilisk/cheatgui), 也就是不安全模组的版本. 这个版本支持游戏外部websocket连接执行lua命令, 于是可以获取当前生命值. **这也意味着要打开Noita模组列表页面的红色不安全模组开关并且要手动安装.**

借助下AI神力和一些调试就弄出了一个python脚本用来连接手机APP同时连接cheatgui的websocket.

具体安装过程如下:

- 首先安装cheatgui模组. 下载或克隆整个项目, 移动cheatgui文件夹到Noita安装目录下mods文件夹中, 如`C:\Program Files (x86)\Steam\steamapps\common\Noita\mods`
- 打开Noita模组列表页面勾选`Cheatgui DG-Lab version`以及右边不安全模组选项, 然后进入一局游戏.
- DGLab文件夹可以放到任意地方, 文件夹下还有一个config.hjson可以调一些设置, 重启生效, 注意**将ip设置为本机内网IP地址**, 可以打开终端输入ipconifg查看对应网卡的ip
- 按照requirement.txt安装依赖运行python脚本**或者**直接运行打包好的exe文件都可以
- ~~找我上门安装狼~~
- 手机扫码连接, APP设置强度上限.

还可以启动Noita Proxy联机, 点开共享血量, 然后在语音里质问别人在搞什么😡


真的有人会玩这个吗, 我有点不信
