import os
import time
import logging

import psycopg2
from flask import Flask, jsonify
from psycopg2.extras import RealDictCursor

app = Flask(__name__)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

DB_HOST = os.getenv("DB_HOST", "database")
DB_PORT = os.getenv("DB_PORT", "5432")
DB_NAME = os.getenv("DB_NAME", "devops_store")
DB_USER = os.getenv("DB_USER", "storeuser")
DB_PASSWORD = os.getenv("DB_PASSWORD", "storepass123")


def get_db_connection():
    retries = 5

    for attempt in range(retries):
        try:
            return psycopg2.connect(
                host=DB_HOST,
                port=DB_PORT,
                database=DB_NAME,
                user=DB_USER,
                password=DB_PASSWORD,
                connect_timeout=5,
            )
        except psycopg2.OperationalError:
            logger.exception(
                "Database connection failed (attempt %s/%s)",
                attempt + 1,
                retries,
            )

            if attempt == retries - 1:
                raise

            time.sleep(3)


@app.route("/health", methods=["GET"])
def health():
    return jsonify({
        "status": "healthy",
        "service": "review-service",
        "version": "v3",
    }), 200


@app.route("/api/reviews", methods=["GET"])
def get_reviews():
    connection = None

    try:
        connection = get_db_connection()

        with connection.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute("""
                SELECT
                    r.id,
                    p.name AS product_name,
                    r.reviewer_name,
                    r.comment,
                    r.rating
                FROM reviews r
                JOIN products p ON r.product_id = p.id
                ORDER BY r.id;
            """)

            reviews = cursor.fetchall()

        return jsonify(reviews), 200

    except Exception:
        logger.exception("Failed to retrieve reviews")
        return jsonify({"error": "Unable to retrieve reviews"}), 500

    finally:
        if connection is not None:
            connection.close()


@app.route("/", methods=["GET"])
def home():
    return jsonify({
        "message": "DevOps Store Review Service",
        "version": "v3",
        "endpoints": ["/health", "/api/reviews"],
    }), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)