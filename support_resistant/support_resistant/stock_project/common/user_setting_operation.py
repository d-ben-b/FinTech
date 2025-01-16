import json
import psycopg2
import pathlib
import os


class ConnectUserDB(object):

    def __init__(self):
        db_config_path = pathlib.Path(
            __file__).parent.parent / 'config' / "db.config.json"

        with open(db_config_path, 'r', encoding='utf-8') as f:
            self.db_info = json.load(f)

        # Connect to PostgreSQL server
        self.db_conn = psycopg2.connect(
            host=self.db_info.get('HOST'),
            # -!!!!!!!!!!!!要修改!!!!!!!!!!!!!!!!!!
            database=self.db_info.get('NAME'),
            # -!!!!!!!!!!!!要修改!!!!!!!!!!!!!!!!!!
            user=self.db_info.get("USER"),
            # -!!!!!!!!!!!!要修改!!!!!!!!!!!!!!!!!!
            password=self.db_info.get("PASSWORD"),
            # -!!!!!!!!!!!!要修改!!!!!!!!!!!!!!!!!!
            port=self.db_info.get("PORT")
        )
        print("Connect successful!")

        self.db_cursor = self.db_conn.cursor()

    def _get_user_id(self, username):
        sql = f"""SELECT id FROM auth_user
            WHERE username = %s"""
        sql_val = (username, )
        self.db_cursor.execute(sql, sql_val)
        user_id = self.db_cursor.fetchall()[0][0]

        return user_id


class UserTrackingHandler(ConnectUserDB):

    def __init__(self):
        super().__init__()

    # add track
    def add(self, **kwargs):
        user_id = self._get_user_id(kwargs['username'])

        sql = f"""
            INSERT INTO user_track_supres(user_id, start_date,
            symbol, number_of_signals, up_gap_interval, down_gap_interval,
            diff, peak_left, peak_right, valley_left, valley_right, swap_times,
            previous_day, survival_time, nk_valley_left, nk_valley_right, nk_peak_left, nk_peak_right, nk_startdate,
            nk_enddate, nk_interval, nk_value)
            VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            ON CONFLICT DO NOTHING;
        """
        sql_val = (user_id,
                   kwargs['start_date'],
                   kwargs['symbol'],
                   kwargs['signals_selected_values'],
                   kwargs['up_gap_interval'],
                   kwargs['down_gap_interval'],
                   kwargs['diff'],
                   kwargs['peak_left'],
                   kwargs['peak_right'],
                   kwargs['valley_left'],
                   kwargs['valley_right'],
                   kwargs['swap_times'],
                   kwargs['previous_day'],
                   kwargs['survival_time'],
                   kwargs['nk_valley_left'],
                   kwargs['nk_valley_right'],
                   kwargs['nk_peak_left'],
                   kwargs['nk_peak_right'],
                   kwargs['nk_startdate'],
                   kwargs['nk_enddate'],
                   kwargs['nk_interval'],
                   kwargs['nk_value'])

        self.db_cursor.execute(sql, sql_val)
        self.db_conn.commit()

    # remove track
    def remove(self, user, symbol, start_date):
        user_id = self._get_user_id(user)

        sql = f"""DELETE FROM user_track_supres U
                    WHERE U.user_id = %s
                    AND U.symbol = %s
                    AND U.start_date = %s
                """
        sql_val = (user_id, symbol, start_date)
        self.db_cursor.execute(sql, sql_val)
        self.db_conn.commit()
        return

    # get user email from name
    def get_user_email(self, user):

        sql = f"""
            SELECT email FROM auth_user
            where username = %s
        """
        sql_val = (user, )
        self.db_cursor.execute(sql, sql_val)
        res = self.db_cursor.fetchall()[0][0]
        return res

    # get user name & email
    def get_all_user_info(self):
        sql = f"""
            SELECT DISTINCT (auth_user.username), auth_user.email FROM user_track_supres
            INNER JOIN auth_user ON user_track_supres.user_id = auth_user.id;
        """
        self.db_cursor.execute(sql)
        res = self.db_cursor.fetchall()
        return res

    # select user
    def get_all_user_id(self):
        sql = f"""SELECT user_track_supres.user_id
                FROM user_track_supres
                GROUP BY user_track_supres.user_id"""
        self.db_cursor.execute(sql)
        res = self.db_cursor.fetchall()
        return res

    # select track spreads
    def get_track_spreads_from_user(self, user):
        sql = f"""
            SELECT user_track_supres.created_at::date,  TO_CHAR(start_date::date, 'Mon-DD-YYYY') AS start_date,
            symbol, number_of_signals, up_gap_interval, down_gap_interval,
            diff, peak_left, peak_right, valley_left, valley_right, swap_times,
            previous_day, survival_time, nk_valley_left, nk_valley_right, nk_peak_left, nk_peak_right, nk_startdate,
            nk_enddate, nk_interval, nk_value
            FROM user_track_supres
            INNER JOIN auth_user ON auth_user.id = user_track_supres.user_id
            WHERE auth_user.username = %s"""
        sql_val = (user, )
        self.db_cursor.execute(sql, sql_val)
        res = self.db_cursor.fetchall()
        return res

    # select underlying
    def get_track_underlying(self):
        sql = f"""
            SELECT DISTINCT (symbol) FROM user_track_spreads
        """
        self.db_cursor.execute(sql)
        res = self.db_cursor.fetchall()
        return [ele[0] for ele in res]


if __name__ == "__main__":
    ush = UserTrackingHandler()

    ush.add(
        username="thomas",
        start_date="2022-01-01",
        symbol="QQQ",
        signals_selected_values=[1, 2, 3],
        up_gap_interval=90,
        down_gap_interval=180,
        diff=1,
        peak_left=10,
        peak_right=10,
        valley_left=10,
        valley_right=10,
        swap_times=10,
        previous_day=10,
        survival_time=10,
        nk_valley_left=10,
        nk_valley_right=10,
        nk_peak_left=10,
        nk_peak_right=10,
        nk_startdate=10,
        nk_enddate=10,
        nk_interval=10,
        nk_value=10,
    )

    user_info = ush.get_all_user_info()
    track_info = ush.get_track_spreads_from_user('thomas')
    ush.remove('thomas', "UUP", "2023-02-01")
