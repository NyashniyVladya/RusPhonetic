# -*- coding: utf-8 -*-
"""
Модуль фонетического разбора слова.

@author: Vladya
"""


class Phonetic(object):

    replace_map = {
        "вств": "ств",
        "дс": "ц",
        "дц": "цц",
        "дч": "чч",
        "жч": "щщ",
        "здн": "зн",
        "здц": "сц",
        "здч": "щщ",
        "зж": "жж",
        "зч": "щщ",
        "зш": "шш",
        "лнц": "нц",
        "ндск": "нск",
        "ндц": "нц",
        "ндш": "нш",
        "нтг": "нг",
        "нтск": "нск",
        "рдц": "рц",
        "рдч": "рч",
        "сж": "жж",
        "стл": "сл",
        "стн": "сн",
        "стс": "сс",
        "стч": "щщ",
        "стьс": "сс",
        "сч": "щщ",
        "сш": "шш",
        "сщ": "щщ",
        "тц": "цц",
        "тч": "чч",
        "тщ": "чщ",
        "ться": "цца",
        "шч": "щщ"
    }

    end_replace = {
        "тс": "ц",
        "тся": "цца",
        "ого": "ово",
        "его": "ево"
    }

    def __init__(self, word, acc):
        """
        :word: Слово для разбора.
        :acc: Номер ударного слога.
        """
        self.word = self.__work_word = word.lower().strip()

        if not self.word:
            raise Exception("Слово не передано.")

        _sylls = self.get_sylls()
        if not _sylls:
            raise Exception("Передано слово без гласных.")
        self.acc = int(acc)
        if not (0 < self.acc <= _sylls):
            raise Exception("Передан неверный номер слога.")

        self.replace_ends()
        for old, new in sorted(
            self.replace_map.items(),
            key=lambda x: len(x[0]),
            reverse=True
        ):
            self.__work_word = self.__work_word.replace(old, new)

    def replace_ends(self):
        for old, new in sorted(
            self.end_replace.items(),
            key=lambda x: len(x[0]),
            reverse=True
        ):
            if self.__work_word.endswith(old):
                self.__work_word = self.__work_word[:(len(old) * -1)] + new

    def get_sylls(self):
        syll_counter = 0
        for s in self.word:
            if s in Letter.vowels:
                syll_counter += 1
        return syll_counter

    def get_phonetic(self):
        _sounds = []
        _last_let = None
        syll_counter = 0
        for s in self.__work_word:
            is_shok = False
            if s in Letter.vowels:
                syll_counter += 1
                if syll_counter == self.acc:
                    is_shok = True
            let = Letter(letter=s, prev_letter=_last_let, shock=is_shok)
            _sounds.append(let)
            _last_let = let
        _sounds[-1].initialize_as_end()
        result = ""
        for s in _sounds:
            result += s.get_sound()
        return result


