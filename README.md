# 🏥 Healthcare Symptom Diagnosis and Treatment Options API

A Flask API that lets users:

- View all available symptoms
- See the top 5 most common symptoms
- Enter one or more symptoms and get associated medicinal products (using live OpenFDA data)

Built with production-ready error handling, caching, and clean JSON output.

---

## 🚀 Features

- **/symptoms** — List all reported symptoms
- **/top-symptoms** — View the top 5 most common symptoms
- **/diagnosis** — Submit 1 or more symptoms and get related drugs/medications
- Real-time data pulled from the **[OpenFDA API](https://open.fda.gov/apis/)**
- Clear and structured API responses
- Robust error handling for better user experience

---

## 📦 Installation

1. **Clone the repository**:

```bash
git clone https://github.com/your-username/healthcare-symptom-api.git
cd healthcare-symptom-api
```

2. **Create a virtual environment** (optional but recommended):

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install the dependencies**:

```bash
pip install -r requirements.txt
```

> If `requirements.txt` doesn't exist, simply install:

```bash
pip install flask requests
```

---

## ⚡ Usage

Start the Flask app:

```bash
python app.py
```

Server will start at:

```
http://localhost:5000/
```

---

## 🌐 Available API Endpoints

### `GET /`
- Welcome message and list of available endpoints.

---

### `GET /symptoms`
- Returns all unique symptoms (cached from OpenFDA on startup).

**Example response:**
```json
{
  "symptoms": [
    "headache",
    "nausea",
    "dizziness",
    ...
  ]
}
```

---

### `GET /top-symptoms`
- Returns the top 5 most frequently reported symptoms.

**Example response:**
```json
{
  "top_symptoms": [
    {"symptom": "headache", "count": 12},
    {"symptom": "nausea", "count": 10},
    ...
  ]
}
```

---

### `POST /diagnosis`
- Submit a JSON body containing one or more symptoms.
- Returns a list of associated medicinal products for each symptom.

**Request Body Example:**
```json
{
  "symptoms": ["nausea", "dizziness"]
}
```

**Response Example:**
```json
{
  "input_symptoms": ["nausea", "dizziness"],
  "diagnosis_results": {
    "nausea": ["ONDANSETRON", "ZOFRAN", "PHENERGAN"],
    "dizziness": ["MECLIZINE", "BONINE", "ANTIVERT"]
  }
}
```

---

## 📋 Example with cURL

```bash
curl -X POST http://localhost:5000/diagnosis \
  -H "Content-Type: application/json" \
  -d '{"symptoms": ["headache", "fatigue"]}'
```

---

## 🛠 Tech Stack

- Python
- Flask
- Requests
- OpenFDA API

---

## 🔥 Future Enhancements (Optional)

- Add basic authentication or API key security
- Deploy to cloud (e.g., AWS, Azure, Heroku)
- Create a simple front-end form for user input
- Add unit tests for key endpoints
- Cache popular symptom lookups to improve speed

---

## 👌 Acknowledgments

- [OpenFDA](https://open.fda.gov/apis/) — for providing open access to drug event data.
- Flask Community

---

## 📄 License

This project is licensed under the MIT License.

