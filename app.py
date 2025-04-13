from flask import Flask, request, jsonify
import json
import subprocess
from oil_data_7day import get_oil_data

app = Flask(__name__)

@app.route('/')
def home():
    return app.send_static_file('diesel.html')

@app.route('/save_location', methods=['POST'])
def save_location():
    location_data = request.json
    
    # 위치 정보를 임시 파일에 저장
    with open('current_location.json', 'w') as f:
        json.dump(location_data, f)
    
    return jsonify({"status": "success"})

@app.route('/update_oil_data')
def update_oil_data():
    try:
        # 저장된 위치 정보 읽기
        with open('current_location.json', 'r') as f:
            location = json.load(f)
            
        # oil_data.py 실행
        get_oil_data(location['lat'], location['lng'])
        
        return jsonify({"status": "success"})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})

if __name__ == '__main__':
    app.run(debug=True)