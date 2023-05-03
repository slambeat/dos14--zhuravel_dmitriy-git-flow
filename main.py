import os, json, csv, time, yaml

#фунция расчета кредита
def credit_func(sum, percent, term):
    month_cred = (sum + (sum * percent / 100) * term) / (term * 12)
    return month_cred

#функция расчета депозита
def deposit_func(sum, percent, term):
    month_dep =((sum * percent / 100) * term) / (term * 12)
    return month_dep

#читаем файл account.csv и формируем список словарей
account = []
with open('/home/dmitriy_zh/dos14_master_project/account.csv', 'r') as f:
    reader = csv.reader(f)
    for row in reader:
       account.append({'id' : row[0], 'amount' : row[1]})
account.remove({'id': 'id', 'amount': 'amount'})

#приводим числовые значения к типу int
account_int =[]
for i in range(len(account)):
    account_id = account[i]
    account_int.append({'id' : int(account_id['id']), 'amount' : int(account_id['amount'])})
account_int.sort(key = lambda x : x['id']) #сортируем список по id

#читаем файл credit.json и формируем список словарей
credit = []
with open('/home/dmitriy_zh/dos14_master_project/credit.json', 'r') as f:
    credit = json.loads(f.read())
credit.sort(key = lambda x : x['id']) #сортируем список по id

#читаем файл deposit.yaml и формируем список словарей
deposit = []
with open('/home/dmitriy_zh/dos14_master_project/deposit.yaml', 'r') as f:
    deposit = yaml.safe_load(f)
deposit.sort(key = lambda x : x['id']) #сортируем список по id


#раздаем кредиты, формируем список клиентов с кредитами
account_cred_dep =[]
for i in credit:
    account_int_id = account_int[i['id']]
    credit_id = credit[i['id']-1]
    bank_sum = account_int[0]
    if i['sum'] != 0:
        account_int[i['id']] = {'id' : i['id'], 'amount' : account_int_id['amount'] + i['sum']}
        bank_sum['amount'] -= i['sum']
        account_cred_dep.append({'id' : i['id'], 'type' : 'credit', 'term' : credit_id['term'] * 12})
account_int[0] = {'id' : 0, 'amount' : bank_sum['amount']}

#формируем список клиентов с депозитами
for i in deposit:
    account_int_id = account_int[i['id']]
    deposit_id = deposit[i['id']-1]
    if i['sum'] != 0:
        account_cred_dep.append({'id' : i['id'], 'type' : 'deposit', 'term' : deposit_id['term'] * 12})

account_cred_dep.sort(key = lambda x : x['id'])

#проводим ежемесячный расчет (взят срок 50 месяцев)
#Если образовалась задолженность - будет выведено сообщение с ID клиента и размером задолженности
#Если кредит выплачен - будет выведено сообщение о том, что кредит погашен
#Если срок депозита истек - будет выведено сообщение об окончании срока депозита и оставшейся сумме на счете
#Для сравнения, все результаты будут писаться в файл account_temp.csv
month_count = 50
bank_sum = account_int[0]
while month_count > 0:
    for i in account_cred_dep:
        if i['type'] == 'credit':
            account_int_id = account_int[i['id']]
            credit_id = credit[i['id']-1]
            if i['term'] == 0 and account_int_id['amount'] > 0:
                print("Дорогой клиент " + str(account_int_id['id']) + ", кредит погашен.")        
            elif i['term'] > 0:
                if i['term'] > 0 and account_int_id['amount'] >= 0:
                    account_int_id['amount'] -= int(credit_func(credit_id['sum'], credit_id['percent'], credit_id['term']))
                    bank_sum['amount'] += int(credit_func(credit_id['sum'], credit_id['percent'], credit_id['term']))
                    i['term'] -= 1
                elif account_int_id['amount'] <= 0:
                    print("Дорогой клиент " + str(account_int_id['id']) + ", погасите ваш кредит. Сумма задолжености " + str(account_int_id['amount']))
        elif i['type'] == 'deposit':
            account_int_id = account_int[i['id']]
            deposit_id = deposit[i['id']-1]
            if i['term'] > 0:
                account_int_id['amount'] += int(deposit_func(deposit_id['sum'], deposit_id['percent'], deposit_id['term']))
                bank_sum['amount'] -= int(deposit_func(deposit_id['sum'], deposit_id['percent'], deposit_id['term']))
                i['term'] -= 1
            else:
                print("Дорогой клиент " + str(account_int_id['id']) + ", срок депозита истек. Ваш остаток на счету: " + str(account_int_id['amount']))
        with open('/home/dmitriy_zh/dos14_master_project/account_temp.csv', 'w') as f:
            writer = csv.writer(f)
            header = ['id','amount']
            writer.writerow(header)
            for i in range(len(account)):
                account_id = account_int[i]
                account_to_csv = [account_id['id'],account_id['amount']]
                writer.writerow(account_to_csv)
    month_count -= 1
    time.sleep(1)
