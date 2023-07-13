import json, csv, time

cred_dep_base = [] #список всех наших кредитов и депозитов с учетом оставшегося срока окончания

class BankProduct:
    def __init__(self, entity_id, percent, term, sum):
        self.__entity_id = entity_id
        self.__percent = percent
        self.__term = term
        self.__sum = sum
        self.__end_sum = self.__sum * (1 + (self.__percent / 100) ** self.__term)
        self.__end_sum_dep = self.__sum + (self.__sum * self.__percent * self.__term )/ 100 

    #функция возвращает значение итоговой суммы с учетом кредита
    def end_sum(self):
        return self.__end_sum 
    
    #функция возвращает значение итоговой суммы с учетом депозита
    def end_sum_dep(self):
        return self.__end_sum_dep
    
    #функция возвращает значение изначальной суммы на счету
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
        self.montly_fee = int(BankProduct.end_sum(self) / (term * 12)) #расчет месячного взноса

    def credit_status(self):
        return self.__closed
    
    def periods(self):
        return self.__periods
    
    #Функция записывает все транзакции по кредитам в файл transactions.csv, если срок кредита истек - параметр closed меняется на True
    def process(self):
        with open('./transactions.csv', 'a') as f:
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

    
class Deposit(BankProduct):
    def __init__(self, entity_id, percent, term, sum, periods):
        BankProduct.__init__(self, entity_id, percent, term, sum)
        self.__periods = periods
        self.__closed = False
        self.__entity_id = entity_id
        self.montly_fee = int((BankProduct.end_sum_dep(self) - BankProduct.sum(self)) / (term * 12)) #расчет месячного взноса
    
    def periods(self):
        return self.__periods
    
    def deposit_status(self):
        return self.__closed
    
    #Функция записывает все транзакции по депозитам в файл transactions.csv, если срок депозита истек - параметр closed меняется на True
    def process(self):
         with open('./transactions.csv', 'a') as f:
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


with open('./credits_deposits.json', 'r') as f:
    credit = json.loads(f.read()) #переносим файл БД credits_deposits.json как словарь

#наполняем список кредитами
for i in credit['credit']:
    cred_dep_base.append({'entity_id': int(i['entity_id']), 'percent': int(i['percent']), 'sum': int(i['sum']), 'term': int(i['term']), 'type': 'credit', 'periods' : int(i['term']) * 12})

#наполняем список депозитами
for i in credit['deposit']:
    cred_dep_base.append({'entity_id': int(i['entity_id']), 'percent': int(i['percent']), 'sum': int(i['sum']), 'term': int(i['term']), 'type': 'deposit', 'periods' : int(i['term']) * 12})


#Цикл длится 50 месяцев
#Цикл проходит по базе cred_dep_base, если элемент - кредит, создает объект класса Credit, передает ему параметры entity_id, percent, term, sum, periods, вызывает функцию process
#Чтобы срок корректно уменьшался, после обработки функции process, мы явно присваиваем элементу periods значение, полученное после уменьшения на 1 в функции process
#Если срок истек - удаляется из БД credit и выводится на экран <ID> is closed, если объект уже удален и срок истек - просто выводится сообщение
#Аналогично и для депозита
#В конце каждого месяца актуальная БД credit записывается в файл credits_deposits_temp.json
month_term = 50 
while month_term > 0:
    for i in cred_dep_base:
        if i['type'] == 'credit':    
            a = Credit(i['entity_id'], i['percent'], i['term'], i['sum'], i['periods'])
            a.process()
            i['periods'] = a.periods()
            if a.credit_status() == True:
                if {'entity_id': i['entity_id'], 'percent': i['percent'], 'sum': i['sum'], 'term': i['term']} in credit['credit']:
                    print(str(i['entity_id']) + ' is closed')
                    credit['credit'].remove({'entity_id': i['entity_id'], 'percent': i['percent'], 'sum': i['sum'], 'term': i['term']})
                else:
                    print(str(i['entity_id']) + ' is closed')
        elif i['type'] == 'deposit':
            b = Deposit(i['entity_id'], i['percent'], i['term'], i['sum'], i['periods'])
            b.process()
            i['periods'] = b.periods()
            if b.deposit_status() == True:
                if {'entity_id': i['entity_id'], 'percent': i['percent'], 'sum': i['sum'], 'term': i['term']} in credit['deposit']:
                    print(str(i['entity_id']) + ' is closed')
                    credit['deposit'].remove({'entity_id': i['entity_id'], 'percent': i['percent'], 'sum': i['sum'], 'term': i['term']})
                else:
                    print(str(i['entity_id']) + ' is closed')
    print('MOnths left: ' + str(month_term - 1))
    with open('./credits_deposits_temp.json', 'w') as f:
        json.dump(credit, f)
    month_term -= 1
    time.sleep(1)