class Letter(object):

    """
    Класс буквы.
    """

    vowels = "аеёиоуыэюя"  # Гласные буквы
    consonants = "бвгджзйклмнпрстфхцчшщ"  # Согласные буквы
    marks = "ъь"  # Знаки

    forever_hard = "жшц"  # Всегда твёрдые.
    forever_soft = "йчщ"  # Всегда мягкие.

    vovels_set_hard = "аоуыэ"  # Делают предыдущую согласную твёрдой.
    vovels_set_soft = "еёиюя"  # Делают предыдущую согласную мягкой.

    ioted_vowels = {  # Йотированные гласные.
        'е': 'э',
        'ё': 'о',
        'ю': 'у',
        'я': 'а'
    }

    forever_sonorus = "йлмнр"  # Всегда звонкие.
    forever_deaf = "xцчщ"  # Всегда глухие.

    sonorus_deaf_pairs = (  # Пары звонкий-глухой.
        ('б', 'п'),
        ('в', 'ф'),
        ('г', 'к'),
        ('д', 'т'),
        ('ж', 'ш'),
        ('з', 'с')
    )

    def __init__(self, letter, prev_letter=None, shock=False):
        """
        :letter:
            Сама буква.
        :prev_letter:
            Предыдущая буква в слове, если есть.
        :shock:
            Если гласная, то ударная ли.
        """

        if prev_letter is not None:
            __self_type = type(self)
            if not isinstance(prev_letter, __self_type):
                raise Exception(
                    (
                        "Предыдущая буква должна быть объектом класса {0!r}, "
                        "или None (передан тип {1!r})."
                    ).format(__self_type, type(prev_letter))
                )

        self.__letter = letter.lower().strip()
        self.__prev_letter = prev_letter

        if len(self.__letter) != 1:
            raise Exception("Передано неверное количество символов.")

        if not (self.is_vowel() or self.is_consonant() or self.is_mark()):
            raise Exception("Передана не буква русского языка.")

        self.__shock = (self.is_vowel() if shock else False)

        self.__forced_hard = None
        self.__forsed_sonorus = None
        self._forced_not_show = False
        self._is_double = False

        self.set_prev_sonorus()
        self.set_prev_hard()
        self.set_double_sound()

    def set_double_sound(self):
        prev = self.get_prev_letter()
        if not prev:
            return
        prev._forced_not_show = False
        prev._is_double = False
        self._is_double = False
        prev.set_double_sound()
        if self.is_consonant() and prev.is_consonant():
            if self._get_sound() == prev._get_sound():
                prev._forced_not_show = True
                prev._is_double = True
                self._is_double = True

    def set_prev_sonorus(self):
        """
        Выставляет параметры звонкости/глухости, для предыдущих согласных.
        """
        prev = self.get_prev_letter()
        if not prev:
            return
        if not (self.is_consonant() and prev.is_consonant()):
            return
        if self.is_sonorus() and self.is_paired_consonant():
            if self._get_sound(False) != 'в':
                prev.set_sonorus(True)
            return
        if self.is_deaf():
            prev.set_sonorus(False)
            return

    def set_prev_hard(self):
        """
        Выставляет параметры твёрдости/мягкости, для предыдущих согласных.
        """
        prev = self.get_prev_letter()
        if not prev:
            return
        if not prev.is_consonant():
            return
        if self.is_softener(prev):
            prev.set_hard(False)
        elif self.letter in self.vovels_set_hard:
            prev.set_hard(True)

    def is_after_acc(self):
        """
        Буква распологается после ударения.
        """
        prev = self._prev_letter()
        while True:
            if not prev:
                return False
            if prev.is_shock():
                return True
            prev = prev._prev_letter()

    def get_sound(self):
        if self.is_mark() or self._forced_not_show:
            return ""
        _snd = self._get_sound()
        if self._is_double and self.is_after_acc():
            _snd += ":"
        return _snd

    def _get_sound(self, return_soft_mark=True):

        if self.is_mark():
            return ""

        prev = self._prev_letter()
        _letter_now = self.letter

        if self.is_vowel():
            if _letter_now in self.ioted_vowels.keys():

                _let = self.ioted_vowels[_letter_now]
                if (not prev) or prev.is_vowel() or prev.is_mark():
                    _letter_now = "й'{0}".format(_let)
                elif not self.is_shock():
                    _letter_now = 'и'
                else:
                    _letter_now = _let

            if _letter_now == 'о':
                if not self.is_shock():
                    _letter_now = 'а'

            if (_letter_now == 'и') and prev:
                if prev.letter == 'ь':
                    _letter_now = "й'и"
                elif prev.letter in prev.forever_hard:
                    _letter_now = 'ы'
            return _letter_now

        _let = self.get_variant(self.is_deaf())
        if return_soft_mark and self.is_soft():
            _let += "'"
        return _let

    def initialize_as_end(self):
        if self.is_consonant():
            self.set_sonorus(False)

    def set_hard(self, new_value=None):
        if self.letter in (self.forever_hard + self.forever_soft):
            return
        self.__forced_hard = new_value
        self.set_prev_hard()

    def set_sonorus(self, new_value=None):
        self.__forsed_sonorus = new_value
        self.set_prev_sonorus()

    @property
    def letter(self):
        return self.__letter

    def get_prev_letter(self):
        """
        Возвращает предыдущий объект буквы, если она не является знаком.
        Если знак, то рекурсивно спускается, до ближайшей.
        """
        prev = self._prev_letter()
        while True:
            if not prev:
                return prev
            if prev.letter in prev.marks:
                prev = prev._prev_letter()
                continue
            return prev

    def _prev_letter(self):
        """
        Возвращает предыдущую букву, без особых указаний.
        """
        return self.__prev_letter

    def get_variant(self, return_deaf):
        """
        Возвращает вариант буквы.

        :return_deaf:
            True - вернуть глухой вариант. Если False - звонкий.
        """
        return_deaf = bool(return_deaf)
        for variants in self.sonorus_deaf_pairs:
            if self.__letter in variants:
                return variants[return_deaf]
        return self.__letter

    def is_paired_consonant(self):
        """
        Парная ли согласная.
        """
        if not self.is_consonant():
            return False
        for variants in self.sonorus_deaf_pairs:
            if self.letter in variants:
                return True
        return False

    def is_sonorus(self):
        """
        Звонкая ли согласная.
        """
        if not self.is_consonant():
            return False
        if self.letter in self.forever_sonorus:
            return True
        if self.letter in self.forever_deaf:
            return False
        if self.__forsed_sonorus:
            return True
        if self.__forsed_sonorus is False:
            return False
        for son, _ in self.sonorus_deaf_pairs:
            if self.letter == son:
                return True
        return False

    def is_deaf(self):
        """
        Глухая ли согласная.
        """
        if not self.is_consonant():
            return False
        if self.letter in self.forever_deaf:
            return True
        if self.letter in self.forever_sonorus:
            return False
        if self.__forsed_sonorus:
            return False
        if self.__forsed_sonorus is False:
            return True
        for _, df in self.sonorus_deaf_pairs:
            if self.letter == df:
                return True
        return False

    def is_hard(self):
        if not self.is_consonant():
            return False
        if self.letter in self.forever_hard:
            return True
        if self.letter in self.forever_soft:
            return False
        if self.__forced_hard:
            return True
        return False

    def is_soft(self):
        if not self.is_consonant():
            return False
        if self.letter in self.forever_soft:
            return True
        if self.letter in self.forever_hard:
            return False
        if self.__forced_hard is False:
            return True
        return False

    def end(self, string):
        """
        Проверяет, заканчивается ли последовательность букв переданной строкой.
        Скан производится, без учёта текущей.
        """
        prev = self._prev_letter()
        for s in reversed(string):
            if prev.letter != s:
                return False
            if not prev:
                return False
            prev = prev._prev_letter()
        return True

    def is_softener(self, let):
        """
        Является ли символ смягчающим.

        :let: Объект буквы, которую пытаемся смягчить.
        """
        if let.letter in let.forever_hard:
            return False
        if not let.is_consonant():
            return False
        if self.letter in self.vovels_set_soft:
            return True
        if self.letter == 'ь':
            return True
        if self.is_soft() and (let.letter in "дзнст"):
            return True
        if self.letter == 'ъ':
            if self.end("раз") or self.end("из") or self.end("с"):
                return True
        return False

    def is_vowel(self):
        return (self.letter in self.vowels)

    def is_consonant(self):
        return (self.letter in self.consonants)

    def is_mark(self):
        return (self.letter in self.marks)

    def is_shock(self):
        return self.__shock
