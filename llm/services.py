from .mem_stores import chat_history


class ChatService:
    """聊天控制类"""

    @staticmethod
    def add_message_to_history(text, role="user"):
        new_message = {"role": role, "content": text}
        chat_history.append(new_message)

    @staticmethod
    def get_history_list():
        return chat_history
