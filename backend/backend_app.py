from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # This will enable CORS for all routes

POSTS = [
    {"id": 1, "title": "First post", "content": "This is the first post."},
    {"id": 2, "title": "Second post", "content": "This is the second post."},
]


@app.route('/api/posts', methods=['GET', 'POST'])
def handle_posts():
    if request.method == 'POST':
        data = request.get_json(silent=True) or request.form
        title = (data.get('title') or '').strip()
        content = (data.get('content') or '').strip()

        if not title or not content:
            return jsonify({"error": "Title and content are required"}), 400

        new_id = max((post['id'] for post in POSTS), default=0) + 1
        new_post = {"id": new_id, "title": title, "content": content}
        POSTS.append(new_post)

        return jsonify(new_post), 201

    # GET
    return jsonify(POSTS)
if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5002, debug=True)
