from flask import Flask, jsonify, render_template, request, session, g, redirect, url_for, flash
from flask_bootstrap import Bootstrap
import dbus

app = Flask(__name__)    
Bootstrap(app)

app.config['BOOTSTRAP_SERVE_LOCAL'] = True
app.config['SECRET_KEY'] = 'ccwduihcwqaucbh2w98d21g39i1bdcouxd2hg932wqbcwr8webhccqy'

@app.route('/aggiungi_rimuovi_estratto')
def add_remove():
    num = request.args.get('num', 0, type=int)
    try:
        bus = dbus.SystemBus()
        remote_object = bus.get_object("it.parrocchiasangiacomobianchi.tombolone", "/")
        remote_object.aggiungiOEliminaEstratto(str(num), dbus_interface = "it.parrocchiasangiacomobianchi.Interface")
    except dbus.DBusException:
        pass
    return jsonify(result='OK')

@app.route('/vittoria')
def vittoria():
    tipo = request.args.get('tipo','')
    try:
        bus = dbus.SystemBus()
        remote_object = bus.get_object("it.parrocchiasangiacomobianchi.tombolone", "/")
        remote_object.vittoria(str(tipo), dbus_interface = "it.parrocchiasangiacomobianchi.Interface")
    except dbus.DBusException:
        pass
    return jsonify(result='OK')


@app.route('/ricomincia')
def ricomincia():
    try:
        bus = dbus.SystemBus()
        remote_object = bus.get_object("it.parrocchiasangiacomobianchi.tombolone", "/")
        remote_object.ricominciaGioco(dbus_interface = "it.parrocchiasangiacomobianchi.Interface")
    except dbus.DBusException:
        pass
    return redirect(url_for('index'))


@app.route('/get_estratti')
def get_estratti():
    try:
        bus = dbus.SystemBus()
        remote_object = bus.get_object("it.parrocchiasangiacomobianchi.tombolone", "/")
        lista_numeri = remote_object.get_estratti(dbus_interface = "it.parrocchiasangiacomobianchi.Interface")
    except dbus.DBusException:
        pass   
    return jsonify(numeri=lista_numeri)

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0")
