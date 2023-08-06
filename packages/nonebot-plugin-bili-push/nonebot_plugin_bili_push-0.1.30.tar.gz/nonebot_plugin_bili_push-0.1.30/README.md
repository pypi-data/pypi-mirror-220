<div align="center">
  <p><img src="http://cdn.kanon.ink/api/image?key=899178&imageid=image-20230618-220942-65085441" width="150" alt="NoneBotPluginText"></p>
</div>

<div align="center">

# nonebot-plugin-bili-push
 B订阅推送插件 
</div>

## 示例

![输入图片描述](README_md_files/9cf89890-0952-11ee-8733-25d9c7397331.jpeg?v=1&type=image)
![输入图片描述](README_md_files/7fd7ee50-0952-11ee-8733-25d9c7397331.jpeg?v=1&type=image)


## 安装
（以下方法三选一）

一.命令行安装：（貌似安装不了，可以试一下先） 

    nb plugin install nonebot-plugin-bili-push
    
二.pip安装：

1.执行此命令

    pip install nonebot-plugin-bili-push
    
2.修改pyproject.toml使其可以加载插件

    plugins = [”nonebot-plugin-bili-push“]
    
 三.使用插件文件安装：（不推荐） 
 
 1.下载插件文件，放到plugins文件夹。

2.修改pyproject.toml使其可以加载插件

 
## 配置
在 nonebot2 项目的`.env`文件中选填配置

1.配置管理员账户，只有管理员才能添加订阅

    SUPERUSERS=["12345678"] # 配置 NoneBot 超级用户
2.插件数据存放位置，默认为 “./”。

    bilipush_basepath="./"

3.推送样式
> 动态的推送样式
可配置选项：[绘图][标题][链接][内容][图片]

    bilipush_push_style="[绘图][标题][链接]"


4.刷新间隔：
> 每次刷新间隔多少分钟，默认为12分钟。

    bilipush_waittime=12

5.发送间隔：
>  每次发送完成后等待的时间，单位秒，默认10-30秒。
> 时间为设置的时间再加上随机延迟1-20秒

    bilipush_sleeptime=10

6.最大发送数量

> 限制单次发送数量，防止一次性发送太多图导致风控。
> 默认5条

	bilipush_maximum_send=5

    
其他配置项

> 只响应一个bot
> 一个群内有多个bot，可以只让1个bot推送消息。
> 默认为关闭该功能，既所有bot都会响应
> （正在考虑是否改为默认开启，如不需要请关闭该功能）

    bilipush_botswift=False
    
> 是否使用api来获取emoji图像，默认使用。

    bilipush_emojiapi=True

## To-Do
🔵接下来：
 - [ ] 将请求api改为异步
 - [ ] 完善动态类型（目前仅支持文字、图文、视频、转发、文章）
 - [ ] 字体排版优化（字符位置以及）
 - [ ] 头像过大
 - [ ] 直播无url
 - [ ] 动态卡片数字样式
 - [ ] 动态卡片非粉丝的位置
 - [ ] 添加话题标签
 - [ ] 添加动态底部相关的内容绘制（游戏、动漫）
 - [ ] 动态背景图？闲的时候可以整一下
 - [ ] 升级数据库"
 - [ ] 动态获取不到名字，导致关注报错
 - [ ] 版面优化
 - [ ] 优化print（）
 - [ ] 代码整理
 - [ ] 增加可配置内容（或尝试创建配置文件的方式
 - [ ] 对话式配置（如果把配置文件独立出来就考虑这种方式
 - [ ] ~~自动bug报告（暂无计划~~
 
 🟢已完成：
 - [x] 配置推送样式
 - [x] 添加各种装饰（头像框、装扮等）
 - [x] 修复文件下载出错导致文件加载报错
 - [x] 无动态时自动跳过
 - [x] 关注时获取信息检查，防止输错uid
 - [x] 设置默认字体。在禁用api时候使用默认字体
 - [x] 单nb对接多q的兼容
 - [x] 增加上下播推送
 - [x] 添加本地计算emoji模式
 
## 更新日志
### 0.1.30
新增配置推送样式
### 0.1.28
修复直播封面获取错误
新增配置推送样式
### 0.1.27
添加头像框和动态卡片
### 0.1.26.1
修复#6图片长度出错
修复#5关注的时候报错
新增动态类型：文章
### 0.1.24
关注时返回up信息  
跳过无动态的up主
### 0.1.23
增加一个nb对接多个gocq的连接方式  

## 参考插件
Mirai动态绘制插件 [BilibiliDynamic MiraiPlugin](https://github.com/Colter23/bilibili-dynamic-mirai-plugin)

## 交流
-   交流群[鸽子窝里有鸽子（291788927）](https://qm.qq.com/cgi-bin/qm/qr?k=QhOk7Z2jaXBOnAFfRafEy9g5WoiETQhy&jump_from=webapi&authKey=fCvx/auG+QynlI8bcFNs4Csr2soR8UjzuwLqrDN9F8LDwJrwePKoe89psqpozg/m)
-   有疑问或者建议都可以进群唠嗑唠嗑。
