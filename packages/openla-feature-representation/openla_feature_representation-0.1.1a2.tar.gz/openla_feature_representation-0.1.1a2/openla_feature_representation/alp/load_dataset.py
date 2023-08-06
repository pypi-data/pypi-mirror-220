import numpy as np
import pandas as pd
import tensorflow as tf
from sklearn.model_selection import StratifiedKFold


# 成績を出力のインデックスに変換（0: no-risk, 1:at-risk）
def change_grade(grade):
    if grade == "A":
        grade = 0
    elif grade == "B":
        grade = 0
    elif grade == "C":
        grade = 1
    elif grade == "D":
        grade = 1
    elif grade == "F":
        grade = 1
    else:
        raise ValueError("invalid grade")

    return grade


# sourceデータとtargetデータの入力特徴と成績のデータをDataFrameで返す
def load_source_target(source_course, target_course=None, until_week=None):
    # 引数
    #  source_course (List[int] or int): source courseの ID．
    #  target_course (List[int] or int): target courseの ID. sourceデータでクロスバリデーションをするときは関係ない
    #  until_week (int)　　　　　　　　　　　　　　: 何週目までのデータを入力するか

    # リスト型での処理を行うため，使用するコースが複数でないならばリストに変換
    if type(source_course) is int:
        source_course = [source_course]
    if type(target_course) is int:
        target_course = [target_course]

    # データセットをDataFrameで読み込み
    def load_df(courses):
        all_score_df, all_feature_df = pd.DataFrame(), pd.DataFrame()
        for course in courses:
            score_df = pd.read_csv(f"Dataset/grade_{course}.csv")
            feature_df = pd.read_csv(f"Dataset/alp_{course}.csv")

            score_df["userid"] = score_df["userid"].apply(lambda id: str(course) + "_" + str(id))
            feature_df["userid"] = feature_df["userid"].apply(lambda id: str(course) + "_" + str(id))

            all_score_df = pd.concat([all_score_df, score_df], axis=0)
            all_feature_df = pd.concat([all_feature_df, feature_df], axis=0)

        return all_score_df, all_feature_df
    source_score_df, source_feature_df = load_df(courses=source_course)
    target_score_df, target_feature_df = load_df(courses=target_course)

    source_score_df.set_index("userid", inplace=True)
    target_score_df.set_index("userid", inplace=True)

    # 成績(A,B,C,D,F)を出力のインデックスに変換（0: no-risk, 1:at-risk）
    source_score_df["grade"] = source_score_df["grade"].apply(change_grade)
    target_score_df["grade"] = target_score_df["grade"].apply(change_grade)

    # モデルの訓練/評価に使う週までのデータのみを抽出
    source_feature_df = source_feature_df[source_feature_df["classid"].isin(list(range(1, until_week+1)))]
    target_feature_df = target_feature_df[target_feature_df["classid"].isin(list(range(1, until_week+1)))]

    # 戻り値
    # source_feature_df (pd.DataFrame) : モデル訓練に使う入力特徴のDataFrame
    # source_score_df (pd.DataFrame)   : モデル訓練に使う正解ラベルのDataFrame
    # target_feature_df (pd.DataFrame) : モデル評価に使う入力特徴のDataFrame
    # target_score_df (pd.DataFrame)   : モデル評価に使う正解ラベルのDataFrame
    return source_feature_df, source_score_df, target_feature_df, target_score_df


# DataFrameから必要な情報を取り出してモデルへの入出力に変換する
def input_output(feature_df, score_df, return_sequences):
    # 引数
    # source_feature_df (pd.DataFrame) : 入力特徴のDataFrame
    # source_score_df (pd.DataFrame)   : 正解ラベルのDataFrame
    # return_sequences (bool)          : すべての時系列に対して出力を行うかどうか
    x = []
    y = []
    output_units = 2
    for user_id, user_df in feature_df.groupby("userid"):
        if user_id not in score_df.index:
            continue
        user_df.sort_values("classid", inplace=True) # 時系列順に並べる

        score = score_df.at[user_id, "grade"]
        if return_sequences:
            score = [score] * len(user_df)  # 全ての時系列に与えるため，時系列長だけ複製

        x.append(user_df.drop(["userid", "classid"], axis=1).values) # 不要なカラムを削除して入力に追加
        y.append(np.eye(output_units)[score])                          # one-hotベクトル化して追加
    x = np.array(x).astype(np.float32)
    y = np.array(y)

    return x, y

# DataFrameから訓練時と評価時に使う入力と出力を作る
def make_input_output(source_feature_df, source_score_df, target_feature_df, target_score_df, return_sequences=True):
    # 引数
    # source_feature_df (pd.DataFrame)        : モデル訓練に使う入力特徴のDataFrame
    # source_score_df (pd.DataFrame)          : モデル訓練に使う正解ラベルのDataFrame
    # target_feature_df (pd.DataFrame)        : モデル評価に使う入力特徴のDataFrame
    # target_score_df (pd.DataFrame)          : モデル評価に使う正解ラベルのDataFrame
    # return_sequences (bool)                 : すべての時系列に対して出力を行うかどうか

    x_train, y_train = input_output(source_feature_df, source_score_df, return_sequences)
    x_test, y_test = input_output(target_feature_df, target_score_df, return_sequences)
    timesteps = x_train.shape[1]
    num_features = x_train.shape[-1]

    # 戻り値
    # x_train (np.array): モデル訓練に使う入力．shape:(ユーザー数，時系列長，特徴数)
    # y_train (np.array): モデル訓練に使う出力．shape:(ユーザー数，正解ラベルの次元数(2))
    # x_test  (np.array): モデル評価に使う入力．shape:(ユーザー数，時系列長，特徴数)
    # y_test  (np.array): モデル評価に使う出力．shape:(ユーザー数，正解ラベルの次元数(2))
    # timesteps (int)   : 時系列の長さ
    # num_features (int): 入力特徴の数
    return x_train, y_train, x_test, y_test, timesteps, num_features



