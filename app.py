from flask import Flask, jsonify, request
from sqlalchemy import create_engine, text
from utils.recommendationSystem import *
from utils.item_based import *;
import pandas as pd
import pymysql


def create_app(test_config=None):
    app = Flask(__name__)

    if test_config is None:
        app.config.from_pyfile("./utils/config.py")
    else:
        app.config.update(test_config)

    database = create_engine(app.config['DB_URL'], encoding='utf-8', max_overflow=0)
    app.database = database

    # 퍼지 이론 추천 시스템
    @app.route('/fuzzyRecommend', methods=['POST', 'GET'])
    def getFuzzyRecommendation():

        user_id = request.values.get('user_id')
        age = request.values.get('age')
        stay_duration = request.values.get('stay_duration')

        interest_id = recommendInterest(getLevel(age, stay_duration))

        print(interest_id)

        query = """
                UPDATE user SET interest_id = %s
                WHERE user_id = %s
        """

        inputData = (interest_id, user_id)
        app.database.execute(query, inputData)

        return 'OK'

    # item based CF
    @app.route('/cfRecommend', methods=['POST', 'GET'])
    def getCFRecommendation():

        user_id = request.values.get('user_id')

        select_interest_name = "SELECT ii.interest_name, u.interest_id, u.recent_id FROM interest_info ii, user u WHERE u.user_id= %s and u.interest_id=ii.interest_id"
        inputData = user_id
        data = app.database.execute(select_interest_name, inputData).fetchone()

        ## interest_id 에 대한 정보 얻어오기
        interestIdVO = {
            'interest_id': data['interest_id'],
            'recent_id': data['recent_id']
        } if data else None

        query2 = "SELECT h.user_id, h.history_count, ii.interest_id FROM interest_info ii, history h, unit_interest_info uii WHERE h.part_no=uii.part_no and h.unit_no=uii.unit_no and ii.interest_id=uii.interest_id ORDER BY h.user_id, h.part_no, h.unit_no"

        interestIdVO['interest_id'] = getDataframe(query2, app.database, interestIdVO['recent_id'])

        updateInterestIdQuery = """
                        UPDATE user SET interest_id = %s
                        WHERE user_id = %s
                    """

        inputData = (int(interestIdVO['interest_id']), user_id)
        app.database.execute(updateInterestIdQuery, inputData)

        return 'OK'

    return app

if __name__=="__main__":
    create_app().run(host="127.0.0.1", port=5000, debug=True)

