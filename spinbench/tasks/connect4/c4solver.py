from flask import Flask, request, jsonify
import subprocess
import argparse

app = Flask(__name__)

SOLVER_PATH = "./c4solver"

@app.route('/solve', methods=['GET'])
def analyze_position():
    pos = request.args.get('pos')
    if not pos:
        return jsonify({"pos":"","score":[-2,-1,0,1,0,-1,-2]})

    input_data = pos + "\n"

    try:
        process = subprocess.Popen(
            [SOLVER_PATH, "-a"],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            bufsize=1
        )
    except Exception as e:
        return jsonify({"error": str(e)}), 500

    try:
        process.stdin.write(input_data)
        process.stdin.flush()

        line = process.stdout.readline()
        print(line)
        parts = line.split()
        if len(parts) < 2:
            return jsonify({"error": "No scores found in output"}), 500

        try:
            scores = list(map(int, parts[1:]))
        except ValueError:
            return jsonify({"error": "Failed to parse scores"}), 500

    finally:
        process.kill()
        process.wait()

    return jsonify({"pos": input_data.replace("\n",""), "score": scores})

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="connect 4 solver server")
    parser.add_argument('--port', type=int, default=5000, help="Port to run the server on")
    args = parser.parse_args()
    # Start the Flask server
    app.run(host='0.0.0.0', port=args.port)
