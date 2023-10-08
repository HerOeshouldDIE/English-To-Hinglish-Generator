from flask import Flask, render_template, request
from googletrans import Translator

app = Flask(__name__)

class HinglishTranslator:
    def __init__(self, exclusion_list):
        self.exclusion_list = exclusion_list
        self.translator = Translator()

    def translate(self, sentences):
        translations = [self.format_sentence(self.translator.translate(sentence, dest='hi').text) for sentence in sentences]
        return translations

    def format_sentence(self, sentence):
        words = sentence.split()
        formatted = ""

        for word in words:
            if word.lower() in self.exclusion_list:
                formatted += f"<span class='eng'>{word}</span> "
            else:
                formatted += word + " "

        return formatted

exclusion_list = ["minute", "headset"]
translator = HinglishTranslator(exclusion_list)

@app.route('/', methods=['GET', 'POST'])
def index():
    result = None

    if request.method == 'POST':
        input_text = request.form['input_text']
        result = translator.translate([input_text])

    # Example sentences to display and their translations
    examples = [
        "Definitely share your feedback in the comment section.",
        "So even if it's a big video, I will clearly mention all the products.",
        "I was waiting for my bag."
    ]

    translations = translator.translate(examples)

    # Zipping the data
    zipped_data = zip(examples, translations)

    return render_template('index.html', result=result, zipped_data=zipped_data)

if __name__ == "__main__":
    app.run(debug=True)
