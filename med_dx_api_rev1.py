from flask import Flask, jsonify, request
import requests
from collections import Counter
import os

app = Flask(__name__)

# Constants
OPENFDA_ENDPOINT = "https://api.fda.gov/drug/event.json"
DEFAULT_LIMIT = 100  # Limit the number of records we fetch for performance

# Cache symptoms on startup
cached_symptoms = []

def fetch_symptoms():
    """Fetch symptoms from OpenFDA and cache them."""
    try:
        response = requests.get(OPENFDA_ENDPOINT, params={"limit": DEFAULT_LIMIT}, timeout=5)
        response.raise_for_status()
        data = response.json()

        symptoms = []
        for result in data.get('results', []):
            for reaction in result.get('patient', {}).get('reaction', []):
                symptom = reaction.get('reactionmeddrapt')
                if symptom:
                    symptoms.append(symptom.lower())

        return symptoms

    except Exception as e:
        print(f"Error fetching symptoms: {e}")
        return []

@app.route('/', methods=['GET'])
def home():
    """Homepage showing available API endpoints."""
    return jsonify({
        "message": "Welcome to the Healthcare Symptom API!",
        "endpoints": {
            "/symptoms": "List all reported symptoms",
            "/top-symptoms": "List top 5 most common symptoms",
            "/diagnosis (POST)": "Provide a list of symptoms to get associated medicinal products"
        }
    })

@app.route('/symptoms', methods=['GET'])
def list_symptoms():
    """Return all available symptoms."""
    return jsonify({
        "symptoms": sorted(set(cached_symptoms))
    })

@app.route('/top-symptoms', methods=['GET'])
def top_symptoms():
    """Return the top 5 most common symptoms."""
    counter = Counter(cached_symptoms)
    top_five = counter.most_common(5)
    return jsonify({
        "top_symptoms": [{"symptom": symptom, "count": count} for symptom, count in top_five]
    })

@app.route('/diagnosis', methods=['POST'])
def diagnosis_by_symptoms():
    """Accept one or more symptoms and return associated medicinal products."""
    try:
        data = request.get_json()

        if not data or "symptoms" not in data:
            return jsonify({"error": "Please provide a JSON body with a 'symptoms' list."}), 400
        
        symptoms = data["symptoms"]

        if not isinstance(symptoms, list) or not symptoms:
            return jsonify({"error": "'symptoms' must be a non-empty list."}), 400

        all_diagnoses = {}

        for symptom in symptoms:
            try:
                response = requests.get(OPENFDA_ENDPOINT, params={
                    "search": f"patient.reaction.reactionmeddrapt:\"{symptom}\"",
                    "limit": 30
                }, timeout=5)
                response.raise_for_status()
                data = response.json()

                products = []
                for result in data.get('results', []):
                    for drug in result.get('patient', {}).get('drug', []):
                        product = drug.get('medicinalproduct')
                        if product:
                            products.append(product)

                unique_products = sorted(list(set(products)))

                if unique_products:
                    all_diagnoses[symptom] = unique_products
                else:
                    all_diagnoses[symptom] = ["No associated products found."]

            except Exception as e:
                all_diagnoses[symptom] = [f"Error retrieving data: {e}"]

        return jsonify({
            "input_symptoms": symptoms,
            "diagnosis_results": all_diagnoses
        })

    except Exception as e:
        return jsonify({"error": f"Unexpected server error: {e}"}), 500

if __name__ == '__main__':
    print("Fetching symptom data from OpenFDA...")
    cached_symptoms = fetch_symptoms()
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 5000)), debug=True)
