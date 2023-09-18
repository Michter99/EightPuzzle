from flask import Flask, render_template, request, jsonify
from flask_cors import CORS  # Import the CORS library
from puzzle_a_estrella import PuzzleAEstrella

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/solve", methods=["POST"])
def solve():
    data = request.get_json()
    initialState = data.get("initialState")
    finalState = data.get("finalState")

    solver = PuzzleAEstrella()
    solution_found, solution_steps = solver.solve_8_puzzle(initialState, finalState)

    if solution_found:
        return jsonify({"message": "Solution found", "solution": solution_steps})
    else:
        return jsonify({"message": "No solution found"}), 400


if __name__ == "__main__":
    app.run(debug=True)
