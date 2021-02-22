from flask import Flask, render_template
from dataframes.summary import summmary
import numpy as np

app = Flask(__name__)

total= np.array(summmary())

print(total)

@app.route('/')
def hello_world():
   return render_template('index.html',prabesh=total)



if __name__ == '__main__':
   app.run(debug=True)