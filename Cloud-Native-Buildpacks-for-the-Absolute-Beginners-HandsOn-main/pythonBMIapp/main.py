# Import the necessary modules
from flask import Flask, request, render_template
from bmiCalculator import calculate_bmi

# Create a Flask app
app = Flask(__name__)

# Define the route and view function for the index page
@app.route('/')
def index():
    # Renders the index.html template.

    return render_template('index.html')

# Define the route and view function for the result page
@app.route('/result', methods=['POST'])
def result():
    # Calculates the user's BMI and health status, and renders the result.html template.

    # Get the user's height and weight from the request form
    height = float(request.form['height'])
    weight = float(request.form['weight'])

    # Calculate the user's BMI and health status
    bmi, health_status = calculate_bmi(height, weight)

    # Render the result.html template, passing in the user's BMI and health status
    return render_template('result.html', bmi=bmi, health_status=health_status)

# Start the Flask server
if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)
