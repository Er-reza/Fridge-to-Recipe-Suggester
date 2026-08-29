from flask import Flask, request, render_template

app = Flask(__name__)

# Simple recipe database
recipes = {
    "Tomato Rice": ["tomato", "rice", "onion"],
    "Egg Curry": ["egg", "tomato", "onion"],
    "Aloo Paratha": ["potato", "flour", "salt"],
    "Vegetable Soup": ["carrot", "tomato", "onion", "beans"]
}

@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        # Get user input
        ingredients = request.form["ingredients"].lower().split(",")
        ingredients = [i.strip() for i in ingredients]

        matched = []
        suggestions = []

        for name, req in recipes.items():
            # Exact match (all ingredients present)
            if all(item in ingredients for item in req):
                matched.append(name)
            # Partial match (at least one ingredient present)
            elif any(item in ingredients for item in req):
                suggestions.append(name)

        return render_template("results.html",
                               recipes=matched,
                               suggestions=suggestions,
                               ingredients=ingredients)

    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)
<!DOCTYPE html>
<html>
<head>
    <title>Fridge-to-Recipe Suggester</title>
</head>
<body>
    <h1>Fridge-to-Recipe Suggester</h1>
    <form method="POST">
        <label>Enter ingredients (comma separated):</label><br>
        <input type="text" name="ingredients" placeholder="e.g. tomato, rice, onion">
        <button type="submit">Find Recipes</button>
    </form>
</body>
</html>
<!DOCTYPE html>
<html>
<head>
    <title>Recipe Results</title>
</head>
<body>
    <h1>Recipes you can cook</h1>
    <p>With your ingredients: {{ ingredients }}</p>

    {% if recipes %}
        <h2>Exact matches:</h2>
        <ul>
        {% for recipe in recipes %}
            <li>{{ recipe }}</li>
        {% endfor %}
        </ul>
    {% else %}
        <h2>No exact recipe found.</h2>
        <p>But here are some dishes you can try with what you have:</p>
        <ul>
        {% for suggestion in suggestions %}
            <li>{{ suggestion }}</li>
        {% endfor %}
        </ul>
    {% endif %}

    <a href="/">Try again</a>
</body>
</html>
