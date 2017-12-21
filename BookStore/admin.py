from django.contrib import admin
from .models import Books
from .models import Feedbacks
from .models import Feedbackrates
from .models import Orders

admin.site.register(Books)
admin.site.register(Feedbacks)
admin.site.register(Feedbackrates)
admin.site.register(Orders)
# Register your models here.
