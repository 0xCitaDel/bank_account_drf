import os
import uuid
from app import settings

from django.db import models, transaction

def customer_image_file_path(instance, filename):
    """Generate file path for new image"""
    ext = filename.split('.')[-1]
    filename = f'{uuid.uuid4()}.{ext}'

    return os.path.join(f'upload/{instance.user.id}/', filename)


class Customer(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(null=True, blank=True, max_length=255)
    city = models.CharField(null=True, blank=True, max_length=255)
    house = models.CharField(null=True, blank=True, max_length=255)
    image = models.ImageField(null=True, blank=True, upload_to=customer_image_file_path)

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        primary_key=True
    )

    def __str__(self):
        return f'{self.first_name} {self.last_name}'


class Account(models.Model):
    balance = models.DecimalField(
        default=0,
        max_digits=12,
        decimal_places=2
    )

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT
    )

    def __str__(self):
        return f'{self.id} of {self.user.username}'


class Action(models.Model):

    amount = models.DecimalField(
        max_digits=12,
        decimal_places=2
    )
    date = models.DateTimeField(auto_now_add=True)

    account = models.ForeignKey(
        Account,
        on_delete=models.CASCADE,
        related_name='actions'
    )

    def __str__(self):
        return f'Account number {self.account.id} ' +\
            f'was changed on {str(self.amount)}'


class Transaction(models.Model):
    amount = models.DecimalField(
        max_digits=12,
        decimal_places=2
    )
    date = models.DateTimeField(auto_now_add=True)

    account = models.ForeignKey(
        Account,
        on_delete=models.CASCADE
    )

    merchant = models.CharField(max_length=255)

    def __str__(self):
        return f'Account number {self.account.id} ' +\
            f'sent {str(self.amount)} to {self.merchant}'
    
    @classmethod
    def make_transaction(cls, amount, account, merchant):
        if account.balance < amount:
            raise(ValueError('Not enough money'))

        with transaction.atomic():
            account.balance -= amount
            account.save()
            tran = cls.objects.create(
                amount=amount, account=account, merchant=merchant)

        return account, tran
    

class Transfer(models.Model):

    from_account = models.ForeignKey(
        Account,
        on_delete=models.CASCADE,
        related_name='from_account'
    )

    to_account = models.ForeignKey(
        Account,
        on_delete=models.CASCADE,
        related_name='to_account'
    )

    amount = models.DecimalField(
        max_digits=12,
        decimal_places=2
    )


class Interest(models.Model):
    date = models.DateTimeField(auto_now_add=True)

    account = models.ForeignKey(
        Account,
        on_delete=models.CASCADE
    )

    amount = models.DecimalField(
        decimal_places=2,
        max_digits=12,
    )