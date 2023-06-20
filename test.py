import os, json, csv, time
import yaml
from account_clients import AccountClient

# #фунция расчета кредита
# def credit_func(sum, percent, term):
#     month_cred = (sum * (1 + percent / 100) ** term) / (term * 12)
#     return month_cred

# #функция расчета депозита
# def deposit_func(sum, percent, term):
#     month_dep =(sum * (1 + percent / 100) ** term) / (term * 12)
#     return month_dep

# account = []
# account_int =[]
# account_cred_dep =[]
# account_dep =[]


# #читаем файл account.csv и формируем список словарей
# with open('/home/dmitriy_zh/homework17/account.csv', 'r') as f:
#     reader = csv.reader(f)
#     for row in reader:
#        account.append({'id' : row[0], 'amount' : row[1]})
# account.remove({'id': 'id', 'amount': 'amount'})

# #приводим числовые значения к типу int
# for i in range(len(account)):
#     account_id = account[i]
#     account_int.append({'id' : int(account_id['id']), 'amount' : int(account_id['amount'])})
# account_int.sort(key = lambda x : x['id']) #сортируем список по id

# #читаем файл credit.json и формируем список словарей
# credit = []
# with open('/home/dmitriy_zh/homework17/credit.json', 'r') as f:
#     credit = json.loads(f.read())
# credit.sort(key = lambda x : x['id']) #сортируем список по id

# #читаем файл deposit.yaml и формируем список словарей
# deposit = []
# with open('/home/dmitriy_zh/homework17/deposit.yaml', 'r') as f:
#     deposit = yaml.safe_load(f)
# deposit.sort(key = lambda x : x['id']) #сортируем список по id

# # print(credit_func(), credit, deposit, sep='\n')

# # with open('/home/dmitriy_zh/homework17/account_temp.csv', 'w') as f:
# #     writer = csv.writer(f)
# #     header = ['id','amount']
# #     writer.writerow(header)
# #     for i in range(len(account)):
# #         account_id = account_int[i]
# #         print(account_id['id'])
# #         account_to_csv = [account_id['id'],account_id['amount']]
# #         account_to_csv_zero = [account_id['id'],'Warning!']
# #         print(account_to_csv)
# #         if account_id['amount'] == 0:
# #             writer.writerow(account_to_csv_zero)
# #         else:
# #             writer.writerow(account_to_csv)
# #         time.sleep(2)

# #добавляем сумму кредита на счета клиентов, удерживаем со счета банка
# # bank_account = account_int[0]
# # bank_account_sum = bank_account['amount']
# # for i in range(1, len(account_int)):
# #     credit_id = credit[i-1]
# #     account_int_id = account_int[i]
# #     bank_account_sum -= credit_id['sum']
# #     account_cred.append({'id' : account_int_id['id'], 'amount' : account_int_id['amount'] + credit_id['sum']})
# #     print(bank_account_sum) 
# # account_cred.append({'id' : 0, 'amount' : bank_account_sum})
# # account_cred.sort(key = lambda x : x['id'])
# # print(account_cred)

# # bank_account_cred = account_cred[0]
# # bank_sum_cred = bank_account_cred['amount']
# # for i in range(1, len(account_cred)):
# #     credit_id = credit[i-1]
# #     account_cred_id = account_cred[i]
# #     if credit_id['term'] == 0:
# #         credit_fee = 0
# #     else:
# #         credit_fee = (credit_id['sum'] * credit_id['percent']) // 3600
# #     bank_sum_cred += credit_fee
# #     account_cred.append({'id' : account_cred_id['id'], 'amount' : account_cred_id['amount'] - credit_fee})
# #     print(bank_sum_cred)
# # print(account_cred) 

# #раздаем кредиты, формируем список клиентов с кредитами
# for i in credit:
#     account_int_id = account_int[i['id']]
#     credit_id = credit[i['id']-1]
#     bank_sum = account_int[0]
#     if i['sum'] != 0:
#         account_int[i['id']] = {'id' : i['id'], 'amount' : account_int_id['amount'] + i['sum']}
#         bank_sum['amount'] -= i['sum']
#         account_cred_dep.append({'id' : i['id'], 'type' : 'credit', 'term' : credit_id['term'] * 12})
# account_int[0] = {'id' : 0, 'amount' : bank_sum['amount']}

# #формируем список клиентов с депозитами
# for i in deposit:
#     account_int_id = account_int[i['id']]
#     deposit_id = deposit[i['id']-1]
#     if i['sum'] != 0:
#         account_cred_dep.append({'id' : i['id'], 'type' : 'deposit', 'term' : deposit_id['term'] * 12})

