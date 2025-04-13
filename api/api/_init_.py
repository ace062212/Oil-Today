# api/opinet.py

import requests
import json
from datetime import datetime

class OpinetAPI:
    def __init__(self, api_key="F241014357"):
        self.api_key = api_key
        self.base_url = "http://www.opinet.co.kr/api"
    
    def request_api(self, endpoint, params):
        """API 요청을 보내는 기본 메서드"""
        try:
            url = f"{self.base_url}/{endpoint}"
            params['code'] = self.api_key
            params['out'] = 'json'
            
            response = requests.get(url, params=params)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.HTTPError as http_err:
            print(f"HTTP 에러 발생: {http_err}")
        except Exception as err:
            print(f"기타 에러 발생: {err}")
        return None

    def get_stations_by_location(self, x, y, radius=1000, prod_cd="D047"):
        """위치 기반으로 주변 주유소 검색"""
        endpoint = "aroundAll.do"
        params = {
            "x": x,
            "y": y,
            "radius": radius,
            "prodcd": prod_cd,
            "sort": "1"  # 1: 가격순, 2: 거리순
        }

        data = self.request_api(endpoint, params)
        if data and "RESULT" in data:
            stations = data["RESULT"].get("OIL", [])
            return self._process_station_data(stations)
        return []

    def _process_station_data(self, stations):
        """주유소 데이터 처리 및 포맷팅"""
        processed_data = []
        for station in stations:
            processed_data.append({
                "id": station.get("UNI_ID", ""),
                "name": station.get("OS_NM", ""),
                "price": int(station.get("PRICE", 0)),
                "distance": float(station.get("DISTANCE", 0)),
                "lat": float(station.get("GIS_Y_COOR", 0)),
                "lng": float(station.get("GIS_X_COOR", 0)),
                "brand": station.get("POLL_DIV_CD", ""),
                "timestamp": datetime.now().isoformat()
            })
        return processed_data

    def save_to_json(self, data, filename="data/oil_prices.json"):
        """데이터를 JSON 파일로 저장"""
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            print(f"데이터가 {filename}에 저장되었습니다.")
        except Exception as e:
            print(f"파일 저장 중 오류 발생: {e}")