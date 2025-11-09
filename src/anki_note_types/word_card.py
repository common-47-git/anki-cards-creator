from genanki import Model

word_card_model = Model(
    1212121212,
    "Word card",
    fields=[
        {"name": "Word"},
        {"name": "Transcription"},
        {"name": "Answer"},
        {"name": "Examples"},
    ],
    templates=[
        {
            "name": "Word card",
            "qfmt": """
                <div style='text-align: center; font-size: 28px; font-weight: bold; margin-bottom: 10px;'>
                    {{Word}}
                </div>
                <div style='text-align: center; font-size: 20px; font-style: italic; color: #555;'>
                    {{Transcription}}
                </div>
            """,
            "afmt": """
                <div style='text-align: center; font-size: 28px; font-weight: bold; margin-bottom: 10px;'>
                    {{Word}}
                </div>
                <div style='text-align: center; font-size: 20px; font-style: italic; color: #555; margin-bottom: 15px;'>
                    {{Transcription}}
                </div>
                <hr style='border: 1px solid #ccc; margin: 10px 0;'>
                <div style='text-align: center; font-size: 22px; margin-bottom: 15px;'>
                    {{Answer}}
                </div>
                <hr style='border: 1px solid #ccc; margin: 10px 0;'>
                <div style='text-align: center; font-size: 20px;'>
                    {{Examples}}
                </div>
            """,
        },
    ],
)
