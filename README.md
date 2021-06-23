## rabbitMQ 웹 관리자 등록방법
* rabbitmqctl add_user test test
* rabbitmqctl set_user_tags test administrator
* rabbitmqctl set_permissions -p / test ".*" ".*" ".*"

## putty 
* synerex
* DB
* mysql -u root -p
* show databases;
* use test;
* show tables;
* select * from 테이블명(rawdata_chung)
* 끝내기 ctrl+c
* desc device / user / building ;

## 실행하기
* d: cd desktop/융캡_오이칠이/5272_project/venv/Scripts && activate.bat && cd .. && cd ..
* pip install -r requirements.txt
* cd flask_code && flask run
* -> 로컬 http://127.0.0.1:5000/login
* -> 서버 http://211.62.179.66:3000/login
