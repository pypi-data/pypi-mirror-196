from django.contrib import admin
from .models import Finance , FinanceAccounting , Exchangerate , Interestaccount , Loanaccount


# Register your models here.
admin.site.register(Finance)
admin.site.register(FinanceAccounting)
admin.site.register(Exchangerate)
admin.site.register(Interestaccount)
admin.site.register(Loanaccount)
