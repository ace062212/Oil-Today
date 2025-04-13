#!/usr/bin/env python3
import requests
import json
from pathlib import Path
import logging
from datetime import datetime

# 로깅 설정
logging.basicConfig(
    filename='oil_prices_update.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def get_sido_list(api_key):
    base_url = "http://www.opinet.co.kr/api/areaCode.do"
    params = {
        'code': api_key,
        'out': 'json'
    }
    
    try:
        response = requests.get(base_url, params=params)
        if response.status_code == 200:
            data = response.json()
            return data['RESULT']['OIL']
        else:
            logging.error(f"에러 발생: {response.status_code}")
            return None
    except Exception as e:
        logging.error(f"요청 실패: {str(e)}")
        return None

def get_opinet_area_data(api_key):
    all_area_data = []
    sido_list = get_sido_list(api_key)
    
    if sido_list is not None:
        for area in sido_list:
            base_url = "http://www.opinet.co.kr/api/avgSidoPrice.do"
            params = {
                'code': api_key,
                'out': 'json',
                'sido': area['AREA_CD']
            }
            
            try:
                logging.info(f"{area['AREA_NM']} 데이터 수집 중...")
                response = requests.get(base_url, params=params)
                if response.status_code == 200:
                    data = response.json()
                    if 'RESULT' in data and 'OIL' in data['RESULT']:
                        for oil in data['RESULT']['OIL']:
                            oil['AREA_NM'] = area['AREA_NM']
                        all_area_data.extend(data['RESULT']['OIL'])
            except Exception as e:
                logging.error(f"{area['AREA_NM']} 데이터 수집 실패: {str(e)}")
                continue
    
    return all_area_data if all_area_data else None

def update_oil_prices():
    try:
        api_key = 'F241106421'
        data = get_opinet_area_data(api_key)
        
        if data is not None:
            # 데이터에 업데이트 시간 추가
            current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            for item in data:
                item['UPDATE_TIME'] = current_time
            
            # JSON 파일로 저장
            save_path = Path('data/oil_prices_sido.json')
            save_path.parent.mkdir(parents=True, exist_ok=True)
            
            with open(save_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            
            logging.info(f"데이터 업데이트 성공 - 레코드 수: {len(data)}")
        else:
            logging.error("데이터 수집 실패")
            
    except Exception as e:
        logging.error(f"오류 발생: {str(e)}")

if __name__ == "__main__":
    update_oil_prices()