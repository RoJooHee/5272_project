import json

from flask import Flask, render_template, request, flash, redirect, url_for, session, g
from device_data_dao import each_device_info
from model.user import User
from repo.user_repo import *  # USER repository
import building_data_dao
import device_list_dao
import device_data_dao
import weather
import box_plot



# Flask 객체 인스턴스 생성
app = Flask(__name__)
app.config['SECRET_KEY'] = 'abcd'  # 세션을 이용한 로그인 시스템을 만들기위해서 필요함

# 모든 요청에 로그인 유무를 확인하여 글로벌 객체에 유저정보를 넣습니다. 앞으로 g.user <-- 에 접근하여 유저정보를 가져오시면 됩니다.
@app.before_request
def before_request():
    print(session)
    if 'user_id' in session:
        user_dao = get_user_by_id(session['user_id'])
        user_dto = User(user_dao)  # 우리가 사용하는 User 객체 (여기는 패스워드가 빠져있다)
        g.user = user_dto


# 로그인 기능
@app.route('/login', methods=['GET', 'POST'])
def login():
    if 'user_id' in session:
        return redirect(url_for('index'))
    else:
        if request.method == 'POST':
            username = request.form['username']  # 클라이언트로 부터 받아온 유저아이디
            password = request.form['password']  # 패스워트

            # 잘못된 아이디
            user = get_user_by_user_nickname(username)  # 유저를 가져옵니다.
            if not get_user_by_user_nickname(username):  # 유저가 없다면
                flash("존재하지 않는 유저입니다")
                return redirect(url_for('login'))  # 다시 로그인 페이지로 이동

            # 잘못된 비밀번호
            if user and user['user_password'] != password:
                flash("잘못된 패스워드 입니다")
                return redirect(url_for('login'))  # 다시 로그인 페이지로 이동

            # 로그인 성공
            if user and user['user_password'] == password:
                session['user_id'] = user['id']  # user_id : 1 (로그인 유저의 고유의 아이디값 추가)
                return redirect(url_for('index'))  # dashboard_building 페이지로 이동
        return render_template('signin.html')

@app.route('/all_dashboard')
def all_dashboard():
    building_num_all = building_data_dao.get_all_building() #건축물개수
    device_num_all = device_data_dao.get_all_device() #계측기개수
    building_info = building_data_dao.get_all_building_info() #이름종류주소개수이상여부
    return render_template('building_dashboard_all.html', building_num_all=building_num_all, device_num_all=device_num_all, building_info=building_info)


# 주희님 이제 경로가 변경되었습니다.
# 로그인하고 들어오시면 아마 주소창이 /index로 변경되었을 겁니다.
@app.route('/index')
def index():
    if 'user_id' in session:

        print(g.user.id)
        '''
         로그인 하면 g.user 객체를 활용하시면 됩니다.로그인한 유저의 고유 아이디 값 입니다. 그 밖에 이메일 등등의 정보도 있으니 자세한 건
         model 폴더에 user.py 참조하시면 됩니다.
        '''
        building_num = building_data_dao.get_user_building(g.user.id) #건축물개수
        device_num = device_data_dao.get_my_device(g.user.id) #계측기개수
        building_map = building_data_dao.get_user_building_info(g.user.id) #이름종류주소계측기개수
        #decide_criteria = building_dat_dao.decide_criteria(g.user.id) #이상여부
        return render_template('building_dashboard.html', building_num=building_num, device_num=device_num, building_map=building_map)  #building_table=building_table, decide_criteria=decide_criteria

         # 로그인 했다면 해당 페이지 반환
    else:
        building_num_all = building_data_dao.get_all_building() #건축물개수
        device_num_all = device_data_dao.get_all_device() #계측기개수
        building_info = building_data_dao.get_all_building_info() #이름종류주소개수이상여부
        return render_template('building_dashboard_all.html', building_num_all=building_num_all, device_num_all=device_num_all, building_info=building_info)
        # 로그인 하지 않았다면 해당 페이지로 이동합니다.


# 특정 건물 정보
# 주희님께서 building_dashboard.html 작업하실 때 개별 건축물 클릭하면 가령 충무로영상센터의 경우 /building/충무로영상센터 href 설정 해주시면 됩니다.
# 이 부분 변경되었습니다.
@app.route('/building/<building_name>')
def building_page(building_name):

    building_name = building_name
    if building_name is None:
        return redirect(url_for('index'))  # 이 경우 index() 라우팅으로 이동 -> building_dashboard.html 로 이동

    if 'user_id' in session:  # 로그인 했다면
        a = device_data_dao.all_device_info()
        device_list = device_list_dao.each_device_building2(g.user.id, building_name)
        # building_name 을 받아 추가적인 데이터를 building_page.html 에 필요한 데이터를 넘기면 됩니다.
        return render_template('building_page.html', device_list=device_list, building_name = building_name, a = a)  # 정상적인 building_page.html 과 데이터 반환
    else:  # 로그인하지 않은 유저라면
        flash('회원만 접근 가능합니다')
        return render_template('signin.html')  # 로그인화면으로 이동합니다.


# 개별 계측기 정보
# 성연님 개별 디바이스 클릭하실 때 이렇게 넘겨주면 고맙겠습니다!
# /building/{building_name}/{device_id}
# ex) /building/충무로영상센터/gnss1
# 그러면 저는 충무로영상센터(건물이름) 과 gnss1(특정계측기) 를 이용해서 작업을 할 수 있을 거 같습니다.
@app.route('/building/<building_name>/<device_id>')
def devices(building_name, device_id):
    print(building_name, device_id)
    # 계측기 데이터
    device_info = each_device_info("syntest1")
    device_info[0]['device_name'] = device_id  # 계측기 이름 추가

    # 날씨정보
    weatherData = weather.get_weather("syntest1")
    print(weatherData)
    # boxplot 데이터
    r = json.dumps(box_plot.plot("syntest1", 5))
    boxplotData = json.loads(r)
    print(boxplotData)


    print(device_info)
    # 실시간 데이터
    return render_template('device.html',
                           device_info=device_info[0],
                           weatherData=weatherData,
                           boxplotData=boxplotData)


# 계측기 등록
@app.route('/register',methods = ['GET','POST'])
def register_device():


    if request.method == 'POST':
        #클라이언트로 부터 받은 정보
        login_user_id = request.form['login_user_id']
        b_name = request.form['b_name']
        b_type = request.form['b_type']
        b_addr = request.form['b_addr']
        d_id = request.form['d_id']
        d_name = request.form['d_name']
        d_loc = request.form['d_loc']

        device_data_dao.register_my_device(login_user_id,b_name,b_type,b_addr,d_id,d_name,d_loc)

    return render_template('register_form.html')


if __name__ == "__main__":
    # print(each_device_info("syntest1"))
    # print(type(each_device_info("syntest1")))
    weatherData = weather.get_weather("syntest1")
    # print(weatherData)
    print(box_plot.plot("syntest1", 5))
    r = json.dumps(box_plot.plot("syntest1", 5))
    loaded_r = json.loads(r)
    print(loaded_r)
    app.run(host="localhost", port=3000, debug=True)