# DataFrameからKnowledge distillationを使った訓練と評価のための入力と出力を作る
def make_input_output_kd(source_feature_df, source_score_df, target_feature_df, target_score_df,
                         return_sequences=True, until_week=None,
                         teacher_model=None, source_feature_df_teacher=None,):
    # 引数
    # source_feature_df (pd.DataFrame)        : モデル訓練に使う入力特徴のDataFrame
    # source_score_df (pd.DataFrame)          : モデル訓練に使う正解ラベルのDataFrame
    # target_feature_df (pd.DataFrame)        : モデル評価に使う入力特徴のDataFrame
    # target_score_df (pd.DataFrame)          : モデル評価に使う正解ラベルのDataFrame
    # return_sequences (bool)                 : すべての時系列に対して出力を行うかどうか
    # kd (bool)                               : Knowledge Distillation (KD) 用の入出力を作るかどうか
    # teacher_model (RNN)                     : KDの教師モデル
    # source_feature_df_teacher (pd.DataFrame): KDの教師モデルの入力特徴
    # until_week (int):                       : 何週目までを入力して学習するか

    def input_output_kd(feature_df_student, feature_df_teacher, score_df, teacher_model):
        x = []
        y_true = []
        y_pred = []
        y_hidden = []
        output_units = 2
        for user_id, student_feature in feature_df_student.groupby("userid"):
            if user_id not in score_df.index: # 成績が無いやつは除外
                continue
            student_feature.sort_values("classid", inplace=True) # 生徒モデルに入力する特徴を時系列順に並べる

            # 生徒モデルに入力したのと同じ学生についての教師モデル用の入力特徴を取得
            teacher_feature = feature_df_teacher[feature_df_teacher["userid"] == user_id]
            teacher_feature.sort_values("classid", inplace=True)
            teacher_feature = np.expand_dims(teacher_feature.drop(["userid", "classid"], axis=1).values, axis=0)

            # 教師モデルの時系列最後の予測結果を取得
            if return_sequences:
                pred_score, final_hidden = teacher_model.predict(teacher_feature)
                pred_score = pred_score[0][-1]
            else:
                pred_score, final_hidden = teacher_model.predict(teacher_feature)
            # 教師モデルの時系列最後の隠れ状態を取得
            final_hidden = final_hidden.reshape(final_hidden.shape[-1])

            # 正解ラベルを取得
            score = score_df.at[user_id, "grade"]
            if return_sequences:
                score = [score] * until_week

            x.append(student_feature.drop(["userid", "classid"], axis=1).values)
            y_true.append(np.eye(output_units)[score])
            y_pred.append(pred_score)
            y_hidden.append(final_hidden)

        x = np.array(x).astype(np.float32)
        y_true = np.array(y_true)
        y_pred = np.array(y_pred)
        y_hidden = np.array(y_hidden)
        return x, y_true, y_pred, y_hidden

    x_train, y_true, y_pred, y_hidden = input_output_kd(source_feature_df, source_feature_df_teacher, source_score_df, teacher_model)
    x_test, y_test = input_output(target_feature_df, target_score_df, return_sequences)
    timestep = 1
    num_features = x_train.shape[-1]

    # 戻り値
    #  x_train, y_true, x_test, y_test, timestep, num_features : make_input_output()関数と同じ
    #  y_pred (np.array)   : 教師モデルの時系列最後の出力．shape:(ユーザー数，正解ラベルの次元数(2))
    #  y_hidden (np.array) : 教師モデルの時系列最後の隠れ状態．shape:(ユーザー数，隠れ層のユニット数)
    return x_train, y_true, y_pred, y_hidden, x_test, y_test, timestep, num_features


def load_dataset_baseline(source_course, target_course=None, return_sequences=True, until_week=None):
    # 入力特徴と出力のDataFrameを取得
    source_target = load_source_target(source_course=source_course, target_course=target_course, until_week=until_week)
    source_feature_df, source_score_df, target_feature_df, target_score_df = source_target

    # DataFrameからモデルの入出力データを取得
    input_output = make_input_output(source_feature_df, source_score_df, target_feature_df, target_score_df, return_sequences)
    x_train, y_train, x_test, y_test, timestep, num_features = input_output

    return x_train, y_train, x_test, y_test, timestep, num_features


def load_dataset_kd(source_course, teacher_model: tf.keras.Model, target_course=None,
                    return_sequences=True, until_week=None, teacher_week=None):

    # 教師モデルの入力特徴と出力のDataFrameを取得
    source_target_teacher = load_source_target(source_course=source_course, target_course=target_course, until_week=teacher_week)
    source_feature_df_teacher, source_score_df, _, _ = source_target_teacher

    # 生徒モデルの入力特徴と出力のDataFrameを取得
    source_target_student = load_source_target(source_course=source_course, target_course=target_course, until_week=until_week)
    source_feature_df_student, _, target_feature_df, target_score_df = source_target_student

    # DataFrameから入出力データを取得
    input_output = make_input_output_kd(source_feature_df_student, source_score_df, target_feature_df, target_score_df,
                                        return_sequences=return_sequences, teacher_model=teacher_model,
                                        source_feature_df_teacher=source_feature_df_teacher, until_week=until_week)
    x_train, y_true, y_pred, y_hidden, x_test, y_test, timestep, num_features = input_output

    return x_train, y_true, y_pred, y_hidden, x_test, y_test, num_features

