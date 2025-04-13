import requests
import pandas as pd
from pathlib import Path
import os

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
            df_sido = pd.DataFrame(data['RESULT']['OIL'])
            return df_sido
        else:
            print(f"에러 발생: {response.status_code}")
            return None
    except Exception as e:
        print(f"요청 실패: {str(e)}")
        return None

def get_opinet_area_data(api_key):
    all_area_data = []
    sido_list = get_sido_list(api_key)
    
    if sido_list is not None:
        for _, row in sido_list.iterrows():
            base_url = "http://www.opinet.co.kr/api/avgSidoPrice.do"
            params = {
                'code': api_key,
                'out': 'json',
                'sido': row['AREA_CD'],
                'prodcd': 'B027'  # B027은 휘발유 제품 코드
            }
            
            try:
                print(f"{row['AREA_NM']} 데이터 수집 중...")
                response = requests.get(base_url, params=params)
                if response.status_code == 200:
                    data = response.json()
                    if 'RESULT' in data and 'OIL' in data['RESULT']:
                        df_temp = pd.DataFrame(data['RESULT']['OIL'])
                        df_temp['AREA_NM'] = row['AREA_NM']  # 지역명 추가
                        all_area_data.append(df_temp)
            except Exception as e:
                print(f"{row['AREA_NM']} 데이터 수집 실패: {str(e)}")
                continue
    
    if all_area_data:
        return pd.concat(all_area_data, ignore_index=True)
    return None

def main():
    # API 키 설정
    api_key = 'F241106421'
    
    # 데이터 수집
    df_all = get_opinet_area_data(api_key)

    if df_all is not None:
        # 현재 스크립트의 디렉토리 경로 가져오기
        current_dir = os.path.dirname(os.path.abspath(__file__))
        
        # 데이터 저장 경로 설정
        save_path = os.path.join(current_dir, 'data', 'gasoline_prices_sido.json')
        
        # 디렉토리가 없으면 생성
        os.makedirs(os.path.dirname(save_path), exist_ok=True)
        
        # JSON 파일로 저장
        df_all.to_json(save_path, orient='records', force_ascii=False, indent=2)
        print(f"\n데이터가 저장되었습니다: {save_path}")
        
        # 데이터 기본 정보 출력
        print("\n수집된 데이터 건수:", len(df_all))
        print("포함된 지역 수:", df_all['AREA_NM'].nunique())
    else:
        print("데이터 수집에 실패했습니다.")

if __name__ == "__main__":
    main()