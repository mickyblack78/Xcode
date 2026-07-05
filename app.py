from flask import Flask, request, jsonify
from flask_cors import CORS
import tinytuya

app = Flask(__name__)
CORS(app) 

# --- DEVICE STORAGE REGISTER ---
DEVICES = {
    "bench_light": {"id": "ID_HERE", "ip": "192.168.1.X", "key": "KEY_HERE", "version": 3.3},
    "garage_light": {"id": "ID_HERE", "ip": "192.168.1.Y", "key": "KEY_HERE", "version": 3.3}
}

@app.route('/control', methods=['POST'])
def control():
    data = request.json
    name = data.get("device")
    action = data.get("action")
    
    if name not in DEVICES:
        return jsonify({"status": "error"}), 400
        
    info = DEVICES[name]
    try:
        device = tinytuya.BulbDevice(info['id'], info['ip'], info['key'])
        device.set_version(info['version'])
        if action == "on":
            device.turn_on()
        elif action == "off":
            device.turn_off()
        return jsonify({"status": "success"})
    except Exception as e:
        return jsonify({"status": "error", "msg": str(e)}), 500

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000)
