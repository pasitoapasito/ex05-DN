from django.db   import models

from core.models import TimeStampModel


class AccountBook(TimeStampModel):
    
    STATUS_TYPES = [
        ('in_use', 'AccountBook in use'),
        ('deleted', 'AccountBook deleted'),
    ]
    
    user   = models.ForeignKey('users.User', on_delete=models.CASCADE)
    name   = models.CharField(max_length=200)
    budget = models.DecimalField(max_digits=10, decimal_places=0)
    status = models.CharField(max_length=200, choices=STATUS_TYPES, default='in_use')
    
    def __str__(self):
        return self.name
    
    class Meta:
        db_table = 'account_books'
        
    
class AccountBookLog(TimeStampModel):
    
    ACCOUNT_TYPES = [
        ('expenditure', 'expenditure'),
        ('income', 'income'),
    ]
    
    STATUS_TYPES = [
        ('in_use', 'AccountBookLog in use'),
        ('deleted', 'AccountBookLog deleted'),
    ]
    
    category    = models.ForeignKey('AccountBookCategory', on_delete=models.DO_NOTHING, null=True, blank=True)
    book        = models.ForeignKey('AccountBook', related_name='logs', on_delete=models.CASCADE)
    title       = models.CharField(max_length=200)
    price       = models.DecimalField(max_digits=10, decimal_places=0)
    description = models.CharField(max_length=255, null=True, blank=True)
    types       = models.CharField(max_length=200, choices=ACCOUNT_TYPES, default='expenditure')
    status      = models.CharField(max_length=200, choices=STATUS_TYPES, default='in_use')
    
    def __str__(self):
        return self.title
    
    class Meta:
        db_table = 'account_book_logs'
        

class AccountBookCategory(TimeStampModel):
    
    STATUS_TYPES = [
        ('in_use', 'AccountBookCategory in use'),
        ('deleted', 'AccountBookCategory deleted'),
    ]
    
    user   = models.ForeignKey('users.User', on_delete=models.CASCADE)
    name   = models.CharField(max_length=200)
    status = models.CharField(max_length=200, choices=STATUS_TYPES, default='in_use')
    
    def __str__(self):
        return self.name
    
    class Meta:
        db_table = 'account_book_categories'