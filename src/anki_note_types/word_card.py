from genanki import Model

word_card_model = Model(
    1212121212,
    "Word card",
    fields=[
        {"name": "Question"},
        {"name": "Answer"},
        {"name": "Examples"},
    ],
    templates=[
        {
            "name": "Word card",
            "qfmt": "<div style='text-align: center; font-size: 24px;'>{{Question}}</div>",
            "afmt": "<div style='text-align: center; font-size: 24px;'>{{FrontSide}} <hr id='answer'> {{Answer}} <hr id='examples'> {{Examples}} </div>",
        },
    ],
)
