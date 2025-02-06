from flask import Flask, render_template
import pandas as pd

app = Flask(__name__)
app.secret_key = "230169"

df = pd.read_excel("myproject\static\excel\J2625.xlsx",
                   sheet_name='R6_Subject')


def NoCvt(cell):
    """
    ローマ数字・漢数字の相互変換をする
    :param cell: 変換するvalue
    :return: 変換後のvalue
    """
    d = dict(III="三", II="二", I="一", iii="三", ii="二", i="一")
    for key, value in d.items():
        if key in cell:
            return cell.replace(key, value)
        elif value in cell:
            return cell.replace(value, key)
    return cell


def add_timetable(data, timetable):
    for _, row in data.iterrows():
        cell = row.to_list()
        cell[0] = NoCvt(cell[0])
        period = row["開講時間"]
        day1 = row["曜日1"]
        day2 = int(row["曜日2"]) if pd.notna(row["曜日2"]) else None

        if timetable[period][day1]:
            timetable[period][day1].append(cell)
        else:
            timetable[period][day1] = [cell]

        if day2 != None:
            if timetable[period][day2]:
                timetable[period][day2].append(cell)
            else:
                timetable[period][day2] = [cell]


periods = ["1,2", "3,4", "5,6", "7,8", "9,10", "11,12"]


@ app.route("/")
def index():
    timetable = [[[""]for col in range(5)] for row in range(6)]
    return render_template("index.html",
                           periods=periods,
                           timetable=timetable,
                           df_records=df.to_dict(orient='records'))


@ app.route("/simulator")
def simulator():
    timetableList = [[[""] for col in range(5)] for row in range(6)]
    subjectList = [["" for col in range(5)] for row in range(6)]
    add_timetable(df, subjectList)

    return render_template("simulator.html", periods=periods, timetableList=timetableList, subjectList=subjectList)


if __name__ == '__main__':
    app.run(debug=True)
