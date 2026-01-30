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
    # Greek Verb Inflection

    [![Open in molab](https://molab.marimo.io/molab-shield.svg)](https://molab.marimo.io/notebooks/nb_j1RdUZChhwksmx8BDQXfsj)

    **Practice Aorist and Simple Future (Στιγμιαίος Μέλλοντας) forms.**

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
    mo.md(f"""
    To complete the test, you must correctly fill in all fields in all test forms for each selected word.
    """)
    return


@app.cell(hide_code=True)
def _(aorist_markdown):
    aorist_markdown
    return


@app.cell(hide_code=True)
def _(aorist_form, check_aorist, current_verb, mo):
    # Checking of Aorist (Αόριστος)

    aorist_ok, aorist_mesg = False, ""
    if current_verb():
        aorist_ok, aorist_mesg = check_aorist(current_verb()['Word'], aorist_form)

    mo.md(aorist_mesg)
    return (aorist_ok,)


@app.cell(hide_code=True)
def _(future_markdown):
    future_markdown
    return


@app.cell(hide_code=True)
def _(check_future, current_verb, future_form, mo):
    # Checking of Simple Future (Στιγμιαίος Μέλλοντας)

    future_ok, future_mesg = False, ""
    if current_verb():
        future_ok, future_mesg = check_future(current_verb()['Word'], future_form)

    mo.md(future_mesg)
    return (future_ok,)


@app.cell(hide_code=True)
def _(
    aorist_ok,
    current_verb,
    future_ok,
    last_passed_mesg,
    mo,
    process_completion,
    random,
    set_current_verb,
    set_last_passed_mesg,
    set_words4test,
    words,
    words4test,
):
    # Is the test completely passed?

    process_completion(current_verb(), aorist_ok, future_ok, words, words4test(), set_words4test, set_last_passed_mesg, set_current_verb)

    if aorist_ok and future_ok:
        set_current_verb(random.choice(words4test))

    mo.md(last_passed_mesg())
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
            {"Translation": "write", "Word": "γράφω"},
            {"Translation": "read", "Word": "διαβάζω"},
            {"Translation": "speak", "Word": "μιλάω"},
            {"Translation": "drink", "Word": "πίνω"},
            {"Translation": "eat", "Word": "τρώω"},
            {"Translation": "go", "Word": "πηγαίνω"}
        ]
        df = pd.DataFrame(test_data)
    return (df,)


@app.cell(hide_code=True)
def _(get_words, mo, random, table):
    # Initializing

    words = get_words(table)
    words4test, set_words4test = mo.state(words.copy() if words else [])
    last_passed_mesg, set_last_passed_mesg = mo.state("")

    current_verb, set_current_verb = mo.state(None)
    if words4test():
        set_current_verb(random.choice(words4test()))
    return (
        current_verb,
        last_passed_mesg,
        set_current_verb,
        set_last_passed_mesg,
        set_words4test,
        words,
        words4test,
    )


@app.cell(hide_code=True)
def _(aorist_test_form, current_verb, future_test_form, words, words4test):
    # Forms and Markdown creation

    aorist_form, aorist_markdown = aorist_test_form(
            words,
            words4test(),
            current_verb)


    future_form, future_markdown = future_test_form(
            words,
            words4test(),
            current_verb)
    return aorist_form, aorist_markdown, future_form, future_markdown


@app.cell(hide_code=True)
def _(modern_greek_inflexion):
    # General functions

    def get_word_by_type(word, wtype):
        if word and wtype:
            word_type = getattr(modern_greek_inflexion, wtype)
            return word_type(word)
        return None

    def word_kind(word_obj, kind_path):
        if word_obj and kind_path:
            result = word_obj.all()
            for item in kind_path:
                if isinstance(result, dict) and item in result:
                    result = result[item]
                else:
                    return None
            return result
        return None

    def get_words(table):
        if table.value.index is not None:
            selected_words = table.data.loc[table.value.index]
            selected_words = selected_words[['Word', 'Translation']]
            return selected_words.to_dict('records')
        return []
    return get_word_by_type, get_words


@app.cell(hide_code=True)
def _(get_word_by_type, mo, random, words4test):
    # Verb related functions

    def make_test_form(
        *,
        title: str,
        words,
        words4test_val,
        current_verb,
    ):
        """
        Universal helper for test forms.
        """
        form = None
        md_view = mo.md(f'**The word list for {title} is empty.**')

        if current_verb():
            current_verb = current_verb()
            word = current_verb["Word"]
            translation = current_verb["Translation"]

            form = mo.ui.array(
                [
                    mo.ui.text(label="εγώ:"),
                    mo.ui.text(label="εσύ:"),
                    mo.ui.text(label="αυτός,-ή,-ό:"),
                    mo.ui.text(label="εμείς:"),
                    mo.ui.text(label="εσείς:"),
                    mo.ui.text(label="αυτοί,-ές,-ά:"),
                ]
            ).form(show_clear_button=True)
            # защита от stale-данных
            form.verb_word = word

            if len(words4test_val):
                md_view = mo.md(f"""
                ### {title}
                (words: {len(words4test_val)}/{len(words)})

                Translation: **{translation}**

                {form}
                """)

        return form, md_view

    def aorist_test_form(
        words,
        words4test_val,
        current_verb
    ):
        return make_test_form(
            title="Aorist (Αόριστος)",
            words=words,
            words4test_val=words4test_val,
            current_verb=current_verb
        )

    def future_test_form(
        words,
        words4test_val,
        current_verb
    ):
        return make_test_form(
            title="Simple Future (Στιγμιαίος Μέλλοντας)",
            words=words,
            words4test_val=words4test_val,
            current_verb=current_verb
        )

    def check_verb(verb_base, form_array, tense):
        """
        Validates verb forms for Aorist or Future.
        tense: 'aorist' or 'future'
        Returns: (bool, str) - (is_correct, markdown_message)
        """
        if form_array is None or form_array.value is None:
            return False, ""

        # Ignore stale form data from previous verbs
        if hasattr(form_array, 'verb_word') and form_array.verb_word != verb_base:
            return False, ""

        v_obj = get_word_by_type(verb_base, 'Verb')
        if not v_obj:
            return False, "Error: Morphological object not found."

        # Map person/number to internal structure
        # In modern-greek-inflexion, verbs are often [tense][voice][mood][number][person]
        # For A2: we care about active indicative

        persons = ['pri', 'sec', 'ter']
        numbers = ['sg', 'pl']

        # Define paths based on tense
        if tense == 'aorist':
            # active indicative aorist
            base_path = ['aorist', 'active', 'ind']
        elif tense == 'future':
            # future uses conjunctive (subjunctive) forms with 'θα'
            # technically modern-greek-inflexion 'conjunctive' is the 'aorist subjunctive'
            # which is used for simple future.
            base_path = ['conjunctive', 'active', 'ind'] # Note: 'ind' might be 'subj' in some engines, checking...
            # Actually, modern-greek-inflexion uses 'ind' or 'subj'. Let's check 'all()'.
        else:
            return False, "Error: Invalid tense."

        all_forms = v_obj.all()

        # Helper to find forms in dict
        def get_actual_forms(path):
            curr = all_forms
            for step in path:
                if isinstance(curr, dict) and step in curr:
                    curr = curr[step]
                else:
                    return None
            return curr

        # Re-evaluating path for future/conjunctive
        if tense == 'future':
            # Future (Simple) = θα + conjunctive active
            path_prefix = ['conjunctive', 'active', 'ind']
            if not get_actual_forms(path_prefix):
                path_prefix = ['conjunctive', 'active', 'subj']
        else:
            path_prefix = ['aorist', 'active', 'ind']

        pronouns = ['εγώ', 'εσύ', 'αυτός,-ή,-ό', 'εμείς', 'εσείς', 'αυτοί,-ές,-ά']
        success = True
        idx = 0
        errors = []
        for num in numbers:
            for pers in persons:
                user_val = form_array.value[idx].strip()
                pronoun = pronouns[idx]
                idx += 1

                if not user_val:
                    success = False
                    continue

                # For future, we expect 'θα ' prefix
                if tense == 'future':
                    if user_val.startswith('θα '):
                        user_form = user_val[3:].strip()
                    else:
                        # Fail if no 'θα' provided
                        errors.append(f'<span style="color: red; font-weight: bold;">Error!</span> [{pronoun}]: Write the form with **"θα"** (e.g., θα γράψω)')
                        success = False
                        continue
                else:
                    user_form = user_val

                correct_forms = get_actual_forms(path_prefix + [num, pers])

                if not correct_forms or user_form not in correct_forms:
                    success = False
                    expected = "/".join(correct_forms) if correct_forms else "unknown"
                    if tense == 'future':
                        expected = f"θα {expected}"
                    errors.append(f'<span style="color: red; font-weight: bold;">Error!</span> [{pronoun}]: entered **"{user_val}"**, must be **{expected}**')

        return success, "\n\n".join(errors)

    def check_aorist(verb_base, form_array):
        return check_verb(verb_base, form_array, 'aorist')

    def check_future(verb_base, form_array):
        return check_verb(verb_base, form_array, 'future')

    def process_completion(current_verb_val, aorist_ok, future_ok, words, words4test_val, set_words4test, set_last_passed_mesg, set_current_verb):
        passed_mesg = ""
        if aorist_ok and future_ok and current_verb_val:
            new_words4test = [w for w in words4test_val if w["Word"] != current_verb_val["Word"]]
            set_words4test(new_words4test)
            remaining = len(new_words4test)
            total = len(words)
            passed_mesg = f'<span style="color: green;">Test for <b>"{current_verb_val["Word"]} -- {current_verb_val["Translation"]}"</b> passed.\n\n{remaining} words remaining out of {total}.</span>'
            set_last_passed_mesg(passed_mesg)
            if words4test():
                set_current_verb(random.choice(words4test()))
            else:
                set_current_verb(None)

        return passed_mesg
    return (
        aorist_test_form,
        check_aorist,
        check_future,
        future_test_form,
        process_completion,
    )


@app.cell(hide_code=True)
def _():
    import marimo as mo
    import pandas as pd
    import io
    import random

    import modern_greek_inflexion
    from modern_greek_inflexion import Verb
    return io, mo, modern_greek_inflexion, pd, random


if __name__ == "__main__":
    app.run()
