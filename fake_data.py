from faker import Faker
import json
from datetime import datetime
from open_search_config import config 

fake = Faker('en_GB')

mapping = {
    "properties": {
        "id_transaction": {"type": "keyword"}, 
        "date": {"type": "date"},               
        "type": {"type": "keyword"},            
        "description": {"type": "text"},       
        "amount": {"type": "double"},          
        "currency": {"type": "keyword"},    
        "balance_after_transaction": {"type": "double"},  
        "details": {
            "type": "nested",
            "properties": {
                "sender": {"type": "text"},           
                "recipient": {"type": "text"},        
                "IBAN_sender": {"type": "keyword"},     
                "IBAN_recipient": {"type": "keyword"} 
            }
        },
        "category": {"type": "keyword"},    
        "notes": {"type": "text"}      
    }
}

template_body = {
  "template": {
    "settings": {
      "number_of_shards": 1
    },
    "mappings": mapping,
  },
  "index_patterns": ["transaction-2024-*"],
  "priority": 500,
  "composed_of": []
}

config.client.indices.put_index_template(name="transaction_template", body=template_body)

def generate_fake_transaction(index_name):
    id_transaction = "TRX" + "".join(fake.random_letters(length=10)).upper()
    year, month = index_name.split("-")[1:3]
    if month == "06":
        start_date = datetime(year=int(year), month=6, day=1)
        end_date = datetime(year=int(year), month=6, day=30)
    elif month == "07":
        start_date = datetime(year=int(year), month=7, day=1)
        end_date = datetime(year=int(year), month=7, day=31)
    else:
        today = datetime.today()
        start_date = today.replace(day=1)
        end_date = today
    
    date = fake.date_between(start_date=start_date, end_date=end_date).isoformat()
    typeTransaction = fake.random_element(elements=("Incoming transfer", "Outgoing transfer"))
    description = "Salary March" if type == "Incoming transfer" else "Supplier Payment"
    amount = round(fake.random_number(digits=4), 2)
    currency = "EUR"
    balance_after_transaction = round(amount + fake.random_number(digits=4), 2)
    details = {
        "sender": fake.company(),
        "recipient": fake.name(),
        "IBAN_sender": fake.iban(),
        "IBAN_recipient": fake.iban()
    }
    category = "Entrate" if typeTransaction == "Incoming transfer" else "Expenses"
    notes =  "Monthly salary credit" if typeTransaction == "Incoming transfer" else "Monthly payment to supplier"

    return {
        "id_transaction": id_transaction,
        "date": date,
        "typeTransaction": typeTransaction,
        "description": description,
        "amount": amount,
        "currency": currency,
        "balance_after_transaction": balance_after_transaction,
        "details": details,
        "category": category,
        "notes": notes
    }
    
def populate_index(index_name):
    for _ in range(10):
        doc = generate_fake_transaction(index_name)
        config.client.index(index=index_name, body=json.dumps(doc))
    print(f"Populated index {index_name} with fake data.")

indices = ["transactions-2024-06", "transactions-2024-07"]

for index in indices:
    populate_index(index)