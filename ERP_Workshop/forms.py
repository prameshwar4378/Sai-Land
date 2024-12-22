from django import forms
from django.core.exceptions import ValidationError
from ERP_Admin.models import Purchase, PurchaseItem,Product,Model,JobCard,JobCardItem

class PurchaseForm(forms.ModelForm):
    class Meta:
        model = Purchase
            
        fields = ['bill_no','bill_date','bill_type', 'supplier_name', 'bill_file']
        widgets={ 
            'bill_date': forms.TextInput(attrs={'type': 'date' })
        }

    def clean_bill_no(self):
        bill_no = self.cleaned_data.get('bill_no')
        if not bill_no:
            raise ValidationError("Bill number is required.")
        if len(bill_no) < 5:
            raise ValidationError("Bill number must be at least 5 characters long.")
        # Check for uniqueness
        if not self.instance.pk:  # self.instance.pk is None when the instance is new
            if Purchase.objects.filter(bill_no=bill_no).exists():
                raise ValidationError('Bill number must be unique.')
        return bill_no

    def clean_supplier_name(self):
        supplier_name = self.cleaned_data.get('supplier_name')
        if supplier_name and len(supplier_name) < 3:
            raise ValidationError("Supplier name must be at least 3 characters long.")
        return supplier_name
  


class UpdatePurchaseForm(forms.ModelForm):
    class Meta:
        model = Purchase
            
        fields = ['bill_date','bill_type', 'supplier_name', 'bill_file']
        widgets={ 
            'bill_date': forms.TextInput(attrs={'type': 'date' })
        }

 
class ProductForm(forms.ModelForm):

    class Meta:
        model = Product
        fields = [
            'product_code',
            'model',
            'product_name',
            'description',
            'sale_price',
            'minimum_stock_alert',
            'available_stock',
            'product_image',
        ]
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4, 'cols': 40}),
        }
        
    def __init__(self, *args, **kwargs):
        super(ProductForm, self).__init__(*args, **kwargs)
        self.fields['model'].required = False

    def clean_product_code(self):
        product_code = self.cleaned_data.get('product_code')
        if not product_code:
            raise ValidationError("Product code is required.")
        if len(product_code) > 20:
            raise ValidationError("Product code cannot exceed 20 characters.")
        return product_code

    def clean_product_name(self):
        product_name = self.cleaned_data.get('product_name')
        if not product_name:
            raise ValidationError("Product name is required.")
        if len(product_name) > 100:
            raise ValidationError("Product name cannot exceed 100 characters.")
        return product_name

    def clean_sale_price(self):
        sale_price = self.cleaned_data.get('sale_price')
        if sale_price is None:
            raise ValidationError("Sale price is required.")
        if sale_price <= 0:
            raise ValidationError("Sale price must be greater than zero.")
        return sale_price

    def clean_minimum_stock_alert(self):
        minimum_stock_alert = self.cleaned_data.get('minimum_stock_alert')
        if minimum_stock_alert < 0:
            raise ValidationError("Minimum stock alert cannot be negative.")
        return minimum_stock_alert

    def clean_available_stock(self):
        available_stock = self.cleaned_data.get('available_stock')
        if available_stock < 0:
            raise ValidationError("Available stock cannot be negative.")
        return available_stock
    
    def clean_product_image(self):
        product_image = self.cleaned_data.get('product_image')
        if product_image:
            # Validate image size (max 500 KB)
            if product_image.size > 500 * 1024:
                raise ValidationError("Image size must not exceed 500 KB.")
            # Validate image type (optional) 
        return product_image


class PurchaseItemForm(forms.ModelForm):
    class Meta:
        model = PurchaseItem
        fields = ['quantity', 'cost_per_unit', 'total_amount']
        widgets = {
            'quantity': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '1',
                'placeholder': 'Enter Quantity',
                'oninput': 'calculate_amount()'  # Call the function on input
            }),
            'cost_per_unit': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01',
                'placeholder': 'Enter Cost per Unit',
                'oninput': 'calculate_amount()'  # Call the function on input
            }),
            'total_amount': forms.NumberInput(attrs={
                'class': 'form-control',
                'readonly': 'readonly',
                'placeholder': 'Total Amount'
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.label = ''  # Hide labels


 
class JobCardForm(forms.ModelForm):
    class Meta:
        model = JobCard
        fields = [
            'technician', 'date', 'reported_defect', 
            'party', 'vehicle', 'driver' 
        ]
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
            'technician': forms.Select(attrs={'id': 'id_technician'}),
            'driver': forms.Select(attrs={'id': 'id_driver'}),
            'party': forms.Select(attrs={'id': 'id_party'}),
            'vehicle': forms.Select(attrs={'id': 'id_vehicle'}),
        }
    # def clean_labour_cost(self):
    #     labour_cost = self.cleaned_data.get('labour_cost')
    #     if labour_cost is not None and labour_cost < 0:
    #         raise ValidationError("Labour cost must be a non-negative value.")
    #     return labour_cost

    # def clean_total_cost(self):
    #     total_cost = self.cleaned_data.get('total_cost')
    #     if total_cost is not None and total_cost < 0:
    #         raise ValidationError("Total cost must be a non-negative value.")
    #     return total_cost


class JobCardItemForm(forms.ModelForm):
    class Meta:
        model = JobCardItem
        fields = ['quantity', 'cost','total_cost']
        widgets = {
            'quantity': forms.NumberInput(attrs={'min': 1}),
            'cost': forms.NumberInput(attrs={'step': 1,'min': 0}),
      
            'quantity': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '1',
                'placeholder': 'Enter Quantity',
                'oninput': 'calculate_amount()'  # Call the function on input
            }),
            'cost': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '1',
                'placeholder': 'Enter Cost per Unit',
                'oninput': 'calculate_amount()'  # Call the function on input
            }),
        }
    # def clean_quantity(self):
    #     quantity = self.cleaned_data.get('quantity')
    #     product_code = self.cleaned_data.get('product_code')
    #     product=Product.objects.get(product_code=product_code)
    #     print("Product Name ", product.product_name)
    #     print("Product Code ", product.product_code)
    #     if quantity <= 0:
    #         raise ValidationError("Quantity must be a positive value.")
    #     if product and quantity > product.available_stock:
    #         raise ValidationError(
    #             f"Stock not available for {product.product_name}. Only {product.available_stock} left."
    #         )
        
    #     return quantity


    def clean_cost(self):
        cost = self.cleaned_data.get('cost')
        if cost < 0:
            raise ValidationError("Cost must be a non-negative value.")
        return cost
    

 
class CloseJobCardForm(forms.ModelForm):
    class Meta:
        model = JobCard
        fields = [
            'completed_action', 'status', 'labour_cost', 
        ]