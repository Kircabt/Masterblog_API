from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_swagger_ui import get_swaggerui_blueprint

app = Flask(__name__)
CORS(app)  # This will enable CORS for all routes

POSTS = [
    {"id": 1, "title": "First post", "content": "This is the first post."},
    {"id": 2, "title": "Second post", "content": "This is the second post."},
]

SWAGGER_URL="/api/docs"  # (1) swagger endpoint e.g. HTTP://localhost:5002/api/docs
API_URL="/static/masterblog.json" # (2) ensure you create this dir and file

swagger_ui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={
        'app_name': 'Masterblog API' # (3) You can change this if you like
    }
)
app.register_blueprint(swagger_ui_blueprint, url_prefix=SWAGGER_URL)


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


    # GET: optional sorting
    sort_field = request.args.get('sort')
    direction = request.args.get('direction', 'asc').lower()

    if sort_field is None:
        return jsonify(POSTS)

    if sort_field not in ('title', 'content'):
        return jsonify({"error": "Invalid sort field. Use 'title' or 'content'."}), 400

    if direction not in ('asc', 'desc'):
        return jsonify({"error": "Invalid direction. Use 'asc' or 'desc'."}), 400

    sorted_posts = sorted(
        POSTS,
        key=lambda post: post[sort_field].lower(),
        reverse=(direction == 'desc'),
    )

    return jsonify(sorted_posts)

@app.route('/api/posts/<int:id>', methods=['DELETE'])
def delete(id):
    post = next((p for p in POSTS if p['id'] == id), None)

    if post is None:
        return jsonify({"error": f"Post with id {id} was not found."}), 404

    POSTS.remove(post)

    return jsonify({"message": f"Post with id {id} has been deleted successfully."}), 200

@app.route('/api/posts/<int:id>', methods=['PUT'])
def update(id):
    #checking if the post with the given ID exist
    post = next((p for p in POSTS if p['id'] == id), None)
    if post is None:
        return jsonify({"error": f"Post with id {id} was not found."}), 404

    data = request.get_json(silent=True) or request.form

    new_title = post['title']
    new_content = post['content']

    if 'title' in data:
        new_title = (data.get('title') or '').strip()
    if 'content' in data:
        new_content = (data.get('content') or '').strip()

    if not new_title and not new_content:
        return jsonify({"error": "Title and content cannot be empty"}), 400

    post['title'] = new_title
    post['content'] = new_content
    return jsonify(post), 200

    return jsonify(post), 200


@app.route('/api/posts/search', methods=['GET'])
def search():
    title_query = (request.args.get('title') or '').strip().lower()
    content_query = (request.args.get('content') or '').strip().lower()

    results = [
        post for post in POSTS
        if (title_query and title_query in post['title'].lower())
           or (content_query and content_query in post['content'].lower())
    ]

    return jsonify(results)



if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5002, debug=True)
