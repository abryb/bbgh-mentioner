import morfeusz2


class TextFinder(object):
    def __init__(self, morf: morfeusz2.Morfeusz):
        self.morf = morf

    def find_full_names(self, text: str) -> set:
        """
        :return {('name', 'lastName'), ...}
        """
        result = set()
        result = result.union(self._find_first_and_last_name_pairs(text))
        return result


    def find_last_names(self, text: str) -> set:
        """
        :return {'name', ...}
        """
        result = set()
        analysis = self.morf.analyse(text)
        for interpretation in analysis:
            if u'nazwisko' in interpretation[2][3]:
                result.add((interpretation[2][1].split(":")[0]))
        return result

    def _find_first_and_last_name_pairs(self, text: str) -> set:
        analysis = self.morf.analyse(text)
        result = set()
        last_name_index = -1
        first_name = None
        for interpretation in analysis:
            if last_name_index == interpretation[0]:
                if u'nazwisko' in interpretation[2][3]:
                    result.add((first_name, interpretation[2][1].split(":")[0]))
                    last_name_index = -1
                    first_name = None
                    continue
            if u'imię' in interpretation[2][3]:
                last_name_index = interpretation[0] + 1
                first_name = interpretation[2][1].split(":")[0]

        return result


finder = TextFinder(morfeusz2.Morfeusz())
