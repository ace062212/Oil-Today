#!/bin/bash

# 사용자 이름과 이메일 설정
echo "깃허브 사용자 이름을 입력하세요:"
read username
echo "깃허브 이메일을 입력하세요:"
read email

# 저장소 이름 설정 (기본값: oil-today)
echo "저장소 이름을 입력하세요 (기본값: oil-today):"
read repo_name
repo_name=${repo_name:-oil-today}

# Git 초기화
git init

# Git 사용자 정보 설정
git config user.name "$username"
git config user.email "$email"

# 모든 파일 추가
git add .

# 초기 커밋
git commit -m "초기 프로젝트 구조 설정"

# 원격 저장소 생성 안내
echo "Github에서 '$repo_name' 저장소를 먼저 생성해주세요."
echo "저장소 생성 후 아무 키나 누르세요..."
read -n 1

# 원격 저장소 추가
git remote add origin "https://github.com/$username/$repo_name.git"

# 푸시
git push -u origin master || git push -u origin main

echo "깃허브 업로드가 완료되었습니다."
echo "저장소 URL: https://github.com/$username/$repo_name" 