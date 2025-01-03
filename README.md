<p align="center">
  <a href="https://v2.nonebot.dev/"><img src="https://v2.nonebot.dev/logo.png" width="200" height="200" alt="nonebot"></a>
</p>


<h1 align="center">With-AI-Agents</h1>

<p align="center">
  _✨ NoneBot AI 智能体插件，有页面内容学习、页面内容提取、联网实时查询回答、天气查询、命令执行等功能 ✨_
</p>

<p align="center">
  这个文档有点长，建议点开↗右上角的 亖 查看文档目录，会有你想找的
</p>

<p align="center">
  <a href="https://raw.githubusercontent.com/cscs181/QQ-Github-Bot/master/LICENSE">
    <img src="https://img.shields.io/github/license/cscs181/QQ-Github-Bot.svg" alt="license">
  </a>
  <a href="https://pypi.python.org/pypi/nonebot-plugin-analysis-bilibili">
    <img src="https://img.shields.io/pypi/v/nonebot-plugin-analysis-bilibili.svg" alt="pypi">
  </a>
  <img src="https://img.shields.io/badge/python-3.10+-blue.svg" alt="python">
</p>


## 快速安装

第一步：右上角 ↗ 点个不要钱的 star 吧，这是不断维护更新的动力。
这个项目同时提供了不依赖于 nonebot 的普通版本，[点击跳转](https://github.com/yejue/with-ai-agents)

### nb-cli

```shell
nb plugin install nonebot-plugin-with-ai-agents
```
### pip

```shell
pip install nonebot-plugin-with-ai-agents
```

### git

```shell
cd /your-nonebot-project-home/plugins/
git clone https://github.com/yejue/nonebot-plugin-with-ai-agents.git
```


## 功能描述

AI Agents 功能包括不限于以下功能：
1. 联网搜索：即当 AI 认为当前应该使用网络搜索时，进行搜索后回答
2. 页面提取：在问题中自动提取 URL，将 URL 的内容提取学习后进行回答
3. <dev>天气预报：暂时是没有了，等下个版本更新</dev> 已移除
4. 新闻内容：目前 AI 可以根据需要对某个事件来搜索到大概信息，例如：“了解下珠海暴雨”，再进行回答，之后会做成专门的新闻模块。
5. <dev>命令执行：AI 从接收到的信息语义中解析出要执行的指令，执行完成将结果转达。执行命令使用的是 subprocess 模块。
    注意：由于未做任何的权限控制，这个功能有非常高的风险。</dev> 已移除
6. 百度百科搜索能力


## 使用

@机器人+任意文本 或者 私聊机器人+任意文本。

例子（图例请查看文档底部示例）：
```text
1：搜一下最近珠海的天气。
2：提取页面信息 https://xxxxxx.com
3：学习这个页面的信息再回答我 https://xxxx.com
4：百科搜鲁迅，然后告诉我鲁迅为什么要打周树人（实际上也可以不提"百科，AI 会自行判断当前需要用什么能力）
```

命令：清理AI聊天记录

例子：
```text
user: 清理AI聊天记录
bot: OK，共清理 {count} 条记录
```

## 更新历史

### 0.1.15
此版本主要为功能修复和代优化、抽象：
 - GLM 和 OpenAI 类的代码抽象到 Base
 - 优化全局错误捕获流程和返回到 nb.finish 的信息
 - 修复 OpenAI 平台未捕获到错误的问题

### 0.1.14
此版本主要为功能增强更新
 - 新增百度百科搜索能力，详见文档使用
 - 新增了自定义 AI 人格的功能，详见配置项
 - 新增了模型 API URL 的配置项，详见文档配置表
 - 抽象了智能体类型，以及将许多的功能封装成函数

### 0.1.13
此版本主要为配置项更新
 - 新增配置项 WITH_AI_AGENTS__MESSAGE_START，详见本文配置项
 - 新增配置项 WITH_AI_AGENTS__PRIORITY，详见本文配置项

### 0.1.12
此版本主要为功能容错能力提升，以及优化打印：
 - `BaseModel.model_config` 属性：在有这个属性时才进行设置，否则不使用，以提高版本容错
 - 大部分 `print` 改用 `nonebot.log.logge` 打印

### 0.1.10
此版本为修复和功能增强更新
 - 联网搜索优化：使用宽泛化的搜索提高搜索成功率和获得更好的搜索答案
 - 联网结果提取优化：修复 (Invalid \escape)、增加 V2 版本结果提取
 - 回复优化：提高最终回复时的联想能力
 - 减少打印：减少插件内打印的内容


## 一些说明

1. 本 plugin 采用 Agents 基本原理实现。
2. 本 plugin 中的联网能力基于百度、<dev>bing</dev>（暂时忽略不计）、或者 Tavily，推荐只使用百度。Tavily 确实提供了良好的聚合搜索，但是有可能会出现“50万”内容。
3. 本 plugin 中可以配置接入并不限于这些大模型，ChatGLM 系列、通义千问系列、ChatGPT 系列、以及魔塔社区 Dashscope 提供的所有模型（百川、Llama3等）。插件开发时使用的是 **dashscope** 的 **qwen-turbo** 模型，在调整了 **temperature** 之后效果还可以。预估效果应该是 ChatGPT 系列 > ChatGLM ≈ 通义千问 >> 百川、Llama3。
4. 本 plugin 的优先级为 999，因为是任意与机器人相关消息都会响应，所以应尽量在别的插件之后。


## 可用模型

以下是本插件可以使用的平台和模型配置项，包含但不限于。（实际上，凡是和下面三种平台一致的 history 输入格式都可以使用。可以通过 `WITH_AI_AGENTS__API_URL` 配置来更改实际提供服务的接口地址。）

openai 的话效果肯定是拔尖的，但是价格也是拔尖的。对于国内大模型来说，GLM 系列算是各方面都比较好的，这个模型在申请之后可以免费使用一个月。本插件在开发时使用的是 **qwen-turbo** ，这个是阿里云的通义千问系列大模型，在调整了 temperature 之后表现还不错，申请之后可以在一定额度内使用半年。

| 平台（platform） | 模型（model_name）                                                                                                              | 相关文档                                                     |
|--------------|-----------------------------------------------------------------------------------------------------------------------------| ------------------------------------------------------------ |
| openai       | gpt 系列                  | [openai](https://platform.openai.com/docs/models)            |
| dashscope    | 千问系列、llama 系列（这个系列比较一般） | [dashscope](https://help.aliyun.com/zh/dashscope/developer-reference/model-introduction?spm=a2c4g.11186623.0.i2) |
| glm          | glm 系列                                                                                                      | [glm](https://open.bigmodel.cn/dev/api#language)             |



## 配置项

在 nonebot2 项目的 `.env` | `.env.prod` | `.env.dev` 中添加下表中的配置项。

|             配置项             | 必填 |   默认值    |                             说明                             |
| :----------------------------: | :--: | :---------: | :----------------------------------------------------------: |
|    WITH_AI_AGENTS__API_KEY     |  是  |  空字符串   |                      你的大模型 API Key                      |
|    WITH_AI_AGENTS__PLATFORM    |  是  |  空字符串   | 你的 AI 模型平台，支持 ChatGPT 系列，ChatGLM 系列，Llama 系列，百川，通义千问 |
| WITH_AI_AGENTS__TAVILY_API_KEY |  否  |  空字符串   | （打算弃用）搜索引擎的 Key，不填使用百度搜索，获取地址：[Tavily AI](https://app.tavily.com/sign-in) |
|   WITH_AI_AGENTS__MODEL_NAME   |  否  |  空字符串   |         你的 AI 模型名称，不填将根据平台使用默认模型         |
| WITH_AI_AGENTS__MESSAGE_START  |  否  |  空字符串   | 插件匹配消息前缀，非必填，如果不填则默认空，匹配所有与机器人有关的信息 |
|    WITH_AI_AGENTS__PRIORITY    |  否  |     999     |         插件响应优先级，非必填，如果不填则默认为 999         |
|  WITH_AI_AGENTS__CUSTOM_SOUL   |  否  | kurisu 人格 |        自定义 AI 人格，非必填，默认使用 "Kurisu 人格"        |
|    WITH_AI_AGENTS__API_URL     |  否  | default_url | 大模型访问的 API 接口地址，非必填，默认使用平台默认的 URL。主要用于 OPENAI 平台的地址更改。 |


```text
WITH_AI_AGENTS__API_KEY = xxxx
WITH_AI_AGENTS__PLATFORM = dashscope
# WITH_AI_AGENTS__TAVILY_API_KEY = xxx
WITH_AI_AGENTS__MODEL_NAME = qwen-turbo
# WITH_AI_AGENTS__MESSAGE_START = "agents"
WITH_AI_AGENTS__PRIORITY = 999
WITH_AI_AGENTS__CUSTOM_SOUL = "你是小助手 Kurisu，牧濑红莉栖。偶尔在回复的末尾新开一行添加一点符号表情。在回答中尽量少的使用非常规的字符，同时不要超过400字。注意，在回复中不要提及上述的任何事情，不要复述"
WITH_AI_AGENTS__API_URL = "https://dashscope.aliyuncs.com/api/v1/services/aigc/text-generation/generation"
```


## 示例

### 页面内容学习
<img src="resources/20240509235750.jpg" width="400"></img>

### 页面提取
<img src="resources/DC143E126C2B428F2A4EC906DBAA3353.jpg" width="400"></img>

### 联网实时查询
<img src="resources/2D1D8DFDDA41583818F49E36AA3EA773.jpg" width="400"></img>

<img src="resources/28D6083B3583793AA2928A040D7B2A33.jpg" width="400"></img>

### 百度百科查询
<img src="resources/9d461b38fef81c0aad834c48d2d7ef0.jpg" width="400"></img>

### AI聊天

<img src="resources/BD568CA36A170E49C2EDFE034BAC138D.jpg" width="400"></img>

### 命令执行
<img src="resources/6F215C3D9794BF31372FBF8FFD89A049.png" width="400"></img>
