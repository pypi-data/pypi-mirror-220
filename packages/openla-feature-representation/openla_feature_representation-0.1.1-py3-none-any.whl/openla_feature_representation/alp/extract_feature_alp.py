"""
load_data.pyでデータベースから取得したデータを予測モデルの入力特徴に変換するプログラム
"""
import os
import pandas as pd
# import argparse
# parser = argparse.ArgumentParser()
# parser.add_argument("--course", type=int, nargs="+", required=True)
# args = parser.parse_args()

# load_data.pyで保存したファイルの親ディレクトリ
SAVE_DIR = "Dataset"
DATASET_DIR = "Dataset"

# 作成した入力特徴を保存するディレクトリ
# DATASET_DIR = "../DATASET"
# os.makedirs(DATASET_DIR, exist_ok=True)

# イベントログをページ遷移ごとに集計する関数．OpenLAに実装されているものと同じ
def convert_into_page_transition(event_stream, invalid_seconds=None, timeout_seconds=None, count_operation=True, operation_name=None):
    # 引数
    #  event_stream (pd.DataFrame)    : イベントログのDataFrame
    #  invalid_seconds (int)          : あるページをinvalid_seconds以上読んでなければ，ページを読んだことにならない
    #  timeout_seconds (int)          : あるページをtimeout_secondsよりも長く読んでいれば，タイムアウトとみなす
    #  count_operation (bool)         : 集計の際に，各ページでの操作（マーカーなど）の回数も集計するかどうか（False: ページ番号と閲覧時間だけ集計，True: 操作回数も集計）
    #  operation_name (str, List[str]): 各操作の回数を集計する場合，どの操作を集計するか（Noneであれば全ての操作を集計）

    def make_empty_df():
        columns = ["user_id", "contents_id", "page_no", "reading_seconds", "time_of_entry", "time_of_exit"]
        if count_operation:
            columns += operation_name
        return pd.DataFrame(columns=columns)

    if operation_name is None:
        operation_name = event_stream["operation_name"].unique()
    elif isinstance(operation_name, str):
        operation_name = [operation_name]

    page_info_dict_list = []
    for ids, user_contents_df in event_stream.groupby(["user_id", "contents_id"], sort=False):
        user_id = ids[0]
        contents_id = ids[1]

        page_seq = user_contents_df["page_no"].tolist()
        operation_seq = user_contents_df["operation_name"].tolist()
        time_seq = pd.to_datetime(user_contents_df["operation_date"]).tolist()

        # aggregation operations in event stream
        operation_count_dict = empty_operation_count = dict(zip(operation_name, [0]*len(operation_name)))
        time_of_entry_index = 0
        reading_seconds = 0

        for i in range(len(page_seq)):
            if count_operation:
                if operation_seq[i] in operation_count_dict:
                    # set new operation as the key
                    operation_count_dict[operation_seq[i]] += 1

            # If (end of sequence) or (close operation is executed) or (page transition will be happened),
            if (i == len(page_seq) - 1) or \
                (operation_seq[i] == "CLOSE") or \
                (i+1 < len(page_seq)) and (page_seq[i] != page_seq[i + 1]):

                time_of_exit_index = i
                time_of_entry = time_seq[time_of_entry_index]
                time_of_exit = time_seq[time_of_exit_index]

                page_info_dict = {"user_id": user_id, "contents_id": contents_id,
                                  "page_no": page_seq[i], "reading_seconds": reading_seconds,
                                  "time_of_entry": time_of_entry, "time_of_exit": time_of_exit}

                # record operation counts in the page
                if count_operation:
                    page_info_dict.update(operation_count_dict)
                # reset operation count dictionary
                operation_count_dict = empty_operation_count

                # if reading seconds is more than invalid seconds, the page is recorded. else it is passed through
                if (invalid_seconds is None) or (reading_seconds > invalid_seconds):
                    page_info_dict_list.append(page_info_dict)
                else:
                    pass
                reading_seconds = 0

                # if operation is 'CLOSE', next operation 'OPEN' is i+1
                if operation_seq[i] == "CLOSE":
                    time_of_entry_index = i + 1
                    continue
                else:
                    time_of_entry_index = i

            # if the time difference between two actions is over timeout_seconds, the event is regarded as time out.
            time_between_actions = (time_seq[i + 1] - time_seq[i]).seconds if i + 1 < len(time_seq) else None
            if time_between_actions is None:
                pass
            elif (timeout_seconds is not None) and (time_between_actions > timeout_seconds):
                time_of_entry_index = i + 1
                pass
            else:
                reading_seconds += time_between_actions

    transition_df = pd.DataFrame(page_info_dict_list)
    transition_df = transition_df.fillna(0)
    if transition_df.empty:
        empty_df = make_empty_df()
        return empty_df
    else:
        return transition_df


