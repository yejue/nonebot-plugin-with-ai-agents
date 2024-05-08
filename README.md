<p align="center">
  <a href="https://v2.nonebot.dev/"><img src="https://v2.nonebot.dev/logo.png" width="200" height="200" alt="nonebot"></a>
</p>


<h1 align="center">With-AI-Agents</h1>

_✨ NoneBot AI 助理插件，有页面内容学习、页面内容提取、联网实时查询回答、天气查询、命令执行等功能 ✨_

<p align="center">
  <a href="https://raw.githubusercontent.com/cscs181/QQ-Github-Bot/master/LICENSE">
    <img src="https://img.shields.io/github/license/cscs181/QQ-Github-Bot.svg" alt="license">
  </a>
  <a href="https://pypi.python.org/pypi/nonebot-plugin-analysis-bilibili">
    <img src="https://img.shields.io/pypi/v/nonebot-plugin-analysis-bilibili.svg" alt="pypi">
  </a>
  <img src="https://img.shields.io/badge/python-3.8+-blue.svg" alt="python">
</p>


## 快速安装

第一步：右上角 ↗ 点个不要钱的 star 吧，这是不断维护更新的动力。

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
3. 天气预报：暂时是没有了，等下个版本更新
4. 新闻内容：目前 AI 可以根据需要对某个事件来搜索到大概信息，例如：”了解下珠海暴雨“，再进行回答，之后会做成专门的新闻模块。
5. 命令执行：AI 从接收到的信息语义中解析出要执行的指令，执行完成将结果转达。执行命令使用的是 subprocess 模块。
  注意：由于未做任何的权限控制，这个功能有非常高的风险。



## TODOs
”！！“ 为近期要做的事情
”~~“ 为可能会鸽的更新，慢慢来

 - [ ] ！！命令执行安全问题，方案：对特定 ID 可用，并提供可关停配置。
 - [ ] 新闻查询增强，方案：从各类新闻网获取聚合数据。
 - [ ] Prompt 调整，方案：优化和精简 Prompt。
 - [ ] AI 聊天历史对群聊和私聊做区分（考虑中，如果加的话可能会使用数据库）。
 - [ ] ~~天气预报，没有很大兴趣。
 - [ ] ~~知识库，采用 Embeddings + PGVector 完成数据向量化和存储搜索。对于一个插件来说，体量可能过大。



## 一些说明

1. 本 plugin 采用 Agents 基本原理实现。
2. 本 plugin 中的联网能力基于百度、bing（暂时忽略不计）、或者 Tavily，推荐只使用百度。Tavily 确实提供了良好的聚合搜索，但是有可能会出现“50万”内容。
3. 本 plugin 中可以配置接入并不限于这些大模型，ChatGLM 系列、通义千问系列、ChatGPT 系列、以及魔塔社区 Dashscope 提供的所有模型（百川、Llama3等）。插件开发时使用的是 **dashscope** 的 **qwen-turbo** 模型，在调整了 **temperature** 之后效果还可以。预估效果应该是 ChatGPT 系列 > ChatGLM ≈ 通义千问 >> 百川、Llama3。
4. 本 plugin 的优先级为 999，因为用的是全部文本匹配，会响应任意文本，所以应尽量在别的插件之后
5. 推荐 COMMAND_START 设置为空



## 可用模型

以下是本插件可以使用的平台和模型配置项，包含但不限于。

openai 的话效果肯定是拔尖的，但是价格也是拔尖的。对于国内大模型来说，GLM 系列算是各方面都比较好的，这个模型在申请之后可以免费使用一个月。本插件在开发时使用的是 **qwen-turbo** ，这个是阿里云的通义千问系列大模型，在调整了 temperature 之后表现还不错，申请之后可以在一定额度内使用半年。

| 平台（platform） | 模型（model_name）                                                                                                              | 相关文档                                                     |
|--------------|-----------------------------------------------------------------------------------------------------------------------------| ------------------------------------------------------------ |
| openai       | gpt-3.5-turbo-0125（推荐，毕竟便宜一点）、gpt-3.5-turbo、gpt-3.5-turbo-16k、gpt-4-turbo、gpt-4-turbo-2024-04-09、gpt-4-32k                  | [openai](https://platform.openai.com/docs/models)            |
| dashscope    | qwen-turbo（推荐，开发时使用）、qwen-plus、qwen-max-longcontext、llama3-8b-instruct（不尽人意）、llama3-70b-instruct（不尽人意）、baichuan-7b-v1（不尽人意） | [dashscope](https://help.aliyun.com/zh/dashscope/developer-reference/model-introduction?spm=a2c4g.11186623.0.i2) |
| glm          | glm-3-turbo（推荐）、glm-4                                                                                                       | [glm](https://open.bigmodel.cn/dev/api#language)             |



## 配置项

在 nonebot2 项目的 `.env` | `.env.prod` | `.env.dev` 中添加下表中的配置项。

|      配置项       | 必填 |  默认值  |                             说明                             |
| :---------------: | :--: | :------: | :----------------------------------------------------------: |
|   WITH_AI_AGENTS__API_KEY    |  是  | 空字符串 |                         你的大模型 API Key                          |
| WITH_AI_AGENTS_PLATFORM |  是  | 空字符串 | 你的 AI 模型平台，支持 ChatGPT 系列，ChatGLM 系列，Llama 系列，百川，通义千问 |
| WITH_AI_AGENTS__TAVILY_API_KEY |  否  | 空字符串 | （打算弃用）搜索引擎的 Key，不填使用百度搜索，获取地址：[Tavily AI](https://app.tavily.com/sign-in) |
|  WITH_AI_AGENTS__MODEL_NAME   |  否  | 空字符串 |        你的 AI 模型名称，不填将根据平台使用默认模型        |

## 使用

@机器人+任意文本或者私聊机器人+任意文本。

## 示例

### 页面内容学习
<img src="resources/IMG_5055.PNG" width="400"></img>
### 页面提取
<img src="resources/DC143E126C2B428F2A4EC906DBAA3353.jpg" width="400"></img>

### 联网实时查询
<img src="resources/2D1D8DFDDA41583818F49E36AA3EA773.jpg" width="400"></img>


<img src="resources/28D6083B3583793AA2928A040D7B2A33.jpg" width="400"></img>



### AI聊天

<img src="resources/BD568CA36A170E49C2EDFE034BAC138D.jpg" width="400"></img>

### 命令执行

### <img src="resources/6F215C3D9794BF31372FBF8FFD89A049.png" width="400"></img>
