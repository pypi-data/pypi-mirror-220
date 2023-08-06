import numpy as np
import pandas as pd
import OpenLA as la


# 閲覧時間と閲覧ページ数(読み返し等の重複含む)の取得
def read_time_and_page(event_stream):

  # ページ遷移ごとの集計
  page_transition = la.convert_into_page_transition(event_stream,          # EventStreamクラスのインスタンス
                                                    user_id=None,          # 変換に含めるユーザーID，リストによる複数指定も可．None: すべて含める
                                                    contents_id=None,      # 変換に含めるコンテンツID，リストによる複数指定も可．None: すべて含める
                                                    invalid_seconds=0,     # 指定した秒数以下の時間で遷移したページは見ていないものとして無効とされる
                                                    timeout_seconds=20*60, # 指定した秒数以上の時間何も操作がなければタイムアウトとして無効とされる
                                                    count_operation=False, # ページ遷移ごとの操作回数も集計するか(True)，ページ遷移ごとの閲覧時間のみ集計するか(False)
                                                    operation_name=None)   # count_operation=Trueの場合，集計に含める操作の名前．None: すべて含める

  # 集計結果から，各ユーザーの閲覧時間と閲覧ページ数を取得（すべてのコンテンツの合計）
  user_list = []
  num_read_pages_list = []
  reading_seconds_list = []
  for user in page_transition.user_id():

    # Page Transitionクラスのnum_transitionメソッドにより遷移回数（重複含む閲覧ページ数）を取得
    # user_id変数で取得するユーザーを指定．contents_id=Noneですべてのコンテンツに対する合計閲覧ページ数を取得
    num_read_pages  = page_transition.num_transition(user_id=user, contents_id=None) 

    # Page Transitionクラスのreading_timeメソッドにより閲覧時間を取得
    # user_id変数で取得するユーザーを指定．contents_id=Noneですべてのコンテンツに対する合計閲覧時間を取得
    reading_seconds = page_transition.reading_time(time_unit="seconds", user_id=user, contents_id=None)

    user_list.append(user)
    num_read_pages_list.append(num_read_pages)
    reading_seconds_list.append(reading_seconds)

  # データフレーム形式にまとめる
  time_page_df = pd.DataFrame({"userid": user_list, 
                               "num_read_pages": num_read_pages_list, 
                               "reading_seconds": reading_seconds_list})
  return time_page_df


# 特徴量作成
def make_feature(event_stream):

  # 閲覧時間と閲覧ページの数を先ほど定義した関数で取得
  time_page_df = read_time_and_page(event_stream)

  # 操作回数の集計
  operation_count = la.convert_into_operation_count(event_stream,           # EventStreamクラスのインスタンス
                                                    user_id=None,           # 変換に含めるユーザーID，リストによる複数指定も可．None: すべて含める
                                                    contents_id=None,       # 変換に含めるコンテンツID，リストによる複数指定も可．None: すべて含める
                                                    operation_name=None,    # 変換に含める操作の名前．None: すべて含める
                                                    for_each_content=False) # コンテンツごとに操作回数を集計するか(True)，すべての合計を出すか(False)

  # 閲覧時間，閲覧ページ数と各操作回数のデータフレームを結合して特徴量とする
  feature_df = pd.merge(left=time_page_df, right=operation_count.df, on="userid")
  feature_df = feature_df.fillna(0)
  feature_df.set_index("userid", drop=True, inplace=True)

  return feature_df
