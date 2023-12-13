from django.db import models
from django.utils import timezone
# Create your models here.
from datetime import timedelta

class admin_user(models.Model):
    name=models.CharField(max_length=30)
    email=models.EmailField(unique=True,max_length=40)
    password=models.CharField(max_length=10)
    otp=models.IntegerField(default=1234)


    def __str__(self) -> str:
        return self.name

class main_category(models.Model):
    name=models.CharField(max_length=30)
    image=models.ImageField(upload_to='img',blank=True,null=True)
    def __str__(self) -> str:
        return self.name

class sub_category(models.Model):
    mcategory=models.ForeignKey(main_category,on_delete=models.CASCADE)
    image=models.ImageField(upload_to='img',blank=True,null=True)
    name=models.CharField(max_length=30)    
    def __str__(self) -> str:
        return self.name
   
class expertise(models.Model):
    name=models.CharField(max_length=30)  
    mcategory=models.ForeignKey(main_category,on_delete=models.SET_NULL, blank=True, null=True)
    scategory=models.ForeignKey(sub_category,on_delete=models.SET_NULL, blank=True, null=True)
      
    def __str__(self) -> str:
        return self.name

class topic(models.Model):
    name=models.CharField(max_length=50)

    def __str__(self):
        return self.name

class price(models.Model):
    name=models.IntegerField()

    def __int__(self):
        return self.name


class session(models.Model):
    time=models.IntegerField()


class ChartData(models.Model):
    label = models.CharField(max_length=100)
    value = models.IntegerField()   
import random
def generate_random_number():
    return random.randint(1000, 9999)
STATUS_CHOICES = (
    ('upcoming', 'Upcoming'),
    ('confirmed', 'Confirmed'),
    ('canceled', 'Canceled'),
)
payment = (
    ('panding', 'panding'),
    ('refunded', 'refunded'),
    
) 
class appointment(models.Model):
    
    id1 = models.IntegerField(unique=True,default=generate_random_number)
    menter_name = models.CharField(max_length=100)
    mentee_name = models.CharField(max_length=100)
    order_date = models.DateTimeField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='upcoming')
    payment = models.CharField(max_length=10, choices=payment, default='panding')
    
    # def save(self, *args, **kwargs):
    #     if not self.id1:
    #         self.id1 = random.randint(1000, 9999)  # Generate a random 4-digit integer if id1 is not set
    #     super(Order, self).save(*args, **kwargs)

    def __str__(self):
        return f"{self.mentee_name}'s Order ({self.menter_name})"     

class refund(models.Model):
    api=models.ForeignKey(appointment,on_delete=models.CASCADE)
    menter_name = models.CharField(max_length=100)
    mentee_name = models.CharField(max_length=100)
    order_date = models.DateTimeField(auto_now_add=True)
    resone=models.CharField(max_length=200)


class refund_req(models.Model):
    api=models.ForeignKey(appointment,on_delete=models.CASCADE)
    id1 = models.IntegerField()
    menter_name = models.CharField(max_length=100)
    mentee_name = models.CharField(max_length=100)
    appointment_date = models.DateTimeField(blank=True,null=True)
    order_date = models.DateTimeField(auto_now_add=True)
    resone=models.CharField(max_length=200)

class order(models.Model):
    pass    


#-----------------------------Mentor---------------------------------------------





class Mentor_user(models.Model):
    email = models.EmailField(max_length=50)
    password = models.CharField(max_length=50)




topic_price=((6000,6000),(5000,5000),(1000,1000),(500,500),(100,100))
topic_durations=((6000,6000),(5000,5000),(1000,1000),(500,500),(100,100))
class Add_profile(models.Model):
    main = models.ForeignKey(main_category,on_delete=models.CASCADE)
    sub = models.ForeignKey(sub_category,on_delete=models.CASCADE)
    exp = models.ForeignKey(expertise,on_delete=models.CASCADE,default=1)
    IMG = models.ImageField(upload_to="img")
    name = models.CharField(max_length=50)
    email = models.EmailField(max_length=50)
    headline = models.CharField(max_length=50)
    about_you = models.CharField(max_length=50)
    cou = models.CharField(max_length=50)
    sta = models.CharField(max_length=50)
    cit = models.CharField(max_length=50)
    lunguages = models.CharField(max_length=500)
    links1 = models.CharField(max_length=1000)
    links2 = models.CharField(max_length=1000)
    ex_education = models.CharField(max_length=1000)
    add_work = models.CharField(max_length=1000)
    add_education = models.CharField(max_length=1000)
    topics = models.CharField(max_length=1000)
    price = models.CharField(choices=topic_price,max_length=500)
    durations = models.CharField(choices=topic_durations,max_length=1000)
    topics_durations = models.CharField(max_length=1000)
    blocked=models.BooleanField(default=False)
    
    def __str__(self):
        return self.name
    



class Add_work(models.Model):
    company_name = models.CharField(max_length=30)
    titel = models.CharField(max_length=30)
    current_role = models.CharField(max_length=50)
    start_month = models.CharField(max_length=50)     
    start_year = models.CharField(max_length=50)
    end_month = models.CharField(max_length=50)     
    end_year = models.CharField(max_length=50)   
    







#=========================== Mentee ======================================
class mentee_user(models.Model):
    email=models.EmailField(max_length=50)
    password=models.CharField(max_length=50)



class mentee(models.Model):
    image=models.ImageField(upload_to="img")
    name=models.CharField(max_length=50)
    email=models.EmailField(max_length=50)
    title=models.CharField(max_length=50)
    headline=models.CharField(max_length=50)
    about_you=models.TextField()
    country=models.CharField(max_length=50,blank=True,null=True)
    state=models.CharField(max_length=50,blank=True,null=True)
    city=models.CharField(max_length=50,blank=True,null=True)
    cou=models.CharField(max_length=50)
    sta=models.CharField(max_length=50)
    cit=models.CharField(max_length=50)

    languages=models.CharField(max_length=50)
    ex_education=models.CharField(max_length=50,blank=True,null=True)
    add_work=models.CharField(max_length=1000)
    add_education=models.CharField(max_length=1000,blank=True,null=True)
    
    blocked = models.BooleanField(default=False)
    mcategory=models.ForeignKey(main_category,on_delete=models.SET_NULL, blank=True, null=True)
    scategory=models.ForeignKey(sub_category,on_delete=models.SET_NULL, blank=True, null=True)
    ecategory=models.ForeignKey(expertise,on_delete=models.SET_NULL, blank=True, null=True)
    # experti=models.ForeignKey(expertise,on_delete=models.SET_NULL, blank=True, null=True)
            
    def __str__(self):
        return self.name
    