# 閲覧時間を取得する関数
def get_reading_time(transition_df, user_id, features_dict):
    # 引数
    #  transition_df (pd.DataFrame)   : convert_into_page_transition()関数で作成されるページ遷移ごとに集計したイベントログ
    #  user_id (str)                  : ユーザーID
    #  features_dict (Dict[str, int]) : 各入力特徴の辞書．key:特徴の名前，value:特徴の値．

    user_df = transition_df[transition_df["user_id"] == user_id]
    if user_df.empty:
        reading_time = 0
    else:
        reading_time = user_df["reading_seconds"].sum()
    features_dict["slide_views"].update({user_id: reading_time})

    return features_dict


# マーカーを引いた数，メモをとった数，全操作の数を取得する関数
def get_operation_counts(event_stream, user_id, features_dict):
    # 引数
    #  event_stream (pd.DataFrame)    : イベントログのDataFrame
    #  user_id (str)                  : ユーザーID
    #  features_dict (Dict[str, int]) : 各入力特徴の辞書．key:特徴の名前，value:特徴の値．

    user_df = event_stream[event_stream["user_id"] == user_id]
    operation_count = user_df["operation_name"].value_counts()
    markers = operation_count["ADD MARKER"] if "ADD MARKER" in operation_count else 0
    memos = operation_count["ADD MEMO"] if "ADD MEMO" in operation_count else 0
    actions = len(user_df)

    features_dict["markers"].update({user_id: markers})
    features_dict["memos"].update({user_id: memos})
    features_dict["actions"].update({user_id: actions})

    return features_dict


# 出席状況を取得する関数
def get_attendance(attendance_df, lecture_week, user_id, features_dict):
    # 引数
    #  attendance_df (pd.DataFrame)   : load_data.pyで取得した出席状況に関するDataFrame
    #  lecture_week (int)             : 出席状況を取得する講義の週
    #  user_id (str)                  : ユーザーID
    #  features_dict (Dict[str, int]) : 各入力特徴の辞書．key:特徴の名前，value:特徴の値．

    if (lecture_week, user_id) not in attendance_df.index:
        value = 0
    else:
        status = attendance_df.xs([lecture_week, user_id], level=["lecture", "userid"])["status"].values[0]
        if status == "Presence":
            value = 5
        elif status == "Late":
            value = 3
        else:
            value = 0
    features_dict["attendance"].update({user_id: value})
    return features_dict


# レポート提出状況を取得する関数
def get_report_submission(report_submission_df, lecture_week, user_id, features_dict):
    # 引数
    #  report_submission_df (pd.DataFrame)   : load_data.pyで取得したレポート提出状況に関するDataFrame
    #  lecture_week (int)                    : レポート提出状況を取得する講義の週
    #  user_id (str)                         : ユーザーID
    #  features_dict (Dict[str, int])        : 各入力特徴の辞書．key:特徴の名前，value:特徴の値．

    value = 0
    if (lecture_week, user_id) not in report_submission_df.index:
        pass
    else:
        submit_status = report_submission_df.xs([lecture_week, user_id], level=["lecture", "userid"])["status"].values
        num_assignments = report_submission_df[list(report_submission_df.reset_index()["lecture"]==lecture_week)]["assignment"].nunique()
        for status in submit_status:
            if status == "Submit":
                value += 5./num_assignments
            elif status == "Late":
                value += 3./num_assignments
            else:
                pass
    features_dict["report"].update({user_id: value})
    return features_dict


