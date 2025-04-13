async function getCurrentLocation() {
    return new Promise((resolve, reject) => {
        if (!navigator.geolocation) {
            reject(new Error('Geolocation is not supported by your browser'));
        }

        navigator.geolocation.getCurrentPosition(
            (position) => {
                resolve({
                    lat: position.coords.latitude,
                    lng: position.coords.longitude
                });
            },
            (error) => {
                reject(error);
            }
        );
    });
}

async function loadStationData() {
    try {
        // 현재 위치 가져오기
        const position = await getCurrentLocation();
        
        // Flask 서버로 위치 정보와 함께 요청 보내기
        const response = await fetch('/api/stations', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(position)
        });
        
        return await response.json();
    } catch (error) {
        console.error('Error:', error);
        return [];
    }
}