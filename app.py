from flask import Flask, render_template, request, jsonify
from logic import get_case_details 

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/search", methods=["POST"])
def search_case():
    try:
        data = request.json
        case_type = data.get("caseType") #type:ignore
        case_number = data.get("caseNumber") #type:ignore
        year = data.get("year") #type:ignore
        result_data = get_case_details(case_type, case_number, year)
        if result_data:
            return jsonify({"success": True, "data": result_data})
        else:
            return jsonify({"success": False, "error": "Case not found for the given details."}), 404

    except Exception as e:
        print(f"An error occurred in /search: {e}")
        return jsonify({"success": False, "error": "An internal server error occurred."}), 500

if __name__ == "__main__":
    app.run(debug=True, port=5001)