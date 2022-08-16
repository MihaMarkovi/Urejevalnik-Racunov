import requests
from .models import Company, Bill, Product
from dateutil import parser


class GetRequest():
    def get_data(self):
        url = "https://apica.iplus.si/api/Naloga?API_KEY=F46F8FFF-D91E-4688-847C-E895EBE51171"
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
