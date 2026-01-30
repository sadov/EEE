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

    [![Open in molab](https://molab.marimo.io/molab-shield.svg)](https://molab.marimo.io/notebooks/nb_KZYjBCXm1jiSjMBnvxWezi)

    **You can test your knowledge of noun declensions on this page.**

    Use the sample word set or upload a TAB-delimited CSV file with "Word" and "Translation" columns.
    """)
    return


@app.cell(hide_code=True)
def _(df, mo):
    table = mo.ui.table(df, selection="multi") if df is not None else None
    table
    return (table,)


@app.cell(hide_code=True)
def _(mo):
    file_upload = mo.ui.file(label="Load CSV")
    file_upload
    return (file_upload,)


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    To complete the test, you must correctly fill in all fields in **one of the test forms** for each selected word.
    """)
    return


@app.cell(hide_code=True)
def _(current_noun, gu):
    # Setup simple test form (reactive to shared current word state)
    _cn = current_noun()
    noun, noun_trans, noun_form = gu.create_noun_test_ui([_cn] if _cn else [], mode='simple')
    return noun, noun_form, noun_trans


@app.cell(hide_code=True)
def _(current_noun, gu):
    # Setup article test form (reactive to shared current word state)
    _acn = current_noun()
    art_noun, art_noun_trans, art_noun_form = gu.create_noun_test_ui([_acn] if _acn else [], mode='article')
    return art_noun, art_noun_form, art_noun_trans


@app.cell(hide_code=True)
def _(gu, mo, noun, noun_form, noun_trans, words, words4test):
    # View Simple Test
    _feedback = ""
    if words4test() and noun:
        with mo.capture_stdout() as _buffer:
            gu.check_noun_test(noun, noun_form, mode='simple')
            _feedback = _buffer.getvalue()

        _view = mo.vstack([
            mo.md(f"**Simple test for Nouns** ({len(words4test())}/{len(words)})"),
            mo.md(f"Translation: **{noun_trans}**"),
            noun_form,
            mo.md(_feedback)
        ])
    else:
        _view = mo.md('**The word list is empty.**')

    _view
    return


@app.cell(hide_code=True)
def _(art_noun, art_noun_form, art_noun_trans, gu, mo, words, words4test):
    # View Article Test
    _feedback = ""
    if words4test() and art_noun:
        with mo.capture_stdout() as _buffer:
            gu.check_noun_test(art_noun, art_noun_form, mode='article')
            _feedback = _buffer.getvalue()

        _view_art = mo.vstack([
            mo.md(f"**Test for Nouns with Articles** ({len(words4test())}/{len(words)})"),
            mo.md(f"Translation: **{art_noun_trans}**"),
            art_noun_form,
            mo.md(_feedback)
        ])
    else:
        _view_art = mo.md('**The word list is empty.**')

    _view_art
    return


@app.cell(hide_code=True)
def _(last_passed_mesg, mo):
    # Progression message display
    _res = mo.md(last_passed_mesg())
    _res
    return


@app.cell(hide_code=True)
def _(
    gu,
    noun,
    noun_form,
    set_current_noun,
    set_last_passed_mesg,
    set_words4test,
    words,
    words4test,
):
    # Logic Simple progression
    if words4test() and noun:
        gu.process_noun_test(noun, noun_form, words, words4test, set_words4test, set_last_passed_mesg, set_current_noun, mode='simple')
    return


@app.cell(hide_code=True)
def _(
    art_noun,
    art_noun_form,
    gu,
    set_current_noun,
    set_last_passed_mesg,
    set_words4test,
    words,
    words4test,
):
    # Logic Article progression (syncs current_noun)
    if words4test() and art_noun:
        gu.process_noun_test(art_noun, art_noun_form, words, words4test, set_words4test, set_last_passed_mesg, set_current_noun, mode='article')
    return


@app.cell(hide_code=True)
def _(file_upload, gu):
    # Setup test data

    test_data = [
        {"Translation": "schedule, working hours", "Word": "το ωράριο"},
        {"Translation": "hour", "Word": "η ώρα"},
        {"Translation": "space, room", "Word": "ο χώρος"}
    ]
    df = gu.load_data(file_upload, test_data)
    return (df,)


@app.cell(hide_code=True)
def _(gu, mo, random, table):
    # Initialize state variables
    words = gu.get_words(table)
    words4test, set_words4test = mo.state(words.copy() if words else [])
    last_passed_mesg, set_last_passed_mesg = mo.state("")

    current_noun, set_current_noun = mo.state(None)

    # Sync current word state if words were selected/loaded
    if words:
        if current_noun() is None:
            set_current_noun(random.choice(words))
    return (
        current_noun,
        last_passed_mesg,
        set_current_noun,
        set_last_passed_mesg,
        set_words4test,
        words,
        words4test,
    )


@app.cell(hide_code=True)
def _():
    import random
    import marimo as mo
    import greek_utils as gu
    return gu, mo, random


if __name__ == "__main__":
    app.run()
