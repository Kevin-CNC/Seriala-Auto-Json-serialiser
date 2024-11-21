from flask import Flask, render_template, request, jsonify
import converter # actual converter module

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('main.html')

@app.route('/generate_class', methods=['POST'])
def generate_class():
    data = request.json # gather jsonified data from form & fill inputs
    json_input = data.get("json_input") 
    class_name = data.get("class_name")
    case_style = data.get("case_style")
    language = data.get("language")

    try:
        json_obj = json_input
    except ValueError:
        return jsonify({"error": "Invalid JSON format."})

    RESULT = converter._Translate_(json_input,class_name,language,case_style) # performs logic for translation
    RESULT.strip(r'\n')
    return jsonify({"class_output": RESULT}) # returns json string with only 1 field: 'class_output'

if __name__ == '__main__':
    app.run(debug=True)
