import os

from revChatGPT.V3 import Chatbot

from .lang import language_dict 


class GrammarHelper:
    def __init__(self, api_key=None) -> None:
        key = "OPEN_AI_API_KEY"
        if key not in os.environ:
            raise Exception('API KEY should be provide as argument or from your env')
        api_key = os.environ.get("OPEN_AI_API_KEY")
        self.client = Chatbot(api_key=api_key, system_prompt='')

    def _call(self, prompt):
        return self.client.ask(prompt)

    def polish(self, text):
        prompt = "Please correct the grammar of the following sentence: {}"
        return self._call(prompt.format(text))

    def translate(self, text, to_language='zh'):
        target_lang = language_dict.get(to_language, 'zh') 
        prompt = "Please translate following sentence as {} without pronunciation: {}"
        return self._call(prompt.format(text, target_lang))
