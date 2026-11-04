from flask import Flask, jsonify

app = Flask(__name__)

reviews = [
    {
        "id": 1,
        "product_id": 1,
        "customer": "Rahul",
        "rating": 5,
        "comment": "Excellent laptop!"
    },
    {
        "id": 2,
        "product_id": 2,
        "customer": "Priya",
        "rating": 4,
        "comment": "Good mobile, great battery."
    },
    {
        "id": 3,
        "product_id": 1,
        "customer": "Arjun",
        "rating": 5,
        "comment": "Very fast performance."
    }
]


@app.route("/api/reviews", methods=["GET"])
def get_reviews():
    return jsonify(reviews)


@app.route("/api/reviews/<int:review_id>", methods=["GET"])
def get_review(review_id):

    for review in reviews:
        if review["id"] == review_id:
            return jsonify(review)

    return jsonify({"error": "Review not found"}), 404


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)

