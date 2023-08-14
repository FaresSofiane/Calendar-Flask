from flask import Flask, render_template, jsonify, request

app = Flask(__name__)


@app.route('/')
def calendar():
    return render_template('calendar.html')

@app.route('/events', methods=['GET', 'POST'])
def get_events():
    global events

    if request.method == 'POST':
        events = request.get_json()
        return jsonify(success=True)

    return jsonify(events)

if __name__ == '__main__':
    app.run(debug=True)