# account_cred_dep.sort(key = lambda x : x['id'])

# print(account_cred_dep)
# print(account_int)

# month_count = 48
# bank_sum = account_int[0]
# while month_count > 0:
#     for i in account_cred_dep:
#         if i['type'] == 'credit':
#             account_int_id = account_int[i['id']]
#             credit_id = credit[i['id']-1]
#             if i['term'] == 0 and account_int_id['amount'] > 0:
#                 print("Дорогой клиент " + str(account_int_id['id']) + ", кредит погашен.")            
#             elif i['term'] > 0:
#                 if i['term'] > 0 and account_int_id['amount'] >= 0:
#                     account_int_id['amount'] -= int(credit_func(credit_id['sum'], credit_id['percent'], credit_id['term']))
#                     bank_sum['amount'] += int(credit_func(credit_id['sum'], credit_id['percent'], credit_id['term']))
#                     i['term'] -= 1
#                     print(i['term'])
#                 elif account_int_id['amount'] <= 0:
#                     print("Дорогой клиент " + str(account_int_id['id']) + ", погасите ваш кредит. Сумма задолжености " + str(account_int_id['amount']))
#         elif i['type'] == 'deposit':
#             account_int_id = account_int[i['id']]
#             deposit_id = deposit[i['id']-1]
#             if i['term'] > 0:
#                 account_int_id['amount'] += int(deposit_func(deposit_id['sum'], deposit_id['percent'], deposit_id['term']))
#                 bank_sum['amount'] -= int(deposit_func(deposit_id['sum'], deposit_id['percent'], deposit_id['term']))
#                 i['term'] -= 1
#             else:
#                 print("Дорогой клиент " + str(account_int_id['id']) + ", срок депозита истек. Ваш остаток на счету: " + str(account_int_id['amount']))
#         with open('/home/dmitriy_zh/homework17/account_temp1.csv', 'w') as f:
#             writer = csv.writer(f)
#             header = ['id','amount']
#             writer.writerow(header)
#             for i in range(len(account)):
#                 account_id = account_int[i]
#                 account_to_csv = [account_id['id'],account_id['amount']]
#                 writer.writerow(account_to_csv)
#     month_count -= 1
#     time.sleep(1)
#     # if i['type'] == 'credit':
#     #     # account_int[i['id']] = {'id' : i['id'], 'amount' : 'credit here'}
#     #     while credit_id['term'] != 0:
#     #         # account_int[i['id']] = {'id' : i['id'], 'amount' : account_int_id['amount'] - credit_func(credit_id['sum'], credit_id['percent'], credit_id['term'])}
#     #         # bank_sum['amount'] += credit_func(credit_id['sum'], credit_id['percent'], credit_id['term'])
#     #         print(bank_sum['amount'])
#     #         credit_id['term'] -= 1
            
#     #         if account_int_id['amount'] <= 0:
#     #             print("Дорогой клиент " + str(account_int_id['id']) + ", погасите ваш кредит. Сумма задолжености " + account_int_id['sum'])
#     #     else:
#     #         print("Дорогой клиент " + str(account_int_id['id']) + ", Ваш кредит погашен")
#     # elif i['type'] == 'deposit':
#     #     while deposit_id['term'] != 0:
#     #         account_int[i['id']] = {'id' : i['id'], 'amount' : account_int_id['amount'] + deposit_func(deposit_id['sum'], deposit_id['percent'], deposit_id['term'])}
#     #         bank_sum['amount'] -= deposit_func(deposit_id['sum'], deposit_id['percent'], deposit_id['term'])
#     #         print(account_int[i['id']])



# # print(account_int)

# # with open('/home/dmitriy_zh/homework17/account_temp.csv', 'w') as f:
# #     writer = csv.writer(f)
# #     header = ['id','amount']
# #     writer.writerow(header)
# #     for i in range(len(account)):
# #         account_id = account_int[i]
# #         account_to_csv = [account_id['id'],account_id['amount']]
# #         writer.writerow(account_to_csv)


cred_dep_base = []

class BankProduct:
    def __init__(self, entity_id, percent, term, sum):
        # self.__entity_id = entity_id
        self.__percent = percent
        self.__term = term
        self.__sum = sum
        self.__end_sum = self.__sum * (1 + (self.__percent / 100) ** self.__term)
        self.__end_sum_dep = self.__sum + (self.__sum * self.__percent * self.__term )/ 100 

    def end_sum(self):
        return self.__end_sum 
    
    def end_sum_dep(self):
        return self.__end_sum_dep
    
    def sum(self):
        return self.__sum

    def process(self):
        pass

