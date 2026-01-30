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

    [![Open in molab](https://molab.marimo.io/molab-shield.svg)](https://molab.marimo.io/notebooks/nb_HJPdFCQMSBvpw3EafKK88v)

    **Practice Aorist and Simple Future (Στιγμιαίος Μέλλοντας) forms.**

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
    To complete the test, you must correctly fill in all fields **in all test forms** for each selected word.
    """)
    return


@app.cell(hide_code=True)
def _(aorist_form, cv, gu, mo, words, words4test):
    # Integrated Aorist Test

    feedback_aorist = ""
    if cv:
        _, _msg = gu.check_verb_test(cv['Word'], aorist_form, 'aorist')
        feedback_aorist = mo.md(_msg)

    view_aorist = mo.vstack([
        mo.md(f"### Aorist (Αόριστος) ({len(words4test())}/{len(words)})"),
        mo.md(f"Translation: **{cv['Translation']}**") if cv else mo.md(""),
        aorist_form,
        feedback_aorist
    ]) if words4test() else mo.md("")

    view_aorist
    return


@app.cell(hide_code=True)
def _(cv, future_form, gu, mo, words, words4test):
    # Integrated Simple Future Test

    feedback_future = ""
    if cv:
        _, _msg = gu.check_verb_test(cv['Word'], future_form, 'future')
        feedback_future = mo.md(_msg)

    view_future = mo.vstack([
        mo.md(f"### Simple Future (Στιγμιαίος Μέλλοντας) ({len(words4test())}/{len(words)})"),
        mo.md(f"Translation: **{cv['Translation']}**") if cv else mo.md(""),
        future_form,
        feedback_future
    ]) if words4test() else mo.md("")

    view_future
    return


@app.cell(hide_code=True)
def _(
    aorist_form,
    cv,
    future_form,
    gu,
    last_passed_mesg,
    mo,
    set_last_passed_mesg,
    set_words4test,
    words,
    words4test,
):
    # Final forms check and progression

    if cv:
        a_ok, _ = gu.check_verb_test(cv['Word'], aorist_form, 'aorist')
        f_ok, _ = gu.check_verb_test(cv['Word'], future_form, 'future')

        def set_cv(val): pass 

        gu.process_verb_completion(cv, a_ok, f_ok, words, words4test(), set_words4test, set_last_passed_mesg, set_cv)

    res = mo.md(last_passed_mesg())
    res
    return


@app.cell(hide_code=True)
def _(file_upload, gu):
    # Setup test data

    test_data = [
        {"Translation": "write", "Word": "γράφω"},
        {"Translation": "read", "Word": "διαβάζω"},
        {"Translation": "speak", "Word": "μιλάω"},
        {"Translation": "drink", "Word": "πίνω"},
        {"Translation": "eat", "Word": "τρώω"},
        {"Translation": "go", "Word": "πηγαίνω"}
    ]
    df = gu.load_data(file_upload, test_data)
    return (df,)


@app.cell(hide_code=True)
def _(gu, mo, table):
    # Initialize state variables

    words = gu.get_words(table)
    words4test, set_words4test = mo.state(words.copy() if words else [])
    last_passed_mesg, set_last_passed_mesg = mo.state("")
    return (
        last_passed_mesg,
        set_last_passed_mesg,
        set_words4test,
        words,
        words4test,
    )


@app.cell(hide_code=True)
def _(gu, words, words4test):
    # Setup test forms

    cv = words4test()[0] if words4test() else None # Simple selection from state
    aorist_form, aorist_md = gu.create_verb_test_ui("Aorist (Αόριστος)", words, words4test(), cv)
    future_form, future_md = gu.create_verb_test_ui("Simple Future (Στιγμιαίος Μέλλοντας)", words, words4test(), cv)
    return aorist_form, cv, future_form


@app.cell(hide_code=True)
def _():
    # Package imports

    import marimo as mo
    import greek_utils as gu
    return gu, mo


if __name__ == "__main__":
    app.run()