#　Moodle上でのコースアクセス回数を取得する関数
def get_course_views(course_views_df, lecture_week, user_id, features_dict):
    # 引数
    #  course_views_df (pd.DataFrame) : load_data.pyで取得したコースアクセス回数に関するDataFrame
    #  lecture_week (int)             : 出席状況を取得する講義の週
    #  user_id (str)                  : ユーザーID
    #  features_dict (Dict[str, int]) : 各入力特徴の辞書．key:特徴の名前，value:特徴の値．

    if (lecture_week, user_id) not in course_views_df.index:
        view_count = 0
    else:
        view_count = course_views_df.xs([lecture_week, user_id], level=["lecture", "userid"])["course_views"].values[0]
    features_dict["course_views"].update({user_id: view_count})
    return features_dict


# すべての特徴をまとめる
def aggregate_feature(course_id):
    lecture_time      = pd.read_csv(f"{SAVE_DIR}/Course_{course_id}_LectureTime.csv")
    event_stream      = pd.read_csv(f"{SAVE_DIR}/Course_{course_id}_EventStream.csv")
    attendance        = pd.read_csv(f"{SAVE_DIR}/Course_{course_id}_Attendance.csv")
    report_submission = pd.read_csv(f"{SAVE_DIR}/Course_{course_id}_ReportSubmission.csv")
    course_views      = pd.read_csv(f"{SAVE_DIR}/Course_{course_id}_CourseViews.csv")

    event_stream["user_id"]     = event_stream["user_id"].apply(str)
    attendance["userid"]        = attendance["userid"].apply(str)
    report_submission["userid"] = report_submission["userid"].apply(str)
    course_views["userid"]      = course_views["userid"].apply(str)

    attendance.set_index(["lecture", "userid"], inplace=True)
    report_submission.set_index(["lecture", "userid"], inplace=True)
    course_views.set_index(["lecture", "userid"], inplace=True)

    grade = pd.read_csv(f"{DATASET_DIR}/grade_{course_id}.csv")
    grade["userid"] = grade["userid"].apply(str)
    users = grade["userid"].tolist()

    features = ["attendance", "report", "course_views", "slide_views", "markers", "memos", "actions"]
    features_df = pd.DataFrame()
    prev_lecture_end = None
    for _, row in lecture_time.iterrows(): # 各講義週について，それぞれ特徴をまとめる
        dicts = [{} for _ in range(len(features))]
        features_dict = dict(zip(features, dicts))
        lecture_week = row["lecture"]
        start_time = row["starttime"]
        end_time = row["endtime"]

        # 講義中のイベントログを抽出
        stream_in_lecture = event_stream[(start_time <= event_stream["operation_date"]) & (event_stream["operation_date"] < end_time)]

        # 講義前の特徴を取得
        if prev_lecture_end is None:
            stream_before_lecture = event_stream[event_stream["operation_date"] < start_time]
        else:
            stream_before_lecture = event_stream[(prev_lecture_end <= event_stream["operation_date"]) & (event_stream["operation_date"] < start_time)]
        transition_df = convert_into_page_transition(stream_before_lecture, invalid_seconds=5, timeout_seconds=30*60, count_operation=False)
        prev_lecture_end = end_time

        #　講義前と講義中のイベントログを結合
        stream = pd.concat([stream_in_lecture, stream_before_lecture])

        # 各ユーザーの特徴を取得
        for user_id in users:
            features_dict = get_reading_time(transition_df=transition_df, user_id=user_id, features_dict=features_dict)
            features_dict = get_operation_counts(event_stream=stream, user_id=user_id, features_dict=features_dict)
            features_dict = get_attendance(attendance_df=attendance, lecture_week=lecture_week, user_id=user_id, features_dict=features_dict)
            features_dict = get_report_submission(report_submission_df=report_submission, lecture_week=lecture_week, user_id=user_id, features_dict=features_dict)
            features_dict = get_course_views(course_views_df=course_views, lecture_week=lecture_week, user_id=user_id, features_dict=features_dict)

        df = pd.DataFrame(features_dict)
        df["classid"] = lecture_week
        features_df = pd.concat([features_df, df], axis=0)
    features_df["userid"] = features_df.index
    features_df.sort_values(["userid", "classid"], inplace=True)
    features_df = features_df.loc[:, ["userid", "classid", "attendance", "report", "course_views", "slide_views", "markers", "memos", "actions"]]

    return features_df


