from dataclasses import dataclass, field
from contextlib import contextmanager
from entail.nli import NliModel
from entail.nli.openai import GptNli


class LazyEntail(NliModel):

    def __init__(self):
        self.engine = None

    def entail(self, premise: str, hypothesis: str) -> float:
        if self.engine is None:
            self.engine = GptNli()
        return self.engine.entail(premise, hypothesis)


GLOBAL_NLI_MODEL = LazyEntail()


@contextmanager
def managed_nli_model(nli_model):
    global GLOBAL_NLI_MODEL
    old_model = GLOBAL_NLI_MODEL
    GLOBAL_NLI_MODEL = nli_model
    try:
        yield GLOBAL_NLI_MODEL
    finally:
        GLOBAL_NLI_MODEL = old_model


def assert_hypothesis(premise, hypothesis, threshold=0.5, message=None):
    assert GLOBAL_NLI_MODEL.entail(premise, hypothesis) >= threshold, message


@dataclass
class NLOutput:
    text: str

    def entail_score(self, hypothesis):
        return GLOBAL_NLI_MODEL.entail(self.text, hypothesis)

    def entail(self, hypothesis, threshold=0.5):
        return self.entail_score(self.text, hypothesis) > threshold
