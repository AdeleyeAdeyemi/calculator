from flask import Flask

app = Flask(__name__)

@app.route('/')
def score_service():
    try:
        with open("Scores.txt", "r") as score_file:
            content = score_file.read().strip()
            score = int(content)
            if 1 <= score <= 1000:
                return f"<h1 id='score'>{score}</h1>"
            else:
                return "<h1>Score out of valid range</h1>", 400
    except FileNotFoundError:
        return "<h1>Scores.txt file not found</h1>", 404
    except ValueError:
        return "<h1>Invalid score format (not a number)</h1>", 400
    except Exception as e:
        return f"<h1>Unexpected error: {str(e)}</h1>", 500
    
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8777, debug=True)




