from flask import Flask, render_template, request
from controllers.csv_controller import CSVController
import json

app = Flask(__name__)

# Cargar prompts desde el archivo prompts.json
with open('prompts.json', 'r', encoding='utf-8') as f:
    prompts = json.load(f)


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        file = request.files["csv_file"]
        prompt = request.form["editablePrompt"]
        ai_provider = request.form["ai_provider"]
        controller = CSVController(file)
        processed_data = controller.process_data(prompt, ai_provider)
        checkbox_checked = request.form.get("checkbox") == "on"  # Verifica si el checkbox está marcado

        if checkbox_checked:
            csv_info = controller.get_csv_info()[0:20000]
        else:
            csv_info = controller.get_csv_info()
            
        return render_template("index.html", data=processed_data, prompts=prompts, prompt=prompt, csv_info=csv_info)
    else:
        return render_template("index.html", prompts=prompts)

if __name__ == "__main__":
    app.run(debug=True)
