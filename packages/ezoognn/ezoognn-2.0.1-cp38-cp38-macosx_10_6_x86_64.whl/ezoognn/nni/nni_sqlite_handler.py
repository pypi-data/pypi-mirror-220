import sqlite3
import os
import json
import pandas


class SqliteDBHandler:

    def __init__(self):
        print('SqliteDB初始化............')
        self.con = None
        self.cur = None

    def connect(self, db_path):
        assert(os.path.exists(db_path), 'sqlite.db is not exists!!!')
        self.con = sqlite3.connect(db_path, check_same_thread=False)
        self.cur = self.con.cursor()

    def close(self):
        self.cur.close()
        self.con.close()

    def create_table(self, create_table_sql):
        try:
            self.cur.execute(create_table_sql)
            print('创建表成功')
        except Exception as e:
            print(e)
            print('创建表失败')

    def insert_tab(self, insert_sql, params):

        try:
            self.cur.execute(insert_sql, params)
            self.con.commit()
            print('插入成功')
        except Exception as e:
            print(e)
            self.con.rollback()
            print("插入失败")

    def delete_data(self, delete_sql, params):

        try:
            self.cur.execute(delete_sql, params)
            self.con.commit()
            print('删除成功')
        except Exception as e:
            print(e)
            self.con.rollback()
            print('删除失败')

    def update_data(self, update_sql, params):
        try:
            self.cur.execute(update_sql, params)
            self.con.commit()
            print('修改成功')
        except Exception as e:
            print(e)
            self.con.rollback()
            print('打印失败')

    def select_data(self, select_sql, params):

        try:
            self.cur.execute(select_sql, params)
            person_all = self.cur.fetchall()
            # 返回数据
            return person_all
        except Exception as e:
            print(e)
            self.con.rollback()
            print('查询失败')


'''
获取最好效果的参数，返回一个json结构
'''


def get_best_hyperparameter(db_path):
    sqlite_db_handler = SqliteDBHandler()
    sqlite_db_handler.connect(db_path)

    metric_data = sqlite_db_handler.select_data('select * from MetricData where 1=?', [1])
    metric_data_df = pandas.DataFrame.from_records(metric_data, index=None, exclude=None, columns=None,
                                                   coerce_float=True, nrows=None)
    metric_data_df[5] = metric_data_df[5].str.replace('"', '').astype('float')
    best_param_name = metric_data_df.groupby([1])[5].sum().sort_values(ascending=False).keys()[0]

    trial_job_evnet = sqlite_db_handler.select_data(
        'select data from TrialJobEvent where trialJobId=? and event="WAITING" limit 1', [best_param_name])
    trial_job_evnet_df = pandas.DataFrame.from_records(trial_job_evnet, index=None, exclude=None, columns=None,
                                                    coerce_float=True, nrows=None)
    param = json.loads(trial_job_evnet_df[0].values[0])
    return param


if __name__ == "__main__":
    path = "" + os.sep + "nni-experiments" + os.sep + "ig19cyzu" + os.sep + "db" + os.sep + "nni.sqlite"
    get_best_hyperparameter()
