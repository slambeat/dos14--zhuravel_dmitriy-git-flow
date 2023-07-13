import os, json, csv, time
import yaml
from account_clients import AccountClient

from flask import Flask, abort, make_response, request
app = Flask(__name__)
import threading

def FlaskThread():
    app.run()

if __name__ == '__main__':
    threading.Thread(target=FlaskThread).start()

cred_dep_base = []                
counter = 1

class BankProduct:
    def __init__(self, client_id, percent, term, sum):
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
    def __init__(self, client_id, percent, term, sum, periods):
        BankProduct.__init__(self, client_id, percent, term, sum)
        self.__client_id = client_id
        self.__periods = periods
        self.__closed = False
        self.montly_fee = int(BankProduct.end_sum(self) / (term * 12))

    def close(self):
        return self.__closed
    
    def periods(self):
        return self.__periods

    def client_id(self):
        return self.__client_id    


    def process(self):
        while counter > 0:
            AccountClientObj = AccountClient(self.__client_id)
            AccountClientObj.transaction(substract=self.montly_fee)
            time.sleep(1)  

class Deposit(BankProduct):
    def __init__(self, client_id, percent, term, sum, periods):
        BankProduct.__init__(self, client_id, percent, term, sum)
        self.__periods = periods
        self.__closed = False
        self.__client_id = client_id
        self.montly_fee = int((BankProduct.end_sum_dep(self) - BankProduct.sum(self)) / (term * 12))
    
    def periods(self):
        return self.__periods
    
    def close(self):
        return self.__closed
    
    def process(self):
        while counter > 0:
            AccountClientObj = AccountClient(self.__client_id)
            AccountClientObj.withdraw = False
            AccountClientObj.transaction(add=self.montly_fee)
            time.sleep(1)

        

with open('credits_deposits.yaml', 'r') as f:
    credit = yaml.safe_load(f)

print(credit)


for i in credit['credit']:
    cred_dep_base.append({'client_id': int(i['client_id']), 'percent': int(i['percent']), 'sum': int(i['sum']), 'term': int(i['term']), 'type': 'credit', 'periods' : int(i['periods'])})
    print(i)

for i in credit['deposit']:
    cred_dep_base.append({'client_id': int(i['client_id']), 'percent': int(i['percent']), 'sum': int(i['sum']),'term': int(i['term']), 'type': 'deposit', 'periods' : int(i['periods'])})
    print(i)

print(cred_dep_base)

id_list_cred = []
id_list_dep = []
for i in cred_dep_base:
    if i['type'] == 'credit':
        id_list_cred.append(i['client_id'])
        print(id_list_cred)
    if i['type'] == 'deposit':
        id_list_dep.append(i['client_id'])
        print(id_list_dep)


@app.route("/api/v1/accounts", methods=["GET"])
def read_account():
    return cred_dep_base

@app.route("/api/v1/deposit/<int:client_id>", methods=["GET"])
def read_deposit(client_id):
    response = make_response({"status": "error", "message": f"Client {client_id} does not have active deposits"})
    response.status = 400
    for i in cred_dep_base:
        if i['client_id'] == int(client_id) and i['type'] == 'deposit':
            return i
        else:
            return response

@app.route("/api/v1/credit/<int:client_id>", methods=["GET"])
def read_credit(client_id):
    response = make_response({"status": "error", "message": f"Client {client_id} does not have active credits"})
    response.status = 400
    for i in cred_dep_base:
        if i['client_id'] == int(client_id) and i['type'] == 'credit':
            return i
        else:
            return response

@app.route("/api/v1/credits", methods=["GET"])
def read_credit_all():
    all_cred = []
    for i in cred_dep_base:
        if i['type'] == 'credit':
            all_cred.append(i)
    return all_cred


@app.route("/api/v1/deposits", methods=["GET"])
def read_deposit_all():
    all_dep = []
    for i in cred_dep_base:
        if i['type'] == 'deposit':
            all_dep.append(i)
    return all_dep

@app.route("/api/v1/credits", methods=["PUT"])
def create_credit():
    new_credit = request.json
    client_id = new_credit['client_id']
    response = make_response({"status": "error", "message": f'Credit for client {client_id} already exists'})
    response.status = 400
    if new_credit['client_id'] in id_list_cred:
        return response
    else:
        credit_data ={
            "client_id": new_credit['client_id'],
            "percent": new_credit['percent'],
            "periods": -1,
            "sum": new_credit['sum'],
            "term": new_credit['term']
        }
        credit['credit'].append(credit_data)        
        id_list_cred.append(new_credit['client_id'])
        with open('credits_deposits.yaml', 'w') as f:
            yaml.dump(credit, f)
        return credit
                   

@app.route("/api/v1/deposits", methods=["PUT"])
def create_deposit():
    new_deposit = request.json
    client_id = new_deposit['client_id']
    response = make_response({"status": "error", "message": f'Deposit for client {client_id} already exists'})
    response.status = 400
    if new_deposit['client_id'] in id_list_dep:
        return response
    else:
        deposit_data ={
            "client_id": new_deposit['client_id'],
            "percent": new_deposit['percent'],
            "periods": -1,
            "sum": new_deposit['sum'],
            "term": new_deposit['term']
            }
        credit['deposit'].append(deposit_data)
        id_list_dep.append(new_deposit['client_id'])
        with open('credits_deposits.yaml', 'r') as f:
            json.dump(credit, f)
        return credit

for i in cred_dep_base:
    if i['type'] == 'credit':    
        thread = threading.Thread(target=Credit.process, args=(Credit(i['client_id'], i['percent'], i['term'], i['sum'], i['periods']),))
        thread.start()
    elif i['type'] == 'deposit':
        thread = threading.Thread(target=Deposit.process, args=(Deposit(i['client_id'], i['percent'], i['term'], i['sum'], i['periods']),))
        thread.start()







