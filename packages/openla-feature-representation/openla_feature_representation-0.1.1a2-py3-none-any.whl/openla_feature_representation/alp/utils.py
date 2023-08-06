import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.metrics import confusion_matrix

def import_source_data(path, filename):
    data = pd.read_csv('{}/{}.csv'.format(path, filename), index_col=False)
    data_columns = list(data.columns)
    if 'lecture' in data_columns:
        data = data.sort_values(by=['userid', 'lecture']).reset_index(drop=True)
    elif 'classid' in data_columns:
        data = data.sort_values(by=['userid', 'classid']).reset_index(drop=True)
    data = data.fillna(0)
    return data


def grade_to_class(data):
    data = data.sort_values(by=['userid']).reset_index(drop=True)
    data_grade = list(data['grade'])
    grade_classification = list()
    
    for i in range(len(data_grade)):
        if data_grade[i] == 'A':
            grade_classification.append(0)
        elif data_grade[i] == 'B':
            grade_classification.append(0)
        elif data_grade[i] == 'C':
            grade_classification.append(1)
        elif data_grade[i] == 'D':
            grade_classification.append(1)
        else:
            grade_classification.append(1)
    grade_classification_ = np.array(grade_classification)
    onehot_array = np.zeros((grade_classification_.size, grade_classification_.max() + 1))
    onehot_array[np.arange(grade_classification_.size), grade_classification_] = 1
    return onehot_array, grade_classification_


def precision_recall_fscore_accuracy_binary(confusion_matrix_value):
    TP = confusion_matrix_value[3]
    FP = confusion_matrix_value[1] 
    TN = confusion_matrix_value[0] 
    FN = confusion_matrix_value[2]
    # print(TP, FN, FP, TN)

    precision = float(TP / (TP + FP))
    recall =  float(TP / (TP + FN))
    f_score =  float((2 * precision * recall) / (precision + recall))
    accuracy =  float((TP + TN) / (TP + FN + TN + FP))

    # print("Precision: {:.3f},  Recall: {:.3f}, F-score: {:.3f}, Accuracy: {:.3f}".format(precision, recall, f_score, accuracy))
    return precision, recall, f_score, accuracy


def no_and_at_risk_ordes(labels_list):
    no_risk_orders = list()
    at_risk_orders = list()
    for i in range(len(labels_list)):
        if labels_list[i] == 0:
            no_risk_orders.append(i)
        else:
            at_risk_orders.append(i)
    return no_risk_orders, at_risk_orders


def a_b_c_d_f_orders(grade_labels):
    a_orders = list()
    b_orders = list()
    c_orders = list()
    d_orders = list()
    f_orders = list()
    for i in range(len(grade_labels['grade'])):
        if grade_labels['grade'][i] == 'A':
            a_orders.append(i)
        elif grade_labels['grade'][i] == 'B':
            b_orders.append(i)
        elif grade_labels['grade'][i] == 'C':
            c_orders.append(i)
        elif grade_labels['grade'][i] == 'D':
            d_orders.append(i)
        else:
            f_orders.append(i)
    return a_orders, b_orders, c_orders, d_orders, f_orders


def time_features_attention_calculation(list_orders, attention_time_layer_output_, attention_features_layer_output_):
    attention_time_stu = list()
    attention_features_stu = list()
    for train_stu_order in list_orders:
        attention_time = attention_time_layer_output_[train_stu_order]
        attention_features = attention_features_layer_output_[train_stu_order]
        attention_time_stu.append(attention_time)
        attention_features_stu.append(attention_features)

    attention_time_stu_ = np.array(attention_time_stu)
    attention_features_stu_ = np.array(attention_features_stu)

    attention_time_stu_mean = np.round(np.mean(attention_time_stu_, axis=0, dtype=np.float32), decimals= 3)
    attention_features_stu_mean = np.round(np.mean(attention_features_stu_, axis=0, dtype=np.float32), decimals= 3)
    attention_time_stu_mean = attention_time_stu_mean.reshape(attention_time_stu_mean.shape[1])
    
    attention_time_stu_std = np.round(np.std(attention_time_stu_, axis=0, dtype=np.float32), decimals= 3)
    attention_features_stu_std = np.round(np.std(attention_features_stu_, axis=0, dtype=np.float32), decimals= 3)
    attention_time_stu_std = attention_time_stu_std.reshape(attention_time_stu_std.shape[1])
    return attention_time_stu_mean, attention_time_stu_std, attention_features_stu_mean, attention_features_stu_std


def attention_data(Y_test, attention_time_layer, attention_feature_layer):
    all_stu_time = list()
    all_stu_feature = list()
    for i in range(Y_test.shape[0]):
        attention_time_stu, _, attention_features_stu, _ = time_features_attention_calculation([i], attention_time_layer, attention_feature_layer)
        all_stu_time.append(attention_time_stu)
        attention_features_stu_ = attention_features_stu.flatten()
        all_stu_feature.append(attention_features_stu_)

    all_stu_time_ = np.array(all_stu_time)
    all_stu_feature_ = np.array(all_stu_feature)

    attention_time = pd.DataFrame(all_stu_time_)
    attention_feature = pd.DataFrame(all_stu_feature_)
    return attention_time, attention_feature


def confusion_matrix_calculator(true_list, predict_result_list):
    cm  = confusion_matrix(true_list, predict_result_list)
    fig, ax = plt.subplots(figsize=(5, 5))
    ax.imshow(cm)
    ax.grid(False)
    ax.xaxis.set(ticks=(0, 1), ticklabels=('Predict NR', 'Predict AR'))
    ax.yaxis.set(ticks=(0, 1), ticklabels=('Actual NR', 'Actual AR'))
    confusion_matrix_value = list()
    for i in range(2):
        for j in range(2):
            ax.text(j, i, cm[i, j], ha='center', va='center', color='red')
            confusion_matrix_value.append(cm[i, j])
    plt.show()
    return confusion_matrix_value
