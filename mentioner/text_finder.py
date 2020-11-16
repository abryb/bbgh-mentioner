import typing
from morfeusz_wrapper import MorfeuszWrapper

X = typing.TypeVar('X')


class TextFinderResult(typing.Generic[X]):
    def __init__(self, result: X, starts_at: int, ends_at: int):
        self.result = result
        self.starts_at = starts_at
        self.ends_at = ends_at


class FullName(typing.NamedTuple):
    first_name: str
    last_name: str

    def full_name(self):
        return "{} {}".format(self.first_name, self.last_name)


class TextFinder(object):
    def __init__(self, morfeusz_wrapper: MorfeuszWrapper):
        self.morfeusz = morfeusz_wrapper

    def find_full_names(self, text: str) -> typing.List[TextFinderResult[FullName]]:
        result = list()
        last_name_index = -1
        first_name_interpretation = None
        for interpretation in self.morfeusz.analyse(text):
            if last_name_index == interpretation.range[0]:
                if u'nazwisko' in interpretation.prevalence:
                    last_name = interpretation.lemma.lexeme
                    first_name = first_name_interpretation.lemma.lexeme
                    result.append(
                        TextFinderResult(
                            FullName(first_name, last_name),
                            first_name_interpretation.starts_at,
                            interpretation.ends_at
                        )
                    )
                    last_name_index = -1
                    first_name_interpretation = None
                    continue
            if u'imię' in interpretation.prevalence:
                last_name_index = interpretation.range[0] + 1
                first_name_interpretation = interpretation
        return result

    def find_last_names(self, text: str) -> typing.List[TextFinderResult[str]]:
        result = list()
        for interpretation in self.morfeusz.analyse(text):
            if u'nazwisko' in interpretation.prevalence:
                result.append(
                    TextFinderResult(interpretation.lemma.lexeme, interpretation.starts_at, interpretation.ends_at)
                )
        return result
