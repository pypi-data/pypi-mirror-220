import os
import json
import pathlib
from typing import List, Dict, Any, AnyStr

from jam.instrument.base import BaseInstrument
from jam.persistence.base import BasePersistence
from jam.persistence.base import PersistenceObject
from jam.interface.openai import OpenAIChat
from jam.util.generate import generate_id

import requests


class BasePersonnel(object):
    BASE_TEMPLATE = {
        'uid': '<UNIQUE ID>',
        'display_name': '<DISPLAY NAME>',
        'description': '<DESCRIPTION>',
        'categories': ['<CAT-1>', '<CAT-2>']
    }

    def __init__(self,
                 uid: str,
                 display_name: str,
                 description: str,
                 categories: List[str],
                 instruction: str,
                 restriction: str,
                 extra: Dict,
                 mention_only: bool = False):
        self.uid = uid
        self.display_name = display_name
        self.description = description
        self.categories = categories
        self.instruction = instruction
        self.restriction = restriction
        self.extra = extra

        self.instruments = None
        self.persistence = None
        self.functions = None
        self.function_map = None
        self.engine = None

        self.mention_only = mention_only

        self.prompt = self.generate_prompt()

    def setup(self, instruments: List[BaseInstrument], persistence: BasePersistence):
        self.instruments = instruments
        self.persistence = persistence

        self.functions = self._structure_functions()
        self.function_map = self._structure_function_map()
        self.engine = OpenAIChat(functions=self.functions)

    def _structure_functions(self):
        return [func.as_dict() for func in self.instruments]

    def _structure_function_map(self):
        return {func.name: func.activate for func in self.instruments}

    def _retrieve_history(self, cid: AnyStr = 'main'):
        conv_hist = (self.persistence.find(conditions={
            'author': [self.uid, 'user'],
            'mention': [self.uid, 'user'],
            'cid': [cid]
        }))
        return list(map(PersistenceObject.as_message, conv_hist))

    def _retrieve_context(self, cid: AnyStr = 'main'):
        return [{'author': 'system', 'role': 'system', 'content': self.prompt}] + self._retrieve_history(cid=cid)

    def _save_message(self,
                      cid: str,
                      role: str,
                      author: str,
                      content: str,
                      function: str = None,
                      success: bool = True) -> PersistenceObject:
        return self.persistence.save(
            cid=cid,
            role=role,
            author=author,
            content=content,
            function=function,
            success=success
        )

    def call(self, cid: AnyStr = 'main', functional: bool = True) -> List[PersistenceObject]:
        po_outputs = []

        ctx_chain = self._retrieve_context(cid=cid)
        response = self.engine.call(messages=ctx_chain, functional=functional)

        if response.output.get('function_call'):
            f_name, f_response = self.function_call(response.output)

            if f_response.success:
                f_chain = [{'role': 'function', 'content': str(f_response.output), 'name': str(f_name)}]
                ctx_chain = self._retrieve_context(cid=cid) + f_chain
                after_response = self.engine.call(messages=ctx_chain, functional=False)
                saved_response = self._save_message(
                    cid=cid,
                    role='assistant',
                    author=self.uid,
                    content=after_response.output['content'],
                    success=after_response.success
                )
                po_outputs += saved_response

                function_response = self._save_message(
                    cid=cid,
                    role='function',
                    author=self.uid,
                    content=f_response.output,
                    function=f_name,
                    success=f_response.success
                )
                po_outputs += function_response
        else:
            saved_response = self._save_message(
                cid=cid,
                role='assistant',
                author=self.uid,
                content=response.output['content'],
                success=response.success
            )
            po_outputs += saved_response

        return po_outputs

    def function_call(self, x: Any):
        f_name = x['function_call']['name']
        f_call = self.function_map[f_name]
        f_args = json.loads(x['function_call']['arguments'])
        f_response = f_call(**f_args)

        return f_name, f_response

    def _retrieve_obj_const(self):
        return {
            'uid': self.uid,
            'display_name': self.display_name,
            'description': self.description,
            'categories': self.categories,
            'instruction': self.instruction,
            'restriction': self.restriction,
            'extra': self.extra
        }

    def save_json(self, filename: str = None):
        if filename is None:
            filename = self.uid + '.json'

        obj_const = self._retrieve_obj_const()
        with open(filename, 'w') as f_new:
            json.dump(obj_const, f_new)

        return self

    @classmethod
    def get_template(cls, filepath: str = 'new-personnel.json'):
        filename, file_extension = os.path.splitext(filepath)
        if file_extension == '.json':
            with open(filepath, 'w') as f:
                json.dump(cls.BASE_TEMPLATE, f)
            return True
        return False

    def generate_prompt(self):
        prompt = "INSTRUCTION:\n{instruction}\n\n".format(instruction=self.instruction)
        prompt += "RESTRICTIONS:\n{restriction}\n\n".format(restriction=self.restriction)
        prompt += "CHARACTER:\nName: {display_name}\nDescription: {description}\nCategories: {categories}\n\n".format(
            display_name=self.display_name,
            description=self.description,
            categories=', '.join(self.categories)
        )
        prompt += "EXTRA:\n{extra}\n".format(
            extra='\n'.join([
                '{key}: {value}'.format(
                    key=key.title().replace('_', ' '),
                    value=value
                ) for key, value in self.extra.items()
            ])
        )

        return prompt

    @classmethod
    def from_dict(cls, data: Dict, mention_only: bool = False):
        """
        Load Character from Dict

        :param mention_only:
        :param data: Dict
        :return: Instance
        """

        uid = data.get('uid', generate_id(8))
        display_name = data.get('display_name', 'No Name')
        description = data.get('description', '')
        categories = data.get('categories', [])
        instruction = data.get('instruction', '')
        restriction = data.get('restriction', '')
        extra = data.get('extra', {})

        return cls(
            uid=uid,
            display_name=display_name,
            description=description,
            categories=categories,
            instruction=instruction,
            restriction=restriction,
            extra=extra,
            mention_only=mention_only
        )

    @classmethod
    def from_json(cls, filepath: str = None, mention_only: bool = False):
        if os.path.exists(filepath):
            ext_file_df = pathlib.Path(filepath).suffix
            if ext_file_df == '.json' or ext_file_df == '.jsonl':
                with open(filepath, 'r') as config_file:
                    config_json = json.load(config_file)

                return cls.from_dict(data=config_json, mention_only=mention_only)
        raise ValueError(f'File {filepath} is not JSON. Please try another format.')

    @classmethod
    def from_url(cls, url: str = None, mention_only: bool = False):
        if url is None:
            raise ValueError(f'URL with value {url} is irretrievable.')

        response = requests.get(url)
        json_response = json.loads(response.text)

        if response.status_code != 200:
            raise ValueError(f'URL with value {url} is irretrievable. Got status {response.status_code}')
        return cls.from_dict(data=json_response, mention_only=mention_only)

    @classmethod
    def from_preset(cls, name: str, format_url: str = None, mention_only: bool = False):
        if format_url is None:
            format_url = 'https://raw.githubusercontent.com/abhishtagatya/jam_ai/master/example/personnel/{name}.json'

        return cls.from_url(url=format_url.format(name=name), mention_only=mention_only)
