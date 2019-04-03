import numpy as np
import FileReader
import model


truth = {
    'free_fall_0' : (0.7, -1),
    'free_fall_1' : (0.4, 0.7),
    'free_fall_2' : (0.4, 0.75),
    'free_fall_3' : (0.4, 0.8),
    'free_fall_4' : (0.2, 0.5),
    'free_fall_5' : (0.25, 0.6),
    'free_fall_6' : (0.4, 0.65),
    'free_fall_7' : (0.4, 0.7),
    'free_fall_8' : (0.5, 0.8),
    'free_fall_9' : (0.35, 0.7),
    'throw_0' : (0.35, -1),
    'throw_1' : (0.375, -1),
    'throw_2' : (0.5, -1),
    'throw_3' : (0.3, -1),
    'throw_4' : (0.5, -1),
    'throw_5' : (0.2, 0.5),
    'throw_7' : (0.35, -1),
    'throw_8' : (0.4, -1),
    'throw_9' : (0.3, -1),
    'throwing_up+catching_0' : (0.35, -1),
    'throwing_up+catching_1' : (0.5, -1),
    'throwing_up+catching_2' : (0.3, -1),
    'throwing_up+catching_3' : (0.28, -1),
    'throwing_up+catching_4' : (0.25, 0.52),
    'throwing_up+catching_5' : (0.3, -1),
    'throwing_up+catching_6' : (0.25, 0.55),
    'throwing_up+catching_7' : (0.18, 0.45),
    'throwing_up+catching_8' : (0.22, 0.5),
    'throwing_up+catching_9' : (0.25, 0.52)
}


if __name__ == '__main__':

    all_data = FileReader.read_files('/../res/data/', '*.txt')
    data = []

    for file_data in all_data:
        time_array = np.linspace(0, file_data[1] * (file_data[0] / 1000), num=file_data[1])
        data.append([file_data[2], file_data[3], file_data[4], file_data[5], time_array])

    res = dict()
    TP_count = 0
    TN_count = 0
    FP_count = 0
    FN_count = 0

    for d in data:
        scores = model.process(d, 5, len(d[0]))
        fall_pos = -1
        fall_time = -1
        for i in range(len(scores)):
            if scores[i] >= 1:
                fall_pos = i
                fall_time = i / 100.0  # d[4][i]
                break
        key = d[3][5:-4]
        print key, "fall_pos: ", fall_pos,  " fall_time: ", fall_time
        truth_val = truth.get(key)
        if fall_time == -1 and truth_val is None:
            res[key] = 'TN'
            TN_count += 1
        if fall_time == -1 and truth_val is not None:
            res[key] = 'FN'
            FN_count += 1
        if fall_time != -1 and truth_val is None:
            res[key] = 'FP'
            FP_count += 1
        if fall_time != -1 and truth_val is not None:
            low = truth_val[0]
            high = truth_val[1]
            if high == -1:
                high = len(scores) / 100.0
            if low <= fall_time <= high:
                res[key] = 'TP'
                TP_count += 1
            else:
                res[key] = 'FP'
                FP_count += 1
    print "TP: ", TP_count, " FP: ",  FP_count, " TN: ", TN_count, " FN: ", FN_count