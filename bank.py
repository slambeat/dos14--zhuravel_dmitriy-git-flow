#массив значений стартовых сумм
sum = [
"1_1000",
"2_30000",
"3_100000",
"8_100",
"5_11111",
"9_14124124124",
"6_444",
"4_123456",
"7_100000000000",
"10_81214"
]

#массив значений процентных ставок
rate = [
"1_10",
"2_11",
"3_8",
"4_13",
"5_11",
"6_6",
"7_9",
"8_11",
"9_13",
"10_12"
]

#массив значений сроков
term_years = [
"1_1",
"2_2",
"3_2",
"4_6",
"5_8",
"6_20",
"7_9",
"8_11",
"9_13",
"10_12"
]

dict_array =[]


for i in range(10):
    splited_sum = sum[i].split("_") #разделение id и значения
    splited_rate = rate[i].split("_") #разделение id и значения
    splited_term = term_years[i].split("_") #разделение id и значения
    end_sum = int(splited_sum[1]) + (int(splited_sum[1]) * int(splited_rate[1]) * int(splited_term[1]) // 100) #расчет суммы
    bank = {"id": i + 1, "start_sum": splited_sum[1], "rate": splited_rate[1], "term": splited_term[1], "end_sum": end_sum} #создание словаря
    print(bank) #вывод отдельного словаря
    dict_array.append(bank) #добавление словаря в массив

print(dict_array) #проверка наличия словарей в массиве