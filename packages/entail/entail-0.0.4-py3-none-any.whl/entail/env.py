import datetime
import json
import sys
from dataclasses import dataclass, field
from typing import Optional

from entail import NLOutputGenerator, RunConfig, TestCase, utils, \
    RuleMatch, Quantifier, Hypothesis, Fn
from entail.results import TestResult, TestResults, PRF1
from entail.nli import NliModel
from entail.assertion import GLOBAL_NLI_MODEL


@dataclass
class TestEnvBuilder:
    handler: NLOutputGenerator = None
    nli: NliModel = None
    config: RunConfig = None
    tests: list[TestCase] = field(default_factory=list)

    def build(self):

        if self.handler is None:
            raise ValueError('There is no ChatHandler to be tested, see .will_be_testing(your_handler)')

        if self.tests is None:
            raise ValueError('There is no testcases, using with_tests or with_test to add test cases')

        if self.config is None:
            self.config = RunConfig()

        if self.nli is None:
            self.nli = GLOBAL_NLI_MODEL

        return TestEnv(
            self.handler,
            nli=self.nli,
            config=self.config,
            tests=self.tests,
        )

    def with_testing_target(self, target: NLOutputGenerator):
        self.handler = target
        return self

    def with_testcases(self, tests):
        return self.with_tests(tests)

    def with_tests(self, tests):
        for t in tests:
            self.tests.append(t)
        return self

    def with_test(self, t):
        self.tests.append(t)
        return self

    def with_config(self, config):
        self.config = config
        return self

    def with_nli_model(self, nli_model):
        self.nli = nli_model
        return self


@dataclass
class TestEnv:
    handler: NLOutputGenerator
    nli: NliModel = field(default_factory=lambda: GLOBAL_NLI_MODEL)
    config: RunConfig = field(default_factory=RunConfig)
    tests: list[TestCase] = field(default_factory=list)

    def run_tests(self, tags=None, name=None):
        todo = []
        if tags is not None:
            if isinstance(tags, str):
                tags = [t.strip() for t in tags.strip(',')]
            for testcase in self.tests:
                match_tag = False
                for t in testcase.tags:
                    for mt in tags:
                        if t == mt:
                            match_tag = True
                            break
                    if match_tag:
                        break
                if match_tag:
                    todo.append(testcase)
        elif name is not None:
            for testcase in self.tests:
                if testcase.name == name:
                    todo.append(testcase)
        else:
            todo = [t for t in self.tests]

        results = []
        for t in todo:
            ret = self.run_test(t)
            results.append(ret)
        return TestResults(results=results, config=self.config)

    def run_test(self, testcase: TestCase) -> TestResult:
        output = self.handler.generate_output(**testcase.args)
        result = TestResult(
            case=testcase,
            output=output,
        )

        if testcase.output.fn_target:
            if self.config.function:
                result.compare_function(testcase.output.fn_target, output.fn)
        else:
            if testcase.output.exact_reference_value:
                result.exact_match = testcase.output.exact_reference_value == output.content
            else:
                if testcase.output.reference_value:
                    if self.config.bleu:
                        result.bleu = utils.bleu(testcase.output.reference_value, output.content)
                    if self.config.rouge:
                        r = utils.rouge(testcase.output.reference_value, output.content)
                        result.rouge_1 = PRF1(
                            precision=r['rouge1'].precision,
                            recall=r['rouge1'].recall,
                            f1=r['rouge1'].fmeasure
                        )
                        result.rouge_l = PRF1(
                            precision=r['rougeL'].precision,
                            recall=r['rougeL'].recall,
                            f1=r['rougeL'].fmeasure
                        )

                    if self.config.meteor:
                        result.meteor = utils.meteor(testcase.output.reference_value, output.content)
                if testcase.output.hypotheses:
                    if self.config.entail:
                        for hypothesis in testcase.output.hypotheses:
                            score = test_hypothesis(hypothesis, self.nli, output.content)
                            result.entails.append(RuleMatch(hypothesis=hypothesis, score=score))

        return result


def test_hypothesis(hypothesis: Hypothesis, nli: NliModel, content: str):
    if hypothesis.quantifier == Quantifier.any_of:
        return max([test_hypothesis(x, nli, content) for x in hypothesis.children])
    elif hypothesis.quantifier == Quantifier.all_of:
        return min([test_hypothesis(x, nli, content) for x in hypothesis.children])
    elif hypothesis.quantifier == Quantifier.none_of:
        return max([1 - test_hypothesis(x, nli, content) for x in hypothesis.children])
    elif hypothesis.quantifier is None:
        score = nli.entail(content, hypothesis.value)
        return score