class Credit(BankProduct):
    def __init__(self, entity_id, percent, term, sum, periods):
        BankProduct.__init__(self, entity_id, percent, term, sum)
        self.__entity_id = entity_id
        self.__periods = periods
        self.__closed = False
        self.montly_fee = int(BankProduct.end_sum(self) / (term * 12))

    def close(self):
        return self.__closed
    
    def periods(self):
        return self.__periods
    
    def process(self):
        with open('/home/dmitriy_zh/homework18/account_temp.csv', 'a') as f:
            writer = csv.writer(f)
            w = credit['credit']
            if i['periods'] == 0:
                self.__closed = True
            else:
                wr = [self.__entity_id, self.montly_fee, 'substract']
                writer.writerow(wr)
                wr = ['0', a.montly_fee, 'add']
                writer.writerow(wr)
                self.__periods -= 1
                print(self.__entity_id, self.__periods)
            f.close()

        # return self.montly_fee
    
class Deposit(BankProduct):
    def __init__(self, entity_id, percent, term, sum, periods):
        BankProduct.__init__(self, entity_id, percent, term, sum)
        self.__periods = periods
        self.__closed = False
        self.__entity_id = entity_id
        self.montly_fee = int((BankProduct.end_sum_dep(self) - BankProduct.sum(self)) / (term * 12))
    
    def periods(self):
        return self.__periods
    
    def close(self):
        return self.__closed
    
    def process(self):
         with open('/home/dmitriy_zh/homework18/account_temp.csv', 'a') as f:
            writer = csv.writer(f)
            w = credit['credit']
            if self.__periods == 0:
                self.__closed = True
            else:
                wr = [self.__entity_id, b.montly_fee, 'substract']
                writer.writerow(wr)
                wr = ['0', b.montly_fee, 'add']
                writer.writerow(wr)
                self.__periods -= 1
                print(self.__entity_id, self.__periods)
            f.close()

        


with open('/home/dmitriy_zh/homework18/credits_deposits.json', 'r') as f:
    credit = json.loads(f.read())


for i in credit['credit']:
    cred_dep_base.append({'entity_id': int(i['entity_id']), 'percent': int(i['percent']), 'sum': int(i['sum']), 'term': int(i['term']), 'type': 'credit', 'periods' : int(i['term']) * 12})
    print(i)

for i in credit['deposit']:
    cred_dep_base.append({'entity_id': int(i['entity_id']), 'percent': int(i['percent']), 'sum': int(i['sum']),'term': int(i['term']), 'type': 'deposit', 'periods' : int(i['term']) * 12})
    print(i)

# print(cred_dep_base)
# cred_dep_base.sort(key = lambda x : x['entity_id'])
# print(cred_dep_base)


for i in cred_dep_base:
    print(i['type'])

month_term = 50


while month_term > 0:
    for i in cred_dep_base:
        if i['type'] == 'credit':    
            a = Credit(i['entity_id'], i['percent'], i['term'], i['sum'], i['periods'])
            a.process()
            i['periods'] = a.periods()
            if a.close() == True:
                if {'entity_id': i['entity_id'], 'percent': i['percent'], 'sum': i['sum'], 'term': i['term']} in credit['credit']:
                    print(str(i['entity_id']) + ' is closed')
                    credit['credit'].remove({'entity_id': i['entity_id'], 'percent': i['percent'], 'sum': i['sum'], 'term': i['term']})
                else:
                    print(str(i['entity_id']) + ' is closed')
        elif i['type'] == 'deposit':
            b = Deposit(i['entity_id'], i['percent'], i['term'], i['sum'], i['periods'])
            b.process()
            i['periods'] = b.periods()
            if b.close() == True:
                if {'entity_id': i['entity_id'], 'percent': i['percent'], 'sum': i['sum'], 'term': i['term']} in credit['deposit']:
                    print(str(i['entity_id']) + ' is closed')
                    credit['deposit'].remove({'entity_id': i['entity_id'], 'percent': i['percent'], 'sum': i['sum'], 'term': i['term']})
                else:
                    print(str(i['entity_id']) + ' is closed')
    print('Months left: ' + str(month_term - 1))
    with open('/home/dmitriy_zh/homework18/credits_deposits_temp.json', 'w') as f:
        # credit = json.loads(f.read())
        json.dump(credit, f)
    month_term -= 1
    time.sleep(1)





