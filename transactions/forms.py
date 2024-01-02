from django import forms
from transactions.models import Transaction

class TransactionForm(forms.ModelForm):
    class Meta:
        model=Transaction
        fields = ['amount','transaction_type']

    # user ke transactions type dekhabo kintu change korthe dibo na tai exta code egulo 
    # jokhon kono object make hobe tokhon kicho ekta kaj korar jonno use kore
    def __init__(self,*args,**kwargs):
        
        self.account = kwargs.pop('account') # buji nai etar kaj ki???
        super().__init__(*args,**kwargs)
        self.fields['transaction_type'].disabled = True
        self.fields['transaction_type'].widget = forms.HiddenInput()

    def save(self,commit=True):
        # je user request kortheche tar kono object jodi database e thake == self.instance
        # self.instance.account == current je user request kortheche database e tar kono object thakle tar account e jabo
        self.instance.account = self.account # je user request korche tar account
        self.instance.balance_after_transaction = self.account.balance
        return super().save()
    

class DepositForm(TransactionForm):
    def clean_amount(self): # amount field ke filter korbo
        min_deposit_amount = 100
        amount = self.cleaned_data.get('amount') # user er fill up kora form theke amra amount field er value ke niye aslam, 50
        if amount < min_deposit_amount:
            raise forms.ValidationError(
                f'You need to deposit at least {min_deposit_amount} $'
            )

        return amount


class WithdrawForm(TransactionForm):

    def clean_amount(self):
        account = self.account # eta kon account eta koi theke ashtheche?? kemne ashteche??
        min_withdraw_amount = 500
        max_withdraw_amount = 20000
        balance = account.balance # 1000 # balance ta kemne pacche??
        amount = self.cleaned_data.get('amount')
        if amount < min_withdraw_amount:
            raise forms.ValidationError(
                f'You can withdraw at least {min_withdraw_amount} $'
            )

        if amount > max_withdraw_amount:
            raise forms.ValidationError(
                f'You can withdraw at most {max_withdraw_amount} $'
            )

        if amount > balance: # amount = 5000, tar balance ache 200
            raise forms.ValidationError(
                f'You have {balance} $ in your account. '
                'You can not withdraw more than your account balance'
            )

        return amount



class LoanRequestForm(TransactionForm):
    def clean_amount(self):  # kono form er kono field ke filter ba update korthe chaile clean_fieldName namok functions use kore korthe hoi
        amount = self.cleaned_data.get('amount')

        return amount