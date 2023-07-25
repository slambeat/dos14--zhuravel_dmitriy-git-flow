import os, json, csv, time
import yaml
from account_clients import AccountClient

from flask import Flask, abort, make_response, request
app = Flask(__name__)
import threading

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
        AccountClientObj = AccountClient(self.__client_id)
        BankObj = AccountClient(0)
        AccountClientObj.transaction(substract=self.montly_fee)
        BankObj.transaction(add=self.montly_fee)


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
        AccountClientObj = AccountClient(self.__client_id)
        AccountClientObj.withdraw = False
        BankObj = AccountClient(0)
        AccountClientObj.transaction(add=self.montly_fee)
        BankObj.transaction(substract=self.montly_fee)
       

with open('credits_deposits.yaml', 'r') as f:
    credit = yaml.safe_load(f)

#Этот блок только для заполнения periods, выполняется только если term=-1
for i in credit['credit']:
    if i['periods'] == -1:
        i['periods'] = i['term'] * 12
    with open('credits_deposits.yaml', 'w') as f:
        yaml.dump(credit, f)

for i in credit['deposit']:
    if i['periods'] == -1:
        i['periods'] = i['term'] * 12
    with open('credits_deposits.yaml', 'w') as f:
        yaml.dump(credit, f)

with open('credits_deposits.yaml', 'w') as f:
    yaml.dump(credit, f)

id_list_cred = []
id_list_dep = []

for i in credit['credit']:
    id_list_cred.append(i['client_id'])

for i in credit['deposit']:
    id_list_dep.append(i['client_id'])


@app.route("/api/v1/deposit/<int:client_id>", methods=["GET"])
def read_deposit(client_id):
    response = make_response({"status": "error", "message": f"Client {client_id} does not have active deposits"})
    response.status = 400
    response_not_found = make_response({"status": "error", "message": f"There is no such client in the base"})
    response_not_found.status = 404
    for i in credit['deposit']:
        if i['client_id'] == int(client_id):
            return i
        elif i['client_id'] == int(client_id) and int(client_id) not in id_list_dep:
            return response
        elif int(client_id) not in id_list_cred and int(client_id) not in id_list_dep:
            return response_not_found

@app.route("/api/v1/credit/<int:client_id>", methods=["GET"])
def read_credit(client_id):
    response = make_response({"status": "error", "message": f"Client {client_id} does not have active credits"})
    response.status = 400
    response_not_found = make_response({"status": "error", "message": f"There is no such client in the base"})
    response_not_found.status = 404
    for i in credit['credit']:
        if i['client_id'] == int(client_id):
            return i
        elif i['client_id'] == int(client_id) and int(client_id) not in id_list_cred:
            return response
        elif int(client_id) not in id_list_cred and int(client_id) not in id_list_dep:
            return response_not_found

@app.route("/api/v1/credits", methods=["GET"])
def read_credit_all():
    all_cred = []
    for i in credit['credit']:
        all_cred.append(i)
    return all_cred


@app.route("/api/v1/deposits", methods=["GET"])
def read_deposit_all():
    all_dep = []
    for i in credit['deposit']:
        all_dep.append(i)
    return all_dep

# curl --request PUT --header 'Content-Type: application/json' --data '{"client_id": 27, "percent": 13, "sum": 100000, "term": 2}' localhost:5000/api/v1/credits
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
            "periods": new_credit['term'] * 12,
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
            "periods": new_deposit['term'] * 12,
            "sum": new_deposit['sum'],
            "term": new_deposit['term']
            }
        credit['deposit'].append(deposit_data)
        id_list_dep.append(new_deposit['client_id'])
        with open('credits_deposits.yaml', 'w') as f:
            json.dump(credit, f)
        return credit

def process_thread():
    while id_list_cred != [] or id_list_dep != []:               
        for i in credit['credit']:
            if i['periods'] == 0:
                credit_data ={
                    "client_id": i['client_id'],
                    "percent": i['percent'],
                    "periods": i['periods'],
                    "sum": i['sum'],
                    "term": i['term'],
                }
                credit['credit'].remove(credit_data)
                id_list_cred.remove(i['client_id'])
            elif i['periods'] > 0:
                obj = Credit(i['client_id'], i['percent'], i['term'], i['sum'], i['periods'])
                obj.process()
                i['periods'] -= 1
        for i in credit['deposit']:
            if i['periods'] == 0:
                deposit_data ={
                    "client_id": i['client_id'],
                    "percent": i['percent'],
                    "periods": i['periods'],
                    "sum": i['sum'],
                    "term": i['term'],
                }
                credit['deposit'].remove(deposit_data)
                id_list_dep.remove(i['client_id'])
            elif i['periods'] > 0:
                obj = Deposit(i['client_id'], i['percent'], i['term'], i['sum'], i['periods'])
                obj.process()
                i['periods'] -= 1
        with open('credits_deposits.yaml', 'w') as f:
            yaml.dump(credit, f)
        time.sleep(1)

def base_check():
    while True:
        if id_list_cred != [] or id_list_dep != []:
            process_thread()

thread = threading.Thread(target=base_check)
thread.start()