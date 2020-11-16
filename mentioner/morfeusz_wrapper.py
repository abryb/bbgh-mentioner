import morfeusz2
import typing


class Lemma(typing.NamedTuple):
    lexeme: str
    mark: str = None

    @staticmethod
    def from_string(lemma: str) -> 'Lemma':
        parts = lemma.split(":")
        if len(parts) > 1:
            return Lemma(lexeme=parts[0], mark=parts[1])
        return Lemma(lexeme=lemma)

    def __str__(self):
        return self.lexeme if self.mark is None else "{}:{}".format(self.lexeme, self.mark)


class Interpretation(typing.NamedTuple):
    range: typing.Tuple[int, int]  # zasięg tuple(0,1)
    segment: str  # segmeng
    lemma: Lemma  # lemat
    marker: str  # znacznik
    prevalence: typing.List[str]  # pospolitość
    classifier: typing.List[str]  # kwalifikator
    starts_at: int  # starting index of segment in text
    ends_at: int  # ending index of segment in text

    @staticmethod
    def from_morfeusz2_interpretation(data: tuple, starts_at: int, ends_at: int) -> 'Interpretation':
        return Interpretation(
            range=(int(data[0]), int(data[1])),
            segment=data[2][0],
            lemma=Lemma.from_string(data[2][1]),
            marker=data[2][2],
            prevalence=data[2][3],
            classifier=data[2][4],
            starts_at=starts_at,
            ends_at=ends_at
        )


class MorfeuszWrapper(object):
    def __init__(self, morf: morfeusz2.Morfeusz):
        self.morfeusz = morf

    def analyse(self, text: str) -> typing.List[Interpretation]:
        index = 0
        last_range = (0, 0)
        result = list()
        for morfeusz_interpretation in self.morfeusz.analyse(text):
            if last_range != (morfeusz_interpretation[0], morfeusz_interpretation[1]):
                index = self._update_index(text, index, morfeusz_interpretation[2][0])
            interpretation = Interpretation.from_morfeusz2_interpretation(
                morfeusz_interpretation,
                index,
                index + len(morfeusz_interpretation[2][0])
            )
            result.append(interpretation)

        return result

    def _update_index(self, text: str, starting_index: int, read_until: str):
        read_until_len = len(read_until)
        max = len(text) - read_until_len
        while text[starting_index:starting_index + read_until_len] != read_until:
            starting_index += 1
            if starting_index > max:
                raise Exception("Something went very wrong!")

        return starting_index