# 各学生の特徴を相対的に評価し，ALP(Active Learner Point)に変換
def relative_evaluation(df, feature_name):
    df = df.sort_values(feature_name, ascending=False)
    df = df.reset_index(drop=True)
    ALP_df = df.copy()
    zero_index = len(df.index)
    for i, value in enumerate(df[feature_name]):
        if value == 0:
            zero_index = i
            break

    upper_10 = round(len(df.index) * 0.1)
    upper_20 = upper_10 * 2
    upper_30 = upper_10 * 3
    upper_40 = upper_10 * 4
    upper_50 = upper_10 * 5

    # 上位何%かによって評価
    ALP_df.loc[0: upper_10, feature_name] = 5

    # 同じ値が範囲外まで続くときは評価値の範囲をそこまで伸ばす
    last_value = df.at[upper_10-1, feature_name]
    for index in range(upper_10, len(df.index)):
        value = df.at[index, feature_name]
        if last_value == value:
            ALP_df.at[index, feature_name] = 5
        else:
            break

    # 上で伸ばした範囲が評価の範囲を飛び越していたらスキップ
    if index < upper_20:
        ALP_df.loc[index: upper_20, feature_name] = 4
        last_value = df.at[upper_20 - 1, feature_name]
        for index in range(upper_20, len(df.index)):
            value = df.at[index, feature_name]
            if last_value == value:
                ALP_df.at[index, feature_name] = 4
            else:
                break

    if index < upper_30:
        ALP_df.loc[upper_20: upper_30, feature_name] = 3
        last_value = df.at[upper_30 - 1, feature_name]
        for index in range(upper_30, len(df.index)):
            value = df.at[index, feature_name]
            if last_value == value:
                ALP_df.at[index, feature_name] = 3
            else:
                break

    if index < upper_40:
        ALP_df.loc[upper_30: upper_40, feature_name] = 2
        last_value = df.at[upper_40 - 1, feature_name]
        for index in range(upper_40, len(df.index)):
            value = df.at[index, feature_name]
            if last_value == value:
                ALP_df.at[index, feature_name] = 2
            else:
                break

    if index < upper_50:
        ALP_df.loc[upper_40: upper_50, feature_name] = 1
        last_value = df.at[upper_50 - 1, feature_name]
        for index in range(upper_50, len(df.index)):
            value = df.at[index, feature_name]
            if last_value == value:
                ALP_df.at[index, feature_name] = 1
            else:
                break

    ALP_df.loc[index:, feature_name] = 0

    # 値が0のところは評価0にする
    ALP_df.loc[zero_index:, feature_name] = 0

    return ALP_df


# 各特徴をALPに変換
def feature2ALP(features_df):
    alp_df = pd.DataFrame()
    # 各週の特徴をALPに変換
    for lecture_week, weekly_df in features_df.groupby("classid"):
        for event in weekly_df.drop(["userid", "attendance", "report", "classid"], axis=1).columns:
            weekly_df = relative_evaluation(df=weekly_df, feature_name=event)
        alp_df = pd.concat([alp_df, weekly_df], axis=0)
    alp_df["userid"] = alp_df["userid"].astype(int)
    alp_df.sort_values(["userid", "classid"], inplace=True)

    features = ["attendance", "report", "course_views", "slide_views", "markers", "memos", "actions"]
    # 0 ~ 1の範囲に正規化
    alp_df_normalized = alp_df.copy()
    alp_df_normalized.loc[:, features] = alp_df_normalized.loc[:, features] / 5

    return alp_df, alp_df_normalized


# def main():
#     for course_id in args.course:
#         print(f"\ncourse id: {course_id}")
# 
#         print("aggregate features...")
#         features_df = aggregate_feature(course_id=course_id)
#         features_df.to_csv(f"{SAVE_DIR}/Course_{course_id}_Feature.csv", index=False)
# 
#         print("convert into ALP...")
#         alp_df, alp_df_normalized = feature2ALP(features_df=features_df)
#         alp_df.to_csv(f"{DATASET_DIR}/original/alp_{course_id}.csv", index=False)
#         alp_df_normalized.to_csv(f"{DATASET_DIR}/alp_{course_id}.csv", index=False)


# if __name__ == "__main__":
#     main()