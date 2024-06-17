from flask import Flask, request, jsonify
import json
import os

app = Flask(__name__)

# 파일 업로드 폴더 설정
UPLOAD_FOLDER = 'uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

@app.route('/upload', methods=['POST'])
def upload_order():
    order_data = request.get_json()
    if not order_data:
        return jsonify({'message': 'No order data provided'}), 400

    order_number = order_data['order_number']
    total_price = order_data['total_price']
    eat_where = order_data['EatWhere']
    payment_method = order_data['payment_method']
    cart = order_data['cart']

    # 여기에 주문 데이터를 데이터베이스에 저장하는 코드를 추가할 수 있습니다.
    # 예를 들어, JSON 파일로 저장하는 방법은 다음과 같습니다.
    order_file = os.path.join(UPLOAD_FOLDER, f'order_{order_number}.json')
    with open(order_file, 'w') as f:
        json.dump(order_data, f)

    return jsonify({'message': 'Order successfully received', 'order_number': order_number}), 200

if __name__ == '__main__':
    app.run(debug=True)
