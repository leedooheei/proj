from flask import Flask, request, jsonify
from flask_cors import CORS
from datetime import datetime

app = Flask(__name__)
CORS(app) 

orders = [] 

@app.route('/orders', methods=['GET'])
def get_orders():
    return jsonify(orders)

@app.route('/orders', methods=['POST'])
def receive_order():
    order_data = request.get_json()

    if order_data:
        order_data['order_time'] = datetime.now().strftime('%H:%M:%S')  # 현재 시간을 주문 데이터에 추가
        for item in order_data['cart']:
            item['price'] = float(item['price'])  
        orders.append(order_data)  
        return jsonify({'message': '주문이 성공적으로 접수되었습니다.'}), 200
    else:
        return jsonify({'error': '주문 데이터가 없습니다.'}), 400

if __name__ == '__main__':
    app.run(debug=True)
