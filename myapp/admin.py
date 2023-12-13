from django.contrib import admin
from .models import *
# Register your models here.

admin.site.register(main_category)
admin.site.register(sub_category)
admin.site.register(expertise)
admin.site.register(topic)
admin.site.register(price)
admin.site.register(session)
admin.site.register(admin_user)
admin.site.register(ChartData)
admin.site.register(appointment)
# admin.site.register(RandomNumberModel)
# admin.site.register(YourModel)
admin.site.register(refund)
admin.site.register(refund_req)
admin.site.register(order)
admin.site.register(mentee)





#--------------mentor--------------------------



admin.site.register(Mentor_user)
admin.site.register(Add_profile)
admin.site.register(Add_work)

