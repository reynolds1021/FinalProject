from app import app
from flask import render_template






@app.route('/')
def index(): #Changed to /quantum

    return render_template('index.html')

"""
Intro to quantum routes:
"""  

@app.route('/quantum') #Why Quantum?
def quantum():
    return render_template('quantum.html') 

@app.route('/quantbkgrd') #Quantum background
def quantbkgrd():
    return render_template('quantum_background.html')

@app.route('/quantbasics') #Quantum components
def quantbasics():
    return render_template('quantum_components.html')

@app.route('/quantalgorithms') #Quantum algorithms
def quantalgorithms():
    return render_template('quantum_algorithms.html')

@app.route('/quantvsclass') #Quantum vs. classical
def quantvsclass():
    return render_template('quantum_challenges.html')


@app.route('/quantfuture') #Quantum future
def quantfuture():
    return render_template('quantum_future.html') 

"""
Quantum finance routes:
"""     

@app.route('/quantumfinance') #Quantum Finance
def quantumfinance():
    return render_template('quantum_finance.html') 

@app.route('/bsbkgrd') #Black Scholes Background
def bsbkgrd():
    return render_template('bs_background.html')

@app.route('/bsmotiv') #Black Scholes Motivation
def bsmotiv():
    return render_template('bs_motivation.html')

@app.route('/bsquantmodel') #Black Scholes Quantum Model
def bsquantmodel():
    return render_template('bs_quantummodel.html')


@app.route('/bsresults') #BS Quantum Results
def bsresults():
    return render_template('bs_results.html') 

@app.route('/bsconc') #BS Quantum Conclusion
def bsconc():
    return render_template('bs_conc.html') 

"""
Quantum database routes:
"""      

@app.route('/quantumdb') #Quantum Database
def quantumdb():
    return render_template('quantum_db.html') 


@app.route('/quantdbbkgrd') #Quantum DB Background
def quantdbbkgrd():
    return render_template('quantum_db_background.html') 

@app.route('/quantdbmotiv') #Quantum DB Motivation
def quantdbmotiv():
    return render_template('quantum_db_motivation.html')  

@app.route('/quantdbmodel') #DB Quantum Model
def quantdbmodel():
    return render_template('quantum_db_model.html') 

@app.route('/quantdbresults') #DB Quantum Results
def quantdbresults():
    return render_template('quantum_db_results.html') 

@app.route('/quantdbconc') #DB Quantum Conclusion
def quantdbconc():
    return render_template('quantum_db_conc.html') 

 
