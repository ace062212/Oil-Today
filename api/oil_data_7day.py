import requests
import json
from datetime import datetime
import os
def request_api(url, params):
    """API 요청 함수"""
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP 에러 발생: {http_err}")
    except Exception as err:
        print(f"기타 에러 발생: {err}")
    return None

def get_price_history_by_product():
    """유종별 최근 7일간의 전국 평균가격 조회"""
    api_key = "F241014357"
    url = "http://www.opinet.co.kr/api/avgRecentPrice.do"
    
    products = {
        "B027": "휘발유",
        "B034": "고급휘발유",
        "D047": "경유",
        "K015": "LPG"
    }
    
    price_history = {}
    
    for code, name in products.items():
        params = {
            "code": api_key,
            "out": "json",
            "prodcd": code
        }
        
        data = request_api(url, params)
        if data and "RESULT" in data:
            prices = []
            for item in data["RESULT"]["OIL"]:
                prices.append(float(item.get("PRICE", 0)))
            price_history[name] = prices
    
    return price_history

def get_oil_data():
    """7일간의 유종별 가격 데이터 수집 함수"""
    historical_prices = get_price_history_by_product()
    
    processed_data = {
        "historical_prices": historical_prices,
        "last_updated": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }

    # data 폴더 경로 설정
    data_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data')
    
    # data 폴더가 없으면 생성
    if not os.path.exists(data_dir):
        os.makedirs(data_dir)
    
    # data 폴더 안에 파일 저장
    file_path = os.path.join(data_dir, 'oil_prices_7day.json')
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(processed_data, f, ensure_ascii=False, indent=2)
        print(f"데이터가 {file_path}에 저장되었습니다.")
if __name__ == "__main__":
    get_oil_data()