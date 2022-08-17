import requests
from django.shortcuts import render, redirect
from django.views import generic
from django.views.generic.edit import FormMixin
from .models import Bill, Company, Product
from .forms import BillDetailsForm, ProductDetailsForm, CompanyDetailsForm
from datetime import datetime
from .api import GetRequest, PostRequest


class IndexView(generic.ListView):
    template_name = 'racuni/index.html'
    context_object_name = 'bills_list'

    def get_queryset(self):
        GetRequest().get_data()
        return Bill.objects.filter(status=False).order_by('-last_updated')


class BillDetailsView(FormMixin, generic.DetailView):
    model = Bill
    template_name = 'racuni/bill_details.html'
    form_class = BillDetailsForm

    def get_initial(self):
        obj = self.get_object()
        return {'eor': obj.eor, 'producer': obj.producer, 'bill_number': obj.bill_number, 'seller': obj.seller,
                'tax_level': obj.tax_level, 'zoi': obj.zoi, 'status': obj.status}

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['products'] = Product.objects.filter(bill__eor=self.kwargs['pk'])
        return context

    def post(self, request, *args, **kwargs):
        form = BillDetailsForm(request.POST)

        if form.is_valid():
            eor = form.cleaned_data['eor']
            b = Bill.objects.get(eor=eor)
            b.producer = Company.objects.get(title=form.cleaned_data['producer'])
            b.bill_number = form.cleaned_data['bill_number']
            b.seller = form.cleaned_data['seller']
            b.tax_level = form.cleaned_data['tax_level']
            b.zoi = form.cleaned_data['zoi']
            b.status = form.cleaned_data['status']
            b.last_updated = datetime.now()
            b.save()

            if b.status:
                PostRequest.send_data(eor)
                return redirect('index')

            return redirect('bill-details', b.eor)


class ProductsDetailsView(FormMixin, generic.DetailView):
    model = Product
    template_name = 'racuni/product_details.html'
    form_class = ProductDetailsForm

    def get_initial(self):
        obj = self.get_object()
        return {'product_title': obj.product_title, 'quantity': obj.quantity, 'value': obj.value}

    def post(self, request, *args, **kwargs):
        form = ProductDetailsForm(request.POST)

        if form.is_valid():
            p = Product.objects.get(pk=self.kwargs['pk'])
            b = Bill.objects.get(eor=self.kwargs['bill_id'])
            p.product_title = form.cleaned_data['product_title']
            p.quantity = form.cleaned_data['quantity']
            p.value = form.cleaned_data['value']
            b.last_updated = datetime.now()
            p.save()
            b.save()

            args = {'form': form, 'product': p}
            return render(request, self.template_name, args)


class CompanyDeleteConfirmView(generic.TemplateView):
    template_name = 'racuni/confirm_company_delete.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['bills'] = Bill.objects.filter(producer_id=self.kwargs['pk'])
        context['company'] = Company.objects.get(pk=self.kwargs['pk'])
        return context

    def post(self, request, *args, **kwargs):
        company = Company.objects.filter(pk=self.kwargs['pk'])
        company.delete()
        return redirect('companies')


class ProductDeleteConfirmView(generic.TemplateView):
    template_name = 'racuni/confirm_product_delete.html'

    def get(self, request, *args, **kwargs):
        product = Product.objects.get(pk=kwargs['pk'])
        args = {'product': product}
        return render(request, self.template_name, args)

    def post(self, request, *args, **kwargs):
        product = Product.objects.filter(pk=self.kwargs['pk'])
        product.delete()
        return redirect('bill-details', self.kwargs['bill_id'])


class CompanyView(generic.ListView):
    template_name = 'racuni/companies.html'
    context_object_name = 'companies_list'

    def get_queryset(self):
        return Company.objects.order_by('pk')


class CompanyDetailsView(FormMixin, generic.DetailView):
    model = Company
    template_name = 'racuni/company_details.html'
    form_class = CompanyDetailsForm

    def get_initial(self):
        obj = self.get_object()
        return {'title': obj.title, 'address': obj.address, 'post_office': obj.post_office, 'ddv_id': obj.ddv_id}

    def post(self, request, *args, **kwargs):
        form = CompanyDetailsForm(request.POST)

        if form.is_valid():
            c = Company.objects.get(pk=kwargs['pk'])
            c.title = form.cleaned_data['title']
            c.address = form.cleaned_data['address']
            c.post_office = form.cleaned_data['post_office']
            c.ddv_id = form.cleaned_data['ddv_id']
            c.save()

            args = {'form': form, 'company': c}
            return render(request, self.template_name, args)


class AddNewCompany(FormMixin, generic.TemplateView):
    template_name = 'racuni/add_company.html'
    form_class = CompanyDetailsForm

    def post(self, request, *args, **kwargs):
        form = CompanyDetailsForm(request.POST)

        if form.is_valid():
            f = Company(title=form.cleaned_data['title'], address=form.cleaned_data['address'],
                        post_office=form.cleaned_data['post_office'], ddv_id=form.cleaned_data['ddv_id'])
            f.save()
            return redirect('companies')


class AddNewProduct(FormMixin, generic.TemplateView):
    template_name = 'racuni/add_product.html'
    form_class = ProductDetailsForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['bill'] = Bill.objects.get(eor=self.kwargs['bill_id'])
        return context

    def post(self, request, *args, **kwargs):
        form = ProductDetailsForm(request.POST)

        if form.is_valid():
            f = Product(bill=Bill.objects.get(eor=self.kwargs['bill_id']),
                        product_title=form.cleaned_data['product_title'],
                        quantity=form.cleaned_data['quantity'], value=form.cleaned_data['value'])
            f.save()
            return redirect('bill-details', self.kwargs['bill_id'])


class HistoryView(generic.ListView):
    template_name = 'racuni/history.html'
    context_object_name = 'bills_list'

    def get_queryset(self):
        return Bill.objects.filter(status=True)


class OutputView(generic.TemplateView):
    template_name = 'racuni/output.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        try:
            last_bill = Bill.objects.filter(status=True).latest('last_updated')
            valid_products = Product.objects.filter(bill=last_bill)

            total_price = 0
            for product in valid_products:
                total_price += product.value

            context['total_price'] = total_price
            context['no_tax'] = total_price - total_price * last_bill.tax_level
            context['ddv'] = total_price * last_bill.tax_level
            context['latest_bill'] = last_bill
            context['latest_products'] = valid_products
            return context
        except:
            return context
