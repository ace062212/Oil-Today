import requests
import json
from pathlib import Path

# API 키 설정
api_key = "F241014357"

def request_api(url, params):
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        print(f"API 응답: {response.text}")  # 디버깅용 응답 출력
        return response.json()
    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP 에러 발생: {http_err}")
    except Exception as err:
        print(f"기타 에러 발생: {err}")
    return None

def search_stations_within_radius():
    url = "http://www.opinet.co.kr/api/aroundAll.do"
    all_data = []

    # 제품 구분 
    prodcd_options = {
        "B027": "휘발유",
        "D047": "경유", 
        "B034": "고급휘발유",
        "K015": "자동차부탄"
    }

    # API 문서의 예시 좌표 사용
    x = "314681.8"
    y = "544837"

    for prodcd, prodcd_name in prodcd_options.items():
        params = {
            "code": api_key,
            "out": "json",  # JSON 형식으로 요청
            "x": x,
            "y": y,
            "radius": "5000",  # 반경 5km
            "prodcd": prodcd,
            "sort": "1"  # 가격순
        }

        print(f"\n요청 URL: {url}?code={api_key}&x={x}&y={y}&radius=5000&sort=1&prodcd={prodcd}&out=json")
        print(f"요청 파라미터: {params}")
        
        data = request_api(url, params)
        if data and "RESULT" in data and "OIL" in data["RESULT"]:
            stations = data["RESULT"]["OIL"]
            
            print(f"\n[제품: {prodcd_name}, 정렬 기준: 가격순]")
            print(json.dumps(stations, indent=4, ensure_ascii=False))
            
            for station in stations:
                station_data = {
                    "product": prodcd_name,
                    "station_id": station.get("UNI_ID", ""),
                    "station_name": station.get("OS_NM", ""),
                    "price": station.get("PRICE", ""),
                    "distance": station.get("DISTANCE", ""),
                    "gis_x": station.get("GIS_X_COOR", ""),
                    "gis_y": station.get("GIS_Y_COOR", "")
                }
                all_data.append(station_data)
        else:
            print(f"\n[제품: {prodcd_name}] - 데이터를 가져오는 데 실패했습니다.")

    # JSON 파일로 저장
    save_path = Path("data/station_prices.json")
    save_path.parent.mkdir(parents=True, exist_ok=True)
    
    with open(save_path, "w", encoding="utf-8") as f:
        json.dump(all_data, f, ensure_ascii=False, indent=2)
        
    print(f"\n데이터가 저장되었습니다: {save_path}")

def main():
    search_stations_within_radius()

if __name__ == "__main__":
    main()