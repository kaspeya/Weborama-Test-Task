"""Архив с рандомными данными cache - какой - то текст id - ид
    1) нужно вывести те id, которые встречаются в файле только 3 раза
    2) нужно вывести частоту повторений(сколько уникальных ид
    встречалось 1 раз, 2 раза и т.д.)
"""
import csv
import hyperloglog

with open('table.csv', newline='') as csvfile:
    csv_reader = csv.reader(csvfile, delimiter=',')
    next(csv_reader)

    unique_idx_dict = dict()
    count_dict = dict()
    for _, idx in csv_reader:
        n_idx = 0

        if idx not in unique_idx_dict:
            unique_idx_dict[idx] = 1
            n_idx = 1
        else:
            unique_idx_dict[idx] += 1
            n_idx = unique_idx_dict[idx]
            count_dict[n_idx - 1].remove(idx)

        if n_idx not in count_dict:
            count_dict[n_idx] = set()
        count_dict[n_idx].add(idx)

print('\n'.join([f'Число повторений {k}: '
                 f'{len(v)} раз' for k, v in count_dict.items()]))

print(f"Id входящие 3 раза: {' '.join(count_dict[3])}")

"""Решение для большего количества данных - приблизительное, время O(N),
    память O(K), где K - размер буфера:

    Для подсчета частотности использовать HyperLogLog,
    для перечисления id входящих 3 раза - использовать один set,
    для троекратного вхождения, записывать и выписывать оттуда id
    по мере обработки потока данных.

    Реализация - очно на собеседовании))

    Для безумного количества данных - можно использовать тот факт,
    что id - int с 7 цифрами и играть от всех возможных значений поля id.
"""
with open('table.csv', newline='') as csvfile:
    csv_reader = csv.reader(csvfile, delimiter=',')
    next(csv_reader)

    unique_idx_dict = hyperloglog.HyperLogLog(0.01)
    count_dict = dict()
    for _, idx in csv_reader:
        n_idx = 0

        if idx not in unique_idx_dict:
            unique_idx_dict[idx] = 1
            n_idx = 1
        else:
            unique_idx_dict[idx] += 1
            n_idx = unique_idx_dict[idx]
            count_dict[n_idx - 1].remove(idx)

        if n_idx not in count_dict:
            count_dict[n_idx] = set()
        count_dict[n_idx].add(idx)

print('\n'.join([f'Число повторений {k}: '
                 f'{len(v)} раз' for k, v in count_dict.items()]))

print(f"Id входящие 3 раза: {' '.join(count_dict[3])}")
