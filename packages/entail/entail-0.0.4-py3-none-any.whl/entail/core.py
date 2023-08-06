import abc
import json
import os
from typing import Optional, Union
from pydantic import BaseModel, Field
from enum import Enum


class NLOutputGenerator(object):
    def __init__(self):
        pass

    @abc.abstractmethod
    def generate(self, **kwargs) -> Union['Fn', str, None]:
        raise NotImplementedError()

    def generate_output(self, **kwargs) -> 'NLOutput':
        o = self.generate(**kwargs)
        if o is None:
            return NLOutput.none()

        return NLOutput.create_from_value(o)

    @staticmethod
    def wrap(f) -> 'NLOutputGenerator':
        return SimpleNLOutputGenerator(f)

    @staticmethod
    def from_chatgpt_output(msg_dict):
        if 'function_call' in msg_dict:
            name = msg_dict['function_call']['name']
            args_str = msg_dict['function_call'].get('arguments', {})
            if args_str == '' or args_str is None:
                args_str = '{}'
            args = json.loads(args_str)
            return Fn(name, args)
        elif 'content' in msg_dict:
            if isinstance(msg_dict['content'], str):
                return msg_dict['content']
        else:
            raise ValueError('Cannot auto process chatgpt output, '
                             'please return a Fn or str object manually')


class SimpleNLOutputGenerator(NLOutputGenerator):
    def __init__(self, f):
        self.f = f

    def generate(self, **kwargs) -> Union['Fn', str, None]:
        return self.f(**kwargs)


class Quantifier(str, Enum):
    any_of = 'any_of'
    all_of = 'all_of'
    none_of = 'none_of'


class Hypothesis(BaseModel):
    quantifier: Optional[Quantifier] = None
    children: Optional[list['Hypothesis']] = None
    value: Optional[str] = None

    @staticmethod
    def any_of(*args):
        return Hypothesis(quantifier=Quantifier.any_of, children=[Hypothesis.of(c) for c in args])

    @staticmethod
    def all_of(*args):
        return Hypothesis(quantifier=Quantifier.all_of, children=[Hypothesis.of(c) for c in args])

    @staticmethod
    def none_of(*args):
        return Hypothesis(quantifier=Quantifier.none_of, children=[Hypothesis.of(c) for c in args])

    @staticmethod
    def of(value: str):
        if isinstance(value, str):
            return Hypothesis(quantifier=None, value=value)
        elif isinstance(value, Hypothesis):
            return value
        else:
            raise ValueError('Hypothesis.of can only construct hypothesis from str of Hypothesis instance')

    def to_str(self):
        if self.quantifier == Quantifier.any_of:
            children = "\n".join([c.to_str() for c in self.children])
            return f"At least one of the following should be true: \n {children}"
        elif self.quantifier == Quantifier.all_of:
            children = "\n".join([c.to_str() for c in self.children])
            return f"All of the following should be true: \n {children}"
        elif self.quantifier == Quantifier.none_of:
            children = "\n".join([c.to_str() for c in self.children])
            return f"None of the following should be true: \n {children}"
        else:
            return self.value


class Fn(BaseModel):
    name: str
    args: dict = Field(default_factory={})

    def __init__(self,
                 name: str,
                 args: Optional[dict] = None,
                 **kwargs) -> None:
        if args is None:
            args = {}
        super(Fn, self).__init__(
            name=name,
            args=args,
            **kwargs
        )


class NLOutput(BaseModel):
    content: Optional[str] = None
    fn: Optional[Fn] = None

    @staticmethod
    def none():
        return NLOutput()

    @staticmethod
    def create_from_value(value):
        if isinstance(value, str):
            return NLOutput(content=value)
        elif isinstance(value, Fn):
            return NLOutput(fn=value)
        else:
            raise ValueError(f'Message value must be str or Fn')

    @property
    def is_none(self):
        return self.fn is None and self.content is None

    @property
    def is_function(self):
        return self.fn is not None

    @property
    def is_text(self):
        return self.content is not None


class DesiredOutput(BaseModel):
    """
    A class describing the desired output of a chat message.

    When describing a desired text output, you should supply at least one of the example, exact, and should_be field
    When describing a desired function call output, you should supply should_call_function

    example: A reference response.
    should_be:
    should_call_function: what function should the response call
    """

    reference_value: Optional[list[str]] = None
    exact_reference_value: Optional[list[str]] = None
    hypotheses: Optional[list[Hypothesis]] = None
    fn_target: Optional[Fn] = None

    def should_be_exactly(self, *args):
        if self.exact_reference_value is None:
            self.exact_reference_value = []

        if isinstance(args, str):
            self.exact_reference_value.append(args)
        elif isinstance(args, list) or isinstance(args, tuple):
            for v in args:
                self.exact_reference_value.append(v)
        return self

    def should_be_similar_to_reference(self, *args):
        if self.reference_value is None:
            self.reference_value = []

        if isinstance(args, str):
            self.reference_value.append(args)
        elif isinstance(args, list) or isinstance(args, tuple):
            for v in args:
                self.reference_value.append(v)
        return self

    def should_be_function_call(self, fn_target):
        self.fn_target = fn_target
        return self

    def should_entail(self, *args):
        if self.hypotheses is None:
            self.hypotheses = []

        if isinstance(args, list) or isinstance(args, tuple):
            for v in args:
                self.add_hypothesis(v)
        else:
            self.add_hypothesis(args)

        return self

    def add_hypothesis(self, hypothesis):
        if self.hypotheses is None:
            self.hypotheses = []

        if isinstance(hypothesis, str):
            self.hypotheses.append(
                Hypothesis.of(hypothesis)
            )
        elif isinstance(hypothesis, Hypothesis):
            self.hypotheses.append(hypothesis)
        else:
            raise ValueError('Hypothesis must be Union[str, Hypothesis]')


class TestCase(BaseModel):
    """
    A test case for chat model
    name: A optional name for this testcase, i.e. you can run a testcase by name
    description: A description of what is this test case testing.
    tags:  A list of tags for this testcase, i.e. you can run a list of testcases contains a certain tag
    args: input to your own model
    output: describe the desired output
    """
    name: Optional[str] = None
    description: Optional[str] = None
    tags: Optional[list[str]] = None

    args: Optional[dict] = None

    output: DesiredOutput = Field(default_factory=DesiredOutput)
    path: str = ''


class RuleMatch(BaseModel):
    hypothesis: Hypothesis
    score: float


def create_default_nli():
    from entail.assertion import GLOBAL_NLI_MODEL
    return GLOBAL_NLI_MODEL


def create_testing_env(test_folder, testing=None, ):
    pass


def load_tests_from_str(content):
    local_ctx = {}
    exec(content, globals(), local_ctx)
    for k, v in local_ctx.items():
        if isinstance(v, TestCase):
            yield v


def load_testcases(folder_path):
    extensions = ['.entail.py']
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            file_path = os.path.join(root, file)
            if any(file_path.endswith(ext) for ext in extensions):
                with open(file_path) as fd:
                    for cases in load_tests_from_str(fd.read()):
                        yield cases
