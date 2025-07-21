from flask import Flask, render_template, request
import pandas as pd

app = Flask(__name__)

# Load your dataset
data = pd.read_csv('data/restaurant_data.csv')

@app.route('/')
def index():
    cities = sorted(data['City'].dropna().astype(str).unique().tolist())
    cuisines = sorted(data['Cuisine'].dropna().astype(str).unique().tolist())
    return render_template('index.html', cities=cities, cuisines=cuisines)

@app.route('/predict', methods=['POST'])
def predict():
    city = request.form['city']
    cuisine = request.form['cuisine']
    food_item = request.form['food_item']
    max_distance = float(request.form['max_distance'])

    # Filter based on inputs
    data['City'] = data['City'].astype(str)
    data['Cuisine'] = data['Cuisine'].astype(str)
    data['Food_Item'] = data['Food_Item'].astype(str)
    filtered = data[
    (data['City'].str.lower() == city.lower()) &
    (data['Cuisine'].str.lower() == cuisine.lower()) &
    (data['Food_Item'].str.lower() == food_item.lower()) &
    (data['Estimated_Distance_km'] <= max_distance)
    ]

    if not filtered.empty:
        top_restaurants = filtered.sort_values(by='Rating', ascending=False).head(3)

        results = []
        for _, row in top_restaurants.iterrows():
            maps_url = f"https://www.google.com/maps/search/?api=1&query={row['Restaurant_Name'].replace(' ', '+')}+{row['Address'].replace(' ', '+')}+{row['City'].replace(' ', '+')}"
            row_data = row.to_dict()
            row_data['maps_url'] = maps_url
            results.append(row_data)

        return render_template('result.html', results=results)
    else:
        return render_template('result.html', error="No matching restaurants found.")

if __name__ == '__main__':
    app.run(debug=True)
