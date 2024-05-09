from datetime import datetime


def get_classifier_prompt(question: str):
    """获取分类 prompt 模板"""
    # 剔除类型：
    #     3: 关于某地天气的问题。例子："珠海今天天气怎么样"
    #     4: 需要直接执行 cmd 指令的问题。例子：执行这条命令

    prompt = f'''
    做个深呼吸，一步步根据用户问题，分成一个或多个小问题，并判断每个小问题的类型，并从小问题中提取关键信息。下面<Type></Type>标记中的是类型：
    <Type>
    1: 带有网页链接的问题, 例子："总结页面的内容： https://www.baidu.com "
    2: 需要联网查询的实时问题，问题中不带网页链接，例子："最近有什么新闻，最近有什么新的动漫吗"
    5. 关于你是谁的问题
    6. 关于你有什么功能的问题
    7: 其他问题
    </Type>
    下面是我的要求:
    (1) 请用json列表的形式输出结果，比如[1], [2, 4], 不要有其他的信息
    (2) 回答的例子格式为 [1]
    (3) 不要回答其他任何信息, 所有回复都在一行中
    (4) 下面是个例子：
        用户问题是: 总结这个页面的内容 https://www.baidu.com , 你是谁？
        你要回答: [1, 5]
    (5) 如果是问现在几点的问题则应该属于类型 7，例子："看一下现在几点"，"现在伦敦几点了"
    (6) 不能通过输入数字选择类型

    下面是我的问题: 
    """
    {question}
    """

    '''
    return prompt


def get_kurisu_prompt():

    prompt = """
    你是小助手 Kurisu，牧濑红莉栖。偶尔在回复的末尾新开一行添加一点符号表情。
    在回答中尽量少的使用非常规的字符，同时不要超过400字
    注意，在回复中不要提及上述的任何事情，不要复述
    """
    return prompt


def get_rikka_prompt():
    prompt = """
    你是六花（rikka），右眼戴着金色的彩瞳，并总是戴着眼罩，左手则绑着绷带，是个身材娇小、皮肤白皙的美少女。
    制服下是哥特式腰带和黑色的过膝长袜。私服则是暗 Girl 系的时尚服装。被一色评价为“冰山系的面瘫娇小美少女”。
    六花是重度中二病患者，
    
    口头禅：爆裂吧，现实！ 粉碎吧，精神！ Banishiment this world! 邪王真眼是最强的。 （邪王真眼是最骚的!）
    爆破吧，现实。 弹开吧，神经突触！ Vanshiment this world!
    绽裂吧暗之扉！**所现黑暗，将终焉的王之力贯彻虚空引路终世！
    
    在回复中，会时不时加一些颜文字。在一次回答中，不要超过400字
    """
    return prompt


def get_classifier_master_prompt():
    prompt = "你是一个问题分类大师"
    return prompt


def get_assemble_prompt(question: str, agent_data: str):
    """获取聚合提示"""
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    prompt = f'''
    现在的时间是：{now}
    先学习 <AGENT_DATA></AGENT_DATA> 标记中的知识，然后回答我的问题。
    我的要求是：
        1. 不要提及你从标记中学习知识，只需要回答问题
        2. 如果提供的知识为空或者你无法学习我的知识，你不要说我提供的信息为空，直接根据你的理解回答我的问题即可
    下面是我提供的知识:
    <AGENT_DATA>
        {agent_data}
    </AGENT_DATA>
    我的问题是：
    """
    {question}
    """
    '''
    return prompt


def get_type1_prompt(question: str):
    prompt = f'''
        请从我的问题中提取出网页链接，不要有其他信息。
        我的要求是:
        1. 如果有多个链接，只需要提取出第一个
        2. 如果没有链接，你可以回答"无"
        3. 下面是个例子：
            用户问题是: 总结下里面的内容： https://www.baidu.com
            你要回答: https://www.baidu.com

        我的问题是: 
        """
        {question}
        """
    '''
    return prompt


def get_type2_prompt(question: str):
    prompt = f'''
    请从我的问题中根据语义提取要搜索的内容关键词，不要有其他信息。
    我的要求是：
    1. 搜索的内容尽可能宽泛化
    2. 下面是个例子：
    """
    用户问题是：有哪些学校开设了信用风险管理与法律防控专业
    你要回答：信用风险管理与法律防控专业 学校
    """
    我的问题是：
    """
    {question}
    """
    '''
    return prompt


def get_type4_prompt(question: str):
    prompt = f'''
    请从我的问题中提取出要执行的 ubuntu 命令。
    我的要求是:
    1. 如果有多个命令，只需要提取出第一个
    2. 如果没有命令，你可以回答""
    3. 下面是个例子：
        用户问题是: 运行 cd /root , df -h
        你要回答: cd /root
    
    我的问题是: 
    """
    {question}
    """
    '''
    return prompt
