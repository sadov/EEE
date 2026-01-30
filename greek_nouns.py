# /// script
# requires-python = ">=3.12"
# dependencies = [
#     "marimo>=0.19.4",
#     "mcp==1.25.0",
#     "modern-greek-inflexion==2.0.7",
#     "pandas==2.3.3",
# ]
# ///

import marimo

__generated_with = "0.19.7"
app = marimo.App(
    width="medium",
    css_file="/usr/local/_marimo/custom.css",
    auto_download=["html"],
)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Greek Noun Declension

    [![Open in molab](https://molab.marimo.io/molab-shield.svg)](https://molab.marimo.io/notebooks/nb_tWcRtwDGGgzokqXTYf9wdb)

    **You can test your knowledge of noun declensions on this page.**

    You can use the sample word set or upload a TAB-delimited CSV file with "Word" and "Translation" columns.
    """)
    return


@app.cell(hide_code=True)
def _(df, mo):
    table = None
    if df is not None:
        table = mo.ui.table(df, selection="multi")
    table
    return (table,)


@app.cell(hide_code=True)
def _(mo):
    file_upload = mo.ui.file(label="Load CSV")
    file_upload
    return (file_upload,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    To complete the test, you must correctly fill in all fields in one of the test forms for each selected word.
    """)
    return


@app.cell(hide_code=True)
def _(mo, nouns_test_form, words, words4test):
    noun, noun_trans, noun_test_form=nouns_test_form(words)
    if len(words4test):
        noun_test_text = f"""
    **Simple test for Nouns**
    (words: {len(words4test)}/{len(words)})

    Write the forms of noun without articles.

    Translation: **{noun_trans}**
    {noun_test_form}
    """
    else:
        noun_test_text = '**The word list is empty.**'

    mo.md(noun_test_text)
    return noun, noun_test_form


@app.cell(hide_code=True)
def _(
    check_noun,
    mo,
    noun,
    noun_test_form,
    process_noun_test,
    words,
    words4test,
):
    noun_mesg = process_noun_test(noun, noun_test_form, words, words4test, check_noun)
    mo.md(noun_mesg)
    return


@app.cell(hide_code=True)
def _(art_nouns_test_form, mo, words, words4test):
    art_noun, art_noun_trans, art_noun_test_form=art_nouns_test_form(words)
    if len(words4test):
        art_noun_test_text = f"""
    **Test for Nouns with Articles**
    (words: {len(words4test)}/{len(words)})

    Write the forms of noun with articles.

    Translation: **{art_noun_trans}**
    {art_noun_test_form}
    """
    else:
        art_noun_test_text = '**The word list is empty.**'

    mo.md(art_noun_test_text)
    return art_noun, art_noun_test_form


@app.cell(hide_code=True)
def _(
    art_noun,
    art_noun_test_form,
    check_art_noun,
    mo,
    process_noun_test,
    words,
    words4test,
):
    art_noun_mesg = process_noun_test(art_noun, art_noun_test_form, words, words4test, check_art_noun)
    mo.md(art_noun_mesg)
    return


@app.cell(hide_code=True)
def _(file_upload, io, pd):
    # Load data
    df = None
    if file_upload.value:
        # Load data from file
        contents = file_upload.value[0].contents
        contents = io.BytesIO(contents)
        df = pd.read_csv(contents, sep='\t')
    else:
        # Just a lot of sample data
        test_data = [
            {"Translation": "schedule, working hours", "Word": "το ωράριο"},
            {"Translation": "hour", "Word": "η ώρα"},
            {"Translation": "space, room", "Word": "ο χώρος"}
        ]
        df = pd.DataFrame(test_data)
    #df
    return (df,)


@app.cell(hide_code=True)
def _(table):
    selected_indices = []

    if table is not None and table.value is not None:
        selected_indices = table.value.index.tolist()

    #selected_indices
    return


@app.cell(hide_code=True)
def _(get_words, table):
    words = get_words(table)
    if words:
        words4test = words.copy()
    else:
        words = []
        words4test = []
    return words, words4test


@app.cell(hide_code=True)
def _(modern_greek_inflexion):
    # General functions

    def get_word_by_type(word, wtype):
        """
        Wraps a raw word string into a morphological object of a given type.

        Args:
            word (str): Base word form.
            wtype (str): Word type name corresponding to an attribute
                         in modern_greek_inflexion (e.g. 'Noun', 'Verb').

        Returns:
            object | None:
                An instance of the corresponding inflection class,
                or None if input is invalid.
        """
        if word and type:
            word_type = getattr(modern_greek_inflexion, wtype)
            word = word_type(word)
            return word
        else:
            return None


    def word_kind(word, kind):
        """
        Extracts specific grammatical forms from a morphological word object.

        Args:
            word (object): Morphological object with .all() method.
            kind (list[str]): Path describing grammatical features
                              (e.g. ['sg', 'acc'], ['pl', 'masc', 'gen']).

        Returns:
            Any | None:
                Nested value from the word description corresponding to `kind`,
                or None if input is invalid.
        """
        if word and kind:
            result = word.all()
            if kind:
                for item in kind:
                    result = result[item]
            return result
        else:
            return None


    def check_word(check, word, wtype, kind):
        """
        Checks whether a given form exists among the inflected forms of a word.

        Args:
            check (str): Word form to validate.
            word (str): Base form of the word.
            wtype (str): Word type (e.g. 'Noun').
            kind (list[str]): Grammatical path to the required forms.

        Returns:
            bool | None:
                True if form is valid, None otherwise.
        """
        if check and word and type and kind:
            word = get_word_by_type(word, wtype)
            if word:
                word = word_kind(word, kind)
                if word:
                    return check in word
        return None


    def get_words(table):
        """
        Selects a random subset of words from a table widget.

        Args:
            table: UI table object with `value` and `data` attributes.

        Returns:
            list: A list of dictionaries, each containing:
                - "Word": the basic form of the word (e.g., "το ωράριο")
                - "Translation": the translation (e.g., "schedule, working hours")
        """
        selected_words = {}
        if table.value.index is not None:
            selected_words = table.data.loc[table.value.index]
            selected_words = selected_words[['Word', 'Translation']]
            selected_words = selected_words.to_dict('records')
        return selected_words
    return check_word, get_word_by_type, get_words, word_kind


@app.cell(hide_code=True)
def _(Article, check_word, get_word_by_type, mo, random, word_kind):
    # Nouns related functions

    def nouns_test_form(words):
        """
        Creates a UI form for testing noun declension without articles.

        Args:
            words (list[str]): List of base nouns.

        Returns:
            tuple:
                word (str): Randomly selected noun.
                noun_form: UI array with input fields for declension.
        """
        word = None
        noun_form = None
        translation = None
        if words:
            item = random.choice(words)
            word = item['Word']
            translation = item['Translation']

            noun_form = mo.ui.array([
                mo.ui.text(label='Sg. Nom.:'),
                mo.ui.text(label='Sg. Acc.:'),
                mo.ui.text(label='Sg. Gen.:'),
                mo.ui.text(label='Pl. Nom.:'),
                mo.ui.text(label='Pl. Acc.:'),
                mo.ui.text(label='Pl. Gen.:'),
            ])
        return word, translation, noun_form


    def art_nouns_test_form(words):
        """
        Creates a UI form for testing noun declension with articles.

        Args:
            words (list[str]): List of base nouns.

        Returns:
            tuple:
                word (str): Randomly selected noun.
                noun_form: UI array with definite and indefinite article forms.
        """
        word = None
        noun_form = None
        translation = None
        if words:
            item = random.choice(words)
            word = item['Word']
            translation = item['Translation']

            noun_form = mo.ui.array([
                mo.ui.text(label='Def. Sg. Nom.:'),
                mo.ui.text(label='Def. Sg. Acc.:'),
                mo.ui.text(label='Def. Sg. Gen.:'),
                mo.ui.text(label='Def. Pl. Nom.:'),
                mo.ui.text(label='Def. Pl. Acc.:'),
                mo.ui.text(label='Def. Pl. Gen.:'),
                mo.ui.text(label='Ind. Sg. Nom.:'),
                mo.ui.text(label='Ind. Sg. Acc.:'),
                mo.ui.text(label='Ind. Sg. Gen.:'),
            ])
        return word, translation, noun_form


    def noun_declension_test(word, declension, noun, descr, article_descr):
        """
        Validates a single noun form (optionally with article).

        Args:
            word (str): User-entered form (may include article).
            declension (list[str]): ['sg'|'pl', 'nom'|'acc'|'gen'].
            noun (str): Base noun (without article).
            descr (dict): Full noun description from morphology engine.
            article_descr (Article | None): Article descriptor or None.

        Returns:
            bool:
                True if form is correct, False otherwise.
        """
        if not word:
            return False
        # Split article and noun if both are present
        word_array = word.split()
        if len(word_array) > 1:
            noun_article = word_array[0].strip()
            noun_word = word_array[1].strip()
        else:
            noun_article = ''
            noun_word = word.strip()

        noun_type = list(descr.keys())[0]
        noun_declension = declension.copy()
        noun_declension.insert(0, noun_type)

        # Validate noun form
        word_is_correct = check_word(
            check=noun_word,
            word=noun,
            wtype='Noun',
            kind=noun_declension
        )

        # Compute correct form for error reporting
        correct_word = get_word_by_type(noun, wtype='Noun')
        correct_word = word_kind(correct_word, kind=noun_declension)

        # Case without article
        if article_descr is None:
            if word_is_correct:
                return True
            else:
                case_label = f"{declension[0]}.{declension[1]}"
                print(f'<span style="color: red; font-weight: bold;">Error!</span> [{case_label}]: entered **"{noun_word}"**, must be **{correct_word}**\n\n')
                return False

        # Case with article
        art_declension = declension.copy()
        art_declension.insert(1, noun_type)

        article_base = article_descr.article
        article_forms = word_kind(article_descr, art_declension)

        if noun_article in article_forms and word_is_correct:
            return True
        else:
            article_type = 'def' if article_base in ['ο', 'η', 'το'] else 'indef'
            case_label = f"{article_type}.{declension[0]}.{declension[1]}"
            correct_full = ' '.join([str(article_forms), str(correct_word)])
            print(f'<span style="color: red; font-weight: bold;">Error!</span> [{case_label}]: entered **"{word}"**, must be **{correct_full}**\n\n')

            return False


    def check_noun(noun, noun_form):
        """
        Checks noun declension without articles in all required forms.

        Args:
            noun (str): Base noun (article will be ignored if present).
            noun_form: UI array containing user-entered forms.

        Returns:
            bool:
                True if all forms are correct, False otherwise.
        """
        noun_array = noun.split()
        noun_word = noun_array[1].strip() if len(noun_array) > 1 else noun.strip()

        descr = get_word_by_type(word=noun_word, wtype='Noun')
        descr = descr.all()

        if not descr:
            print(f"Error: word '{noun_word}' not found in noun dictionary")
            return False

        return all([
            noun_declension_test(noun_form.value[0], ['sg', 'nom'], noun_word, descr, None),
            noun_declension_test(noun_form.value[1], ['sg', 'acc'], noun_word, descr, None),
            noun_declension_test(noun_form.value[2], ['sg', 'gen'], noun_word, descr, None),
            noun_declension_test(noun_form.value[3], ['pl', 'nom'], noun_word, descr, None),
            noun_declension_test(noun_form.value[4], ['pl', 'acc'], noun_word, descr, None),
            noun_declension_test(noun_form.value[5], ['pl', 'gen'], noun_word, descr, None),
        ])


    def check_art_noun(noun, noun_form):
        """
        Checks noun declension with definite and indefinite articles.

        Args:
            noun (str): Base noun (article may be present).
            noun_form: UI array containing user-entered forms.

        Returns:
            bool:
                True if all forms are correct, False otherwise.
        """
        noun_array = noun.split()
        noun_word = noun_array[1].strip() if len(noun_array) > 1 else noun

        descr = get_word_by_type(word=noun_word, wtype='Noun')
        descr = descr.all()

        if not descr:
            print(f"Error: word '{noun_word}' not found in noun dictionary")
            return False

        article_def = Article('ο')
        article_indef = Article('ένας')

        return all([
            noun_declension_test(noun_form.value[0], ['sg', 'nom'], noun_word, descr, article_def),
            noun_declension_test(noun_form.value[1], ['sg', 'acc'], noun_word, descr, article_def),
            noun_declension_test(noun_form.value[2], ['sg', 'gen'], noun_word, descr, article_def),
            noun_declension_test(noun_form.value[3], ['pl', 'nom'], noun_word, descr, article_def),
            noun_declension_test(noun_form.value[4], ['pl', 'acc'], noun_word, descr, article_def),
            noun_declension_test(noun_form.value[5], ['pl', 'gen'], noun_word, descr, article_def),
            noun_declension_test(noun_form.value[6], ['sg', 'nom'], noun_word, descr, article_indef),
            noun_declension_test(noun_form.value[7], ['sg', 'acc'], noun_word, descr, article_indef),
            noun_declension_test(noun_form.value[8], ['sg', 'gen'], noun_word, descr, article_indef),
        ])

    def process_noun_test(noun, noun_test_form, words, words4test, check_func):
        """
        Processes noun test result and removes the word from test list if passed.

        Args:
            noun: the noun being tested
            noun_test_form: form with noun declensions to check
            words: complete list of words (for statistics)
            words4test: list of words remaining to test (will be modified)
            check_noun: function for noun checking (eg. check_noun, check_art_noun)

        Returns:
            str: Markdown-formatted message about test result

        Example:
            message = process_noun_test(noun, noun_test_form, words, words4test)
            mo.md(message)
        """
        output = ''
        with mo.capture_stdout() as buffer:
            if len(words4test) and check_func(noun, noun_test_form):
                # Remove word from words list
                for i, word in enumerate(words4test):
                    if word["Word"] == noun:
                        words4test.pop(i)
                        break
                remaining = len(words4test)
                total = len(words)
                print(f'<span style="color: green;">Test for <b>"{noun}"</b> passed.\n\n{remaining} words remaining out of {total}.</span>')
            output = buffer.getvalue()

        return output
    return (
        art_nouns_test_form,
        check_art_noun,
        check_noun,
        nouns_test_form,
        process_noun_test,
    )


@app.cell(hide_code=True)
def _():
    import marimo as mo
    import pandas as pd
    import io
    import random

    import modern_greek_inflexion
    from modern_greek_inflexion import Adjective, Adverb, Article, Noun, Numeral, Pronoun, Verb
    return Article, io, mo, modern_greek_inflexion, pd, random


if __name__ == "__main__":
    app.run()
