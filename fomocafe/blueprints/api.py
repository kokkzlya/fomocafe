import json
import os
import sqlite3
from datetime import UTC, datetime

import shortuuid
from pydantic.json import pydantic_encoder
from flask import Blueprint, Response, jsonify, request, send_from_directory
from werkzeug.utils import secure_filename

from fomocafe.models import Product, User

p = os.path.dirname
UPLOAD_FOLDER = p(p(p(__file__))) + "/images/products"
ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "gif"}

bp = Blueprint("api", __name__)


@bp.route("/register", methods=["POST"])
def register():
    data = request.get_json()
    user = User(
        id=shortuuid.uuid(),
        name=data["name"],
        email=data["email"],
        username=data["username"],
        password=data["password"],
        created=datetime.now(UTC),
        updated=datetime.now(UTC),
    )
    with sqlite3.connect("database.db") as conn:
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO users (id, name, email, username, password, created, updated) "
            "VALUES (?, ?, ?, ?, ?, ?, ?)",
            (
                user.id, user.name, user.email,
                user.username, user.password,
                user.created, user.updated,
            ),
        )
    return jsonify({
        "id": user.id,
        "name": user.name,
        "email": user.email,
        "username": user.username,
        "created": user.created,
        "updated": user.updated,
    }), 201


@bp.route("/login", methods=["POST"])
def login():
    return "", 200


@bp.route("/logout", methods=["POST"])
def logout():
    pass


@bp.route("/products", methods=["GET"])
def fetch_products():
    conn = sqlite3.connect("database.db")
    cur = conn.cursor()
    cur.execute(
        "SELECT "
        "id, name, description, category, price, stock, image_url, created, updated "
        "FROM products",
    )
    products = []
    for row in cur.fetchall():
        product = Product(
            id=row[0],
            name=row[1],
            description=row[2],
            category=row[3],
            price=row[4],
            stock=row[5],
            image_url=row[6],
            created=row[7],
            updated=row[8],
        )
        products.append(product)

    return Response(
        json.dumps(products, default=pydantic_encoder),
        status=200,
        headers={"Content-Type": "application/json"},
    )


@bp.route("/products", methods=["POST"])
def create_product():
    data = request.get_json()
    product_id = shortuuid.uuid()
    product = Product(
        id=product_id,
        name=data["name"],
        description=data["description"],
        category=data["category"],
        price=data["price"],
        stock=data["stock"],
        image_url=None,
        created=datetime.now(UTC),
        updated=datetime.now(UTC),
    )
    with sqlite3.connect("database.db") as conn:
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO products ("
            "id, name, description, category, price, stock, image_url, created, updated"
            ") "
            "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
            (
                product.id, product.name, product.description,
                product.category, product.price, product.stock,
                product.image_url, product.created, product.updated,
            ),
        )

    return jsonify({
        "id": product.id,
        "name": product.name,
        "description": product.description,
        "category": product.category,
        "price": product.price,
        "stock": product.stock,
        "image_url": product.image_url,
        "created": product.created,
        "updated": product.updated,
    }), 201


@bp.route("/products/<product_id>", methods=["GET"])
def fetch_product(product_id):
    conn = sqlite3.connect("database.db")
    cur = conn.cursor()
    cur.execute(
        "SELECT "
        "id, name, description, category, price, stock, image_url, created, updated "
        "FROM products "
        "WHERE id = ?",
        (product_id,),
    )
    row = cur.fetchone()
    if row is None:
        return jsonify({"message": "Product not found"}), 404

    product = Product(
        id=row[0],
        name=row[1],
        description=row[2],
        category=row[3],
        price=row[4],
        stock=row[5],
        image_url=row[6],
        created=row[7],
        updated=row[8],
    )
    return jsonify({
        "id": product.id,
        "name": product.name,
        "description": product.description,
        "category": product.category,
        "price": product.price,
        "stock": product.stock,
        "image_url": product.image_url,
        "created": product.created,
        "updated": product.updated,
    }), 200


def allowed_file(filename):
    return "." in filename and \
           filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


@bp.route("/products/<product_id>/image", methods=["POST", "PATCH"])
def upload_product_image(product_id):
    if "file" not in request.files:
        return jsonify({"message": "No file part"}), 400
    file = request.files["file"]
    if file.filename == "":
        return jsonify({"message": "No selected file"}), 400

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(f"{UPLOAD_FOLDER}/{filename}")
        with sqlite3.connect("database.db") as conn:
            cur = conn.cursor()
            cur.execute(
                "UPDATE products SET image_url = ?, updated = ? WHERE id = ?",
                (f"/images/products/{filename}", datetime.now(UTC), product_id),
            )
        return jsonify({"message": "File uploaded"}), 201

    return jsonify({"message": "File part not allowed"}), 400


@bp.route("/images/products/<path:path>", methods=["GET"])
def get_product_image(path: str):
    return send_from_directory(UPLOAD_FOLDER, path)
