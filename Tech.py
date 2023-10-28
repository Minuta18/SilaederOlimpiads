from flask import Flask, render_template

app = Flask('Main')

@app.route('/')
def index():
    return render_template('init/Tech.html')

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=11601)