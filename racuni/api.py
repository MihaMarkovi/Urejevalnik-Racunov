import os

import requests
from datetime import datetime
from .models import Company, Bill, Product
from dateutil import parser
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("API_KEY")


class GetRequest():
    def get_data(self):
        url = f"https://apica.iplus.si/api/Naloga?API_KEY={API_KEY}"
        response = requests.get(url)
        data = response.json()

        data = data['Data']

        company_data = data['a'].split('#')
        title = company_data[0]

        address = company_data[1]
        post_office = company_data[2]
        ddv_id = company_data[3]
        companies = Company.objects.filter(title=title, address=address, post_office=post_office, ddv_id=ddv_id)
        if companies.count() == 0:
            company = Company(title=title, address=address, post_office=post_office, ddv_id=ddv_id)
            company.save()

        eor = data['g']
        bills = Bill.objects.filter(eor=eor)
        if bills.count() == 0:
            bill_number = data['c']
            producer = Company.objects.get(title=title)
            seller = data['b']
            last_updated = parser.parse(data['d'])
            tax_level = data['e']
            zoi = data['f']
            status = data['h']
            if status == 1:
                status = False
            else:
                status = True

            bill = Bill(eor=eor, bill_number=bill_number, producer=producer, seller=seller, last_updated=last_updated,
                        tax_level=tax_level, zoi=zoi,
                        status=status)
            bill.save()

            products = data['z']
            for product in products:
                product_title = product['a']
                quantity = product['b']
                value = product['c']
                p = Product(bill=Bill.objects.get(eor=eor), product_title=product_title, quantity=quantity, value=value)
                p.save()


class PostRequest():
    def send_data(eor):
        bill = Bill.objects.get(eor=eor)
        products = Product.objects.filter(bill__eor=eor)

        company = Company.objects.get(pk=bill.producer.pk)
        company_string = "%s#%s#%s#%s" % (company.title, company.address, company.post_office, company.ddv_id)

        last_updated = bill.last_updated.astimezone().strftime('%Y-%m-%dT%H:%M:%S%z')
        last_updated = last_updated[:22] + ':' + last_updated[22:]

        if bill.status:
            status = 5
        else:
            status = 1

        products_list = []
        for product in products:
            pro = {
                "a": product.product_title,
                "b": product.quantity,
                "c": product.value
            }
            products_list.append(pro)

        data = {
            "a": company_string,
            "b": bill.seller,
            "c": bill.bill_number,
            "d": last_updated,
            "e": bill.tax_level,
            "f": bill.zoi,
            "g": bill.eor,
            "h": status,
            "z": products_list
        }

        url = f"https://apica.iplus.si/api/Naloga?API_KEY={API_KEY}"
        r = requests.post(url, json=data)
