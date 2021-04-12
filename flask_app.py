# -*- coding: utf-8 -*-
# @Time: 04/11/2021 11:55
# @Author: Jiayi(Mike) Wang
# @File: flask_app.py
import json

from flask import render_template, request, Flask

from jwringcentral import ImportLocal, CommonColumns, Percentiles

app = Flask(__name__)
auto_data_path = "./data/autodata.csv"
house_data_path = "./data/housedata.csv"
auto_data_df = ImportLocal(auto_data_path)
house_data_df = ImportLocal(house_data_path)


@app.route('/result', methods=['post', 'get'])
def result():
    if request.method == "POST": 
        res = request.form  
        number = int(res['number'])
        csv_list = ["autodata.csv", "housedata.csv"]
        auto_data_path = csv_path + csv_list[0]
        house_data_path = csv_path + csv_list[1]
        auto_data_df = ImportLocal(auto_data_path)
        house_data_df = ImportLocal(house_data_path)
        successful = True
        first_result = None
        second_result = None
        third_result = None
        df_shape = None
        try:
            first_result = CommonColumns(auto_data_df, house_data_df)
            df_shape = auto_data_df.shape
            second_result = json.loads(ImportLocal(auto_data_path)[0:2].to_json(orient='records', force_ascii=False))
            third_result = Percentiles(house_data_df, number)
            print(first_result)
            print(second_result)
            print(third_result)
            print(df_shape)
        except Exception:
            successful = False
        if successful is False:
            return render_template("result.html", successful=successful)
        else:
            return render_template("result.html", successful=successful, first_result=csv_list,
                                   second_result=second_result, third_result=third_result, df_shape=df_shape)


@app.route('/')
def index():
    return render_template("index.html")


if __name__ == "__main__":
    app.run()
