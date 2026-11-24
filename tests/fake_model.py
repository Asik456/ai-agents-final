from langchain_core.messages import AIMessage


class FakeModel:
    def __init__(self, replies):
        self.replies = list(replies)
        self.calls = 0

    def bind_tools(self, tools):
        self.tools = tools
        return self

    def invoke(self, messages):
        self.calls += 1
        reply = self.replies.pop(0)
        if isinstance(reply, Exception):
            raise reply
        if isinstance(reply, list):
            calls = [{"name": name, "args": args, "id": f"call-{self.calls}-{i}"} for i, (name, args) in enumerate(reply)]
            return AIMessage("", tool_calls=calls)
        return AIMessage(reply)
