from flask import Flask, render_template, request, jsonify
from core.manager import TaskManager

app = Flask(__name__)
manager = TaskManager(storage_path="data/tasks.json")

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/api/tasks", methods=["GET"])
def get_tasks():
    status = request.args.get("status")
    priority = request.args.get("priority")
    category = request.args.get("category")
    search = request.args.get("search")
    sort_by = request.args.get("sort_by", "created_desc")

    tasks = manager.get_all(
        status=status,
        priority=priority,
        category=category,
        search=search,
        sort_by=sort_by
    )
    return jsonify([t.to_dict() for t in tasks])

@app.route("/api/tasks", methods=["POST"])
def create_task():
    data = request.get_json() or {}
    title = data.get("title")
    if not title or not title.strip():
        return jsonify({"error": "Title is required"}), 400

    task = manager.add_task(
        title=title,
        description=data.get("description", ""),
        priority=data.get("priority", "Medium"),
        category=data.get("category", "General"),
        due_date=data.get("due_date")
    )
    return jsonify(task.to_dict()), 201

@app.route("/api/tasks/<task_id>", methods=["PUT"])
def update_task(task_id):
    data = request.get_json() or {}
    try:
        updated = manager.update_task(task_id, data)
        if not updated:
            return jsonify({"error": "Task not found"}), 404
        return jsonify(updated.to_dict())
    except ValueError as e:
        return jsonify({"error": str(e)}), 400

@app.route("/api/tasks/<task_id>/toggle", methods=["PATCH"])
def toggle_task(task_id):
    toggled = manager.toggle_task(task_id)
    if not toggled:
        return jsonify({"error": "Task not found"}), 404
    return jsonify(toggled.to_dict())

@app.route("/api/tasks/<task_id>", methods=["DELETE"])
def delete_task(task_id):
    success = manager.delete_task(task_id)
    if not success:
        return jsonify({"error": "Task not found"}), 404
    return jsonify({"success": True})

@app.route("/api/tasks/clear-completed", methods=["POST"])
def clear_completed():
    count = manager.clear_completed()
    return jsonify({"cleared_count": count})

@app.route("/api/stats", methods=["GET"])
def get_stats():
    return jsonify(manager.get_stats())

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8080, debug=True)
