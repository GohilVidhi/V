from django.shortcuts import render,redirect,get_object_or_404
from .models import *
from django.core.paginator import Paginator
from django.http import JsonResponse
from .forms import *
from django.db.models import Q
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
import random
from django.core.mail import send_mail
from django.urls import reverse
from django.db.models import Count
import re
import math
# Create your views here.
def index(request):
    if 'email' in request.session:
        m_count=main_category.objects.count()
        s_count=sub_category.objects.count()
        e_count=expertise.objects.count()
        t_count=topic.objects.count()
        p_count=price.objects.count()
        s1_count=session.objects.count()
        labels = ['main_category','sub_category','expertise','topic','price','session']
        values = [m_count,s_count,e_count,t_count,p_count,s1_count]
        contaxt={
            "m_count":m_count,
            "s_count":s_count,
            "e_count":e_count,
            "t_count":t_count,
            "p_count":p_count,
            "s1_count":s1_count,
            "labels":labels,
            "values":values

        }
        
        return render(request,"index.html",contaxt)
    else:
        messages.success(request,"First Login")   
        return render(request,"login.html")
        

# def login_user(request):
#     if request.user.is_authenticated:
#         return redirect('index')
#     else:    
#         if request.POST:
#             username = request.POST.get('username')
#             password = request.POST.get('password')
#             user = authenticate(request, username= username, password = password)
#             if user is None:
#                 messages.info(request,'Sorry!You are invalid user.\n Please Register First')
#                 return render(request, 'login.html')
        
#             login(request,user)
#             return redirect('index')
        
#         return render(request, 'login.html')

# def logoutUser(request):
#     logout(request)
#     return redirect('login')

def form(request):
    return render(request,"form.html")

def table(request):
    return render(request,"table.html")
# ===================================== m_category =============================
from PIL import Image
def add_main_category(request):
    if request.POST:
        name=request.POST['name']
        
        try:
            mid=main_category.objects.get(name=name)
            if mid.name==name:
                print("ok")
                messages.success(request,"Main Category Already Exists ")   
                                 
                return render(request,'add_main_category.html')
        except:
            pattern = r"^[A-Z']+[A-Za-z']+$"  # Allow letters, single quotes, hyphens, and spaces
              
            if name==" ":
                # messages.success(request,"please data enterd")
                contaxt={
                    "msg":"Please fill out this field"
                }  
                return render(request,"add_main_category.html",contaxt)
            if any(char.isdigit() for char in name):
                # messages.error(request, "Topic name cannot consist of only digits") 
                contaxt={
                    "msg":"Digit are not allowed in the name"
                }  
                return render(request,"add_main_category.html",contaxt)
            if re.search(r'[!@#$%^&*()_+=\[\]{}|\\:;"\'<>,.?/~`]', name):
                    # messages.error(request, "s") 
                    contaxt={
                        "msg":"Special characters are not allowed in the name."
                }  
                    return render(request,"add_main_category.html",contaxt) 
            if not name[0].isupper():
                context = {"msg": "The first character of the name should be capitalized."}
                return render(request, "add_main_category.html", context)             
            if re.match(pattern, name):   
                    contaxt={
                        "msg":"Spaces are not allowed in the name"
                }  
                    return render(request,"add_main_category.html",contaxt)  
                      
            if len(name) < 5: 
                    # messages.error(request, "len") 
                    contaxt={
                        "msg":"Name must be at least 5 characters long"
                }  
                    return render(request,"add_main_category.html",contaxt) 
                       
            else:
                if "img" in request.FILES:
                    img=request.FILES['img']
                    try:
                        with Image.open(img) as i:
                            if i.format.lower() not in ['jpeg', 'jpg', 'png', 'gif']:
                                contaxt={
                                    "msg1":"Unsupported image format"
                                }  
                                return render(request,"add_main_category.html",contaxt)    
                            else:     
                            
                                main_category.objects.create(name=name,
                                                    image=img)
                                print("ok1")                    
                                messages.success(request,"Successful Add")                    
                                return redirect('show_main_category')
                    except:
                        contaxt={
                                    "msg1":"Video not suppoted"
                                }  
                        return render(request,"add_main_category.html",contaxt)    

                else:
                    contaxt={
                        "msg1":"No image provided"
                    }  
                    return render(request,"add_main_category.html",contaxt)      

    else:
        return render(request,"add_main_category.html")

def show_main_category(request):
    mid=main_category.objects.order_by("-id")
    mid1=main_category.objects.count()
    mid = [(item, index + 1) for index, item in enumerate(mid)]
    # main_categories = main_category.objects.annotate(product_count=Count('sub_category'))
    # for i in main_categories:
    #     print(i.name,i.product_count)
    show_page=10
    paginator = Paginator(mid, show_page)
    page_number = request.GET.get('page')
    print(page_number)
    mid= paginator.get_page(page_number)
    p=mid1/show_page
    p1=math.ceil(p)-2
    contaxt={
        "mid":mid,
        "mid1":mid1,
        "p1":p1,
        "show_page":show_page,
        "page_number":page_number,
    }
    return render(request,"show_main_category.html",contaxt)
def delete_main_category(request,id):
    mid=main_category.objects.get(id=id)
    mid.delete()
    messages.success(request,"Successful Delete")   
    return redirect('show_main_category')
def edit_main_category(request,id):
    mid=main_category.objects.get(id=id)
    # print("ok")
    if request.POST:
        name=request.POST['name']
        try:
            mid=main_category.objects.get(name=name)
            if mid.name==name:
                print("ok")
                if "img" in request.FILES:
                    img=request.FILES['img']
                    try:
                        with Image.open(img) as i:
                            if i.format.lower() not in ['jpeg', 'jpg', 'png', 'gif']:
                                contaxt={
                                    "msg1":"Unsupported image format",
                                    "mid":mid
                                }  
                                return render(request,"edit_main_category.html",contaxt)    
                            else:     
                                if "img" in request.FILES:
                                    img=request.FILES['img']
                                    mid.name=name
                                    mid.image=img
                                    mid.save()
                                    messages.success(request,"Successful Updated") 
                                    return redirect('show_main_category') 
                                else:
                                    mid.name=name    
                                    mid.save()
                                    messages.success(request,"Successful Updated")  
                                    return redirect('show_main_category')
                    except:
                        contaxt={
                                    "msg1":"Video not suppoted",
                                    "mid":mid
                                }  
                        return render(request,"edit_main_category.html",contaxt)
                else:    
                    messages.success(request,"Main Category Already Exists")
                    return redirect('show_main_category')     
            # else:
                
            #     if "img" in request.FILES:
            #         img=request.FILES['img']
            #         # mid.name=name
            #         mid.image=img
            #         mid.save()
            #         messages.success(request,"Successful Updated") 
            #         return redirect('show_main_category') 
            #     else:
            #         mid.name=name    
            #         mid.save()
            #         messages.success(request,"Successful Updated")  
            #         return redirect('show_main_category')    
        except:  

            pattern = r"^[A-Z']+[A-Za-z']+$"  # Allow letters, single quotes, hyphens, and spaces
              
            if name=="":
                # messages.success(request,"please data enterd")
                contaxt={
                    "msg":"Please fill out this field",
                    "mid":mid
                }  
                return render(request,"edit_main_category.html",contaxt)      
            if any(char.isdigit() for char in name):
                # messages.error(request, "Topic name cannot consist of only digits") 
                contaxt={
                    "msg":"Digit are not allowed in the name",
                      "mid":mid
                }  
                return render(request,"edit_main_category.html",contaxt)
            if re.search(r'[!@#$%^&*()_+=\[\]{}|\\:;"\'<>,.?/~`]', name):
                    # messages.error(request, "s") 
                    contaxt={
                        "msg":"Special characters are not allowed in the name.",
                        "mid":mid
                }  
                    return render(request,"edit_main_category.html",contaxt) 
            if not name[0].isupper():
                context = {
                    "msg": "The first character of the name should be capitalized.",
                    "mid":mid
                    }
                return render(request, "edit_main_category.html", context)             
            if  re.match(pattern, name):   
                    contaxt={
                        "msg":"Spaces are not allowed in the name",
                        "mid":mid
                }  
                    return render(request,"edit_main_category.html",contaxt)  
                      
            if len(name) < 5: 
                    # messages.error(request, "len") 
                    contaxt={
                        "msg":"Name must be at least 5 characters long",
                        "mid":mid
                }  
                    return render(request,"edit_main_category.html",contaxt)    
            # if "img" not in request.FILES:
            #     contaxt={
            #                         "msg1":"Vidio not suppoted"
            #                     }  
            #     return render(request,"edit_main_category.html",contaxt)
            if "img" in request.FILES:
                    img=request.FILES['img']
                    try:
                        with Image.open(img) as i:
                            if i.format.lower() not in ['jpeg', 'jpg', 'png', 'gif']:
                                contaxt={
                                    "msg1":"Unsupported image format"
                                }  
                                return render(request,"edit_main_category.html",contaxt)    
                            else:     
                                if "img" in request.FILES:
                                    img=request.FILES['img']
                                    mid.name=name
                                    mid.image=img
                                    mid.save()
                                    messages.success(request,"Successful Updated") 
                                    return redirect('show_main_category') 
                                else:
                                    mid.name=name    
                                    mid.save()
                                    messages.success(request,"Successful Updated")  
                                    return redirect('show_main_category')
                    except:
                        contaxt={
                                    "msg1":"Video not suppoted"
                                }  
                        return render(request,"edit_main_category.html",contaxt)    

            else:
                mid.name=name    
                mid.save()
                messages.success(request,"Successful Updated")  
                return redirect('show_main_category')               
            
    else:
        contaxt={
            "mid":mid
        }
        return render(request,'edit_main_category.html',contaxt)    
# ============================= search ===============================
# def main_searchview(request):
#     srch = request.GET["srch"]
#     if srch:
#         mid1 = main_category.objects.filter(name__contains=srch).count()
#         mid = main_category.objects.filter(name__contains=srch)
#         print(mid1)
        # paginator = Paginator(mid, 5)
        # page_number = request.GET.get('page')
        # mid= paginator.get_page(page_number)
    # contaxt={
    #     'mid':mid,
    #     'mid1':mid1,
    # }    
    # return render(request,"show_main_category.html",contaxt)

def main_searchview(request):
    query = request.GET.get('query', '')
    products = main_category.objects.filter(name__icontains=query).order_by("-id")
    results = [{'row_number': index + 1, 'id': product.id, 'name': product.name, 'image_url': product.image.url,
                'edit_url': reverse('edit_main_category', args=[product.id]),
                'delete_url': reverse('delete_main_category', args=[product.id])} for index, product in enumerate(products)]
    return JsonResponse(results, safe=False)


# def sub_searchview(request):
#     query = request.GET.get('query', '')
#     products = sub_category.objects.filter(name__icontains=query)
#     results = [{'row_number': index + 1, 'id': product.id,'mcategory':product.mcategory.name, 'name': product.name, 'image_url': product.image.url,
#                 'edit_url': reverse('edit_sub_category', args=[product.id]),
#                 'delete_url': reverse('delete_sub_category', args=[product.id])} for index, product in enumerate(products)]
#     return JsonResponse(results, safe=False)

# def expertise_searchview(request):
#     query = request.GET.get('query', '')
#     products = expertise.objects.filter(name__icontains=query)
#     results = [{'row_number': index + 1, 'id': product.id,'mcategory':product.mcategory.name,'scategory':product.scategory.name, 'name': product.name, 
#                 'edit_url': reverse('edit_expertise', args=[product.id]),
#                 'delete_url': reverse('delete_expertise', args=[product.id])} for index, product in enumerate(products)]
#     return JsonResponse(results, safe=False)

# def topic_searchview(request):
#     query = request.GET.get('query', '')
#     products = topic.objects.filter(name__icontains=query)
#     results = [{'row_number': index + 1, 'id': product.id, 'name': product.name,
#                 'edit_url': reverse('edit_topic', args=[product.id]),
#                 'delete_url': reverse('delete_topic', args=[product.id])} for index, product in enumerate(products)]
#     return JsonResponse(results, safe=False)

# def price_searchview(request):
#     query = request.GET.get('query', '')
#     products = price.objects.filter(name__icontains=query)
#     results = [{'row_number': index + 1, 'id': product.id, 'name': product.name,
#                 'edit_url': reverse('edit_price', args=[product.id]),
#                 'delete_url': reverse('delete_price', args=[product.id])} for index, product in enumerate(products)]
#     return JsonResponse(results, safe=False)

# def session_searchview(request):
#     query = request.GET.get('query', '')
#     products = session.objects.filter(time__icontains=query)
#     results = [{'row_number': index + 1, 'id': product.id, 'name': product.time,
#                 'edit_url': reverse('edit_session', args=[product.id]),
#                 'delete_url': reverse('delete_session', args=[product.id])} for index, product in enumerate(products)]
#     return JsonResponse(results, safe=False)
# =========================== s_category ===========================

def get_subcategories(request):
    main_category_id = request.GET.get('main_category_id')
    print(main_category_id)
    subcategories = sub_category.objects.filter(mcategory_id=main_category_id).values('id', 'name')
    print(subcategories)
    return JsonResponse(list(subcategories), safe=False)

def add_sub_category(request):
    mid=main_category.objects.all()
    if request.POST:
        m_cate=request.POST['m_cate']
        print(m_cate)
        m=main_category.objects.get(id=m_cate)
        print(m)
        name=request.POST['name']
        # img=request.FILES['img']

        try:
            print("ok1")
            sid=sub_category.objects.get(name=name)
            print("ok2")

            if sid.name==name:
                print("ok")
                messages.success(request,"Sub Category Already Exists ")   
                contaxt={
                    "mid":mid
                }
                return render(request,"add_sub_category.html",contaxt)
        except:   
            pattern = r"^[A-Z']+[A-Za-z']+$"  # Allow letters, single quotes, hyphens, and spaces
              
            if name=="":
                # messages.success(request,"please data enterd")
                contaxt={
                    "msg":"Please fill out this field",
                    "mid":mid
                }  
                return render(request,"add_sub_category.html",contaxt)
            if any(char.isdigit() for char in name):
                # messages.error(request, "Topic name cannot consist of only digits") 
                contaxt={
                    "msg":"Digit are not allowed in the name",
                    "mid":mid
                }  
                return render(request,"add_sub_category.html",contaxt)
            if re.search(r'[!@#$%^&*()_+=\[\]{}|\\:;"\'<>,.?/~`]', name):
                    # messages.error(request, "s") 
                    contaxt={
                        "msg":"Special characters are not allowed in the name.",
                        "mid":mid
                }  
                    return render(request,"add_sub_category.html",contaxt) 
            if not name[0].isupper():
                context = {"msg": "The first character of the name should be capitalized.","mid":mid}
                return render(request, "add_sub_category.html", context)             
            if not re.match(pattern, name):   
                    contaxt={
                        "msg":"Spaces are not allowed in the name",
                        "mid":mid
                }  
                    return render(request,"add_sub_category.html",contaxt)  
                      
            if len(name) < 5: 
                    # messages.error(request, "len") 
                    contaxt={
                        "msg":"Name must be at least 5 characters long",
                        "mid":mid
                }  
                    return render(request,"add_sub_category.html",contaxt) 
                       
            else:
                if "img" in request.FILES:
                    img=request.FILES['img']
                    try:
                        with Image.open(img) as i:
                            if i.format.lower() not in ['jpeg', 'jpg', 'png', 'gif']:
                                contaxt={
                                    "msg1":"Unsupported image format",
                                    "mid":mid
                                }  
                                return render(request,"add_sub_category.html",contaxt)    
                            else:     
                            
                                sub_category.objects.create(name=name, mcategory=m,image=img)
                                messages.success(request,"Successful Add")    
                                return redirect('show_sub_category')
                    except:
                        contaxt={
                                    "msg1":"Video not suppoted",
                                    "mid":mid
                                }  
                        return render(request,"add_sub_category.html",contaxt)    

                else:
                    contaxt={
                        "msg1":"No image provided",
                        "mid":mid


                    }  
                    return render(request,"add_sub_category.html",contaxt)      

              
    else:

        contaxt={
            "mid":mid
        }
        return render(request,"add_sub_category.html",contaxt)

def show_sub_category(request):
    sid=sub_category.objects.order_by("-id")
    sid1=sub_category.objects.count()
    sid = [(item, index + 1) for index, item in enumerate(sid)]
    show_page=10
    p=sid1/show_page
    p1=math.ceil(p)-2
    paginator = Paginator(sid, show_page)
    page_number = request.GET.get('page')
    sid= paginator.get_page(page_number)
    contaxt={
        "sid":sid,
        "sid1":sid1,
        "p1":p1,
        "show_page":show_page,
    }
    return render(request,"show_sub_category.html",contaxt)

def edit_sub_category(request,id):
    mid=main_category.objects.all()
    sid=sub_category.objects.get(id=id)
   
    if request.POST:
        m_cate=request.POST['m_cate']
        m=main_category.objects.get(id=m_cate)
        name=request.POST['name']
        # try:
        #     print("ok1")
        #     # sid1=sub_category.objects.get(name=name)
        #     print("ok2")
        if sid.name==name:
            print("ok")
            # if m:
            #     sid.mcategory=m
            #     sid.name=name
            #     sid.save() 
            #     messages.success(request,"Successful Updated")  
            #     return redirect('show_sub_category')    
            if "img1" in request.FILES and m :
                    img=request.FILES['img1']
                    try:
                        with Image.open(img) as i:
                            if i.format.lower() not in ['jpeg', 'jpg', 'png', 'gif']:
                                contaxt={
                                    "msg1":"Unsupported image format",
                                    "mid":mid,
                                    "sid":sid,
                                }  
                                return render(request,"add_sub_category.html",contaxt)    
                            else:     
                            
                                if "img1" in request.FILES:
                                    img=request.FILES['img1']
                                    sid.mcategory=m
                                    sid.name=name
                                    sid.image=img
                                    sid.save()
                                    messages.success(request,"Successful Updated")  
                                    return redirect('show_sub_category') 
                                else:
                                    sid.mcategory=m
                                    sid.name=name
                                    sid.save()    
                                    messages.success(request,"Successful Updated")  
                                    return redirect('show_sub_category') 
                    except:
                        contaxt={
                                    "msg1":"Video not suppoted",
                                    "mid":mid,
                                    "sid":sid,

                                }  
                        return render(request,"edit_sub_category.html",contaxt)
            else:    
                sid.mcategory=m
                sid.save()
                messages.success(request,"Sub Category Already Exists")
                return redirect('show_sub_category')  
        else:
            pattern = r"^[A-Z']+[A-Za-z']+$"  # Allow letters, single quotes, hyphens, and spaces
              
            if name=="":
                # messages.success(request,"please data enterd")
                contaxt={
                    "msg":"Please fill out this field",
                    "mid":mid,
                    "sid":sid,
                }  
                return render(request,"edit_sub_category.html",contaxt)
            if any(char.isdigit() for char in name):
                # messages.error(request, "Topic name cannot consist of only digits") 
                contaxt={
                    "msg":"Digit are not allowed in the name",
                    "mid":mid,
                    "sid":sid,
                }  
                return render(request,"edit_sub_category.html",contaxt)
            if re.search(r'[!@#$%^&*()_+=\[\]{}|\\:;"\'<>,.?/~`]', name):
                    # messages.error(request, "s") 
                    contaxt={
                        "msg":"Special characters are not allowed in the name.",
                        "mid":mid,
                        "sid":sid,
                }  
                    return render(request,"edit_sub_category.html",contaxt) 
            if not name[0].isupper():
                context = {"msg": "The first character of the name should be capitalized.","mid":mid,
                    "sid":sid,}
                return render(request, "edit_sub_category.html", context)             
            if not re.match(pattern, name):   
                    contaxt={
                        "msg":"Spaces are not allowed in the name",
                        "mid":mid,
                        "sid":sid,
                }  
                    return render(request,"edit_sub_category.html",contaxt)  
                      
            if len(name) < 5: 
                    # messages.error(request, "len") 
                    contaxt={
                        "msg":"Name must be at least 5 characters long",
                        "mid":mid,
                        "sid":sid,
                }  
                    return render(request,"edit_sub_category.html",contaxt)    
            if "img1" in request.FILES:
                    img=request.FILES['img1']
                    try:
                        with Image.open(img) as i:
                            if i.format.lower() not in ['jpeg', 'jpg', 'png', 'gif']:
                                contaxt={
                                    "msg1":"Unsupported image format",
                                    "mid":mid
                                }  
                                return render(request,"add_sub_category.html",contaxt)    
                            else:     
                            
                                if "img1" in request.FILES:
                                    img=request.FILES['img1']
                                    sid.mcategory=m
                                    sid.name=name
                                    sid.image=img
                                    sid.save()
                                    messages.success(request,"Successful Updated")  
                                    return redirect('show_sub_category') 
                                else:
                                    sid.mcategory=m
                                    sid.name=name
                                    sid.save()    
                                    messages.success(request,"Successful Updated")  
                                    return redirect('show_sub_category') 
                    except:
                        contaxt={
                                    "msg1":"Video not suppoted",
                                    "mid":mid
                                }  
                        return render(request,"edit_sub_category.html",contaxt)          
            # if "img1" in request.FILES:
            #     img=request.FILES['img1']
            #     sid.mcategory=m
            #     sid.name=name
            #     sid.image=img
            #     sid.save()
            #     messages.success(request,"Successful Updated")  
            #     return redirect('show_sub_category') 
            else:
                sid.mcategory=m
                sid.name=name
                sid.save()    
                messages.success(request,"Successful Updated")  
                return redirect('show_sub_category')    
        
    else:
        contaxt={
            "mid":mid,
            "sid":sid,
            
        }
        return render(request,'edit_sub_category.html',contaxt)      
def delete_sub_category(request,id):
    sid=sub_category.objects.get(id=id)
    sid.delete()
    messages.success(request,"Successful Delete")  
    return redirect('show_sub_category')    

def sub_searchview(request):
    query = request.GET.get('query', '')
    products = sub_category.objects.filter(name__icontains=query).order_by("-id")
    # products = sub_category.objects.filter(
    #     Q(name__icontains=query) | Q(mcategory__name__icontains=query)
    # ).order_by("-id")
    results = [{'row_number': index + 1, 'id': product.id,'mcategory':product.mcategory.name, 'name': product.name, 'image_url': product.image.url,
                'edit_url': reverse('edit_sub_category', args=[product.id]),
                'delete_url': reverse('delete_sub_category', args=[product.id])} for index, product in enumerate(products)]
    return JsonResponse(results, safe=False)

# def sub_searchview(request):
#     srch = request.GET["srch"]
#     if srch:
#         sid1 = sub_category.objects.filter(name__contains=srch).count()
#         sid = sub_category.objects.filter(name__contains=srch)
#         print(sid1)
#     contaxt={
#         'sid':sid,
#         'sid1':sid1,
#     }    
#     return render(request,"show_sub_category.html",contaxt)

# ==================== expertise =====================

def add_expertise(request):
    mid=main_category.objects.all()
    sid=sub_category.objects.all()  
    if request.POST:
    
        m_category=request.POST['main_category']
        name=request.POST['name']
        s_category=request.POST['sub_category']
        # m_id=main_category.objects.get(id=m_category)
        # s_id=sub_category.objects.get(id=s_category)
        # print(s_id,m_id,name)
        try:
            m_id=main_category.objects.get(id=m_category)
            s_id=sub_category.objects.get(id=s_category)
            eid=expertise.objects.get(name=name)
            # print(eid)
            if eid.name==name:
                print("ok")
                messages.success(request,"Expertise Already Exists ")   
                contaxt={
                    "mid":mid,
                    "sid":sid,
                }
                return render(request,"add_expertise.html",contaxt)
        except:    
            pattern = r"^[A-Z']+[A-Za-z']+$"  # Allow letters, single quotes, hyphens, and spaces
              
            if m_category=="":
                # messages.success(request,"please data enterd")
                contaxt={
                    "msg":"Please fill out this field",
                    "mid":mid,
                    "sid":sid,
                }  
                return render(request,"add_expertise.html",contaxt)  
            if s_category=="":
                # messages.success(request,"please data enterd")
                contaxt={
                    "msg1":"Please fill out this field",
                    "mid":mid,
                    "sid":sid,
                }  
                return render(request,"add_expertise.html",contaxt) 
            if name=="":
                # messages.success(request,"please data enterd")
                contaxt={
                    "msg2":"Please fill out this field",
                    "mid":mid,
                    "sid":sid,
                }  
                return render(request,"add_expertise.html",contaxt) 
            if any(char.isdigit() for char in name):
                # messages.error(request, "Topic name cannot consist of only digits") 
                contaxt={
                    "msg2":"Digit are not allowed in the name",
                    "mid":mid
                }  
                return render(request,"add_expertise.html",contaxt)
            if re.search(r'[!@#$%^&*()_+=\[\]{}|\\:;"\'<>,.?/~`]', name):
                    # messages.error(request, "s") 
                    contaxt={
                        "msg2":"Special characters are not allowed in the name.",
                        "mid":mid
                }  
                    return render(request,"add_expertise.html",contaxt) 
            if not name[0].isupper():
                context = {"msg2": "The first character of the name should be capitalized.","mid":mid}
                return render(request, "add_expertise.html", context)             
            if not re.match(pattern, name):   
                    contaxt={
                        "msg2":"Spaces are not allowed in the name",
                        "mid":mid
                }  
                    return render(request,"add_expertise.html",contaxt)  
                      
            if len(name) < 5: 
                    # messages.error(request, "len") 
                    contaxt={
                        "msg2":"Name must be at least 5 characters long",
                        "mid":mid
                }  
                    return render(request,"add_expertise.html",contaxt)                
            else:    
                expertise.objects.create(name=name, mcategory=m_id,scategory=s_id)
                messages.success(request,"Successful Add")   
                return redirect('show_expertise')
    else:        
        contaxt={
                    "mid":mid,
                    "sid":sid,
                }
        return render(request,"add_expertise.html",contaxt)
import math
def show_expertise(request):
    eid=expertise.objects.order_by("-id")
    eid1=expertise.objects.count()
    eid = [(item, index + 1) for index, item in enumerate(eid)]
    show_page=10
    paginator = Paginator(eid,show_page)
    page_number = request.GET.get('page')
    p=eid1/show_page
    p1=math.ceil(p)-2
    eid= paginator.get_page(page_number)
    contaxt={
        "eid":eid,
        "eid1":eid1,
        "p1":p1,
        "show_page":show_page,
    }
    return render(request, 'show_expertise.html',contaxt)

def edit_expertise(request,id):
    mid=main_category.objects.all()
    sid=sub_category.objects.all()
    eid=expertise.objects.get(id=id)
    print(eid.mcategory,eid.scategory)
    # form = PersonCreationForm()
    if request.POST:
        m_cate=request.POST['main_category']
        s_cate=request.POST['sub_category']
        name=request.POST['name']  
        try:
           
            eid=expertise.objects.get(name=name)
            # print(eid)
            if eid.name==name:
                print("ok")
                m=main_category.objects.get(id=m_cate)
                s=sub_category.objects.get(id=s_cate) 
                eid.mcategory=m
                eid.scategory=s
                eid.name=name
                eid.save()
                messages.success(request,"Expertise Already Exists ")   
                return redirect('show_expertise')
        except:
            pattern = r"^[A-Z']+[A-Za-z']+$"  # Allow letters, single quotes, hyphens, and spaces
              
            if m_cate=="":
                # messages.success(request,"please data enterd")
                contaxt={
                    "msg":"Please fill out this field",
                    "mid":mid,
                    "sid":sid,
                    "eid":eid,
                }  
                return render(request,"edit_expertise.html",contaxt)  
            if s_cate=="":
                # messages.success(request,"please data enterd")
                contaxt={
                    "msg1":"Please fill out this field",
                    "mid":mid,
                    "sid":sid,
                    "eid":eid,

                }  
                return render(request,"edit_expertise.html",contaxt) 
            if name=="":
                # messages.success(request,"please data enterd")
                contaxt={
                    "msg2":"Please fill out this field",
                    "mid":mid,
                    "sid":sid,
                    "eid":eid,
                }  
                return render(request,"edit_expertise.html",contaxt) 
            if any(char.isdigit() for char in name):
                # messages.error(request, "Topic name cannot consist of only digits") 
                contaxt={
                    "msg2":"Digit are not allowed in the name",
                    "mid":mid,
                    "sid":sid,
                    "eid":eid,

                }  
                return render(request,"edit_expertise.html",contaxt)
            if re.search(r'[!@#$%^&*()_+=\[\]{}|\\:;"\'<>,.?/~`]', name):
                    # messages.error(request, "s") 
                    contaxt={
                        "msg2":"Special characters are not allowed in the name.",
                        "mid":mid,
                        "sid":sid,
                        "eid":eid,

                }  
                    return render(request,"edit_expertise.html",contaxt) 
            if not name[0].isupper():
                context = {
                    "msg2": "The first character of the name should be capitalized.",
                    "mid":mid,
                    "sid":sid,
                    "eid":eid,
                    }
                return render(request, "edit_expertise.html", context)             
            if not re.match(pattern, name):   
                    contaxt={
                        "msg2":"Spaces are not allowed in the name",
                        "mid":mid,
                        "sid":sid,
                        "eid":eid,

                }  
                    return render(request,"edit_expertise.html",contaxt)  
                      
            if len(name) < 5: 
                    # messages.error(request, "len") 
                    contaxt={
                        "msg2":"Name must be at least 5 characters long",
                        "mid":mid,
                        "sid":sid,
                        "eid":eid,

                }  
                    return render(request,"edit_expertise.html",contaxt)                
            else:    
                m=main_category.objects.get(id=m_cate)
                s=sub_category.objects.get(id=s_cate) 
                eid.mcategory=m
                eid.scategory=s
                eid.name=name
                eid.save()
                messages.success(request,"Successful Updated")  
                return redirect('show_expertise')
    else:
        
        contaxt={
            "eid":eid,
            "mid":mid,
            "sid":sid,
            "form":form,
        
        }
        return render(request, 'edit_expertise.html',contaxt)

def delete_expertise(request,id):
    eid=expertise.objects.get(id=id)
    eid.delete()
    messages.success(request,"Successful Delete")  
    return redirect('show_expertise')

def expertise_searchview(request):
    query = request.GET.get('query', '')
    products = expertise.objects.filter(name__icontains=query).order_by("-id")
    results = [{'row_number': index + 1, 'id': product.id,'mcategory':product.mcategory.name,'scategory':product.scategory.name, 'name': product.name, 
                'edit_url': reverse('edit_expertise', args=[product.id]),
                'delete_url': reverse('delete_expertise', args=[product.id])} for index, product in enumerate(products)]
    return JsonResponse(results, safe=False)

# def expertise_searchview(request):
#     srch = request.GET["srch"]
#     if srch:
#         eid1 = expertise.objects.filter(name__contains=srch).count()
#         eid = expertise.objects.filter(name__contains=srch)
#         # eid=expertise.objects.filter(
#         #     Q(mcategory__name__icontains=srch) or Q(name__icontains=srch)
#         # )
#         print(eid1)
#     contaxt={
#         'eid':eid,
#         'eid1':eid1,
#     }    
#     return render(request,"show_expertise.html",contaxt)   

# ==================== topic =====================


def add_topic(request):
    if request.POST:
        name=request.POST['name']
        
        try:
            tid=topic.objects.get(name=name)
            if tid.name==name:
                print("ok")
                messages.success(request,"Topic Already Exists ")   
                return render(request,"add_topic.html")
        except: 

            pattern = r"^[A-Z']+[A-Za-z']+$"  # Allow letters, single quotes, hyphens, and spaces
            
            if name=="":
                # messages.success(request,"please data enterd")
                contaxt={
                    "msg":"Please fill out this field"
                }  
                return render(request,"add_topic.html",contaxt)
            if any(char.isdigit() for char in name):
                # messages.error(request, "Topic name cannot consist of only digits") 
                contaxt={
                    "msg":"Digit are not allowed in the name"
                }  
                return render(request,"add_topic.html",contaxt)
            if re.search(r'[!@#$%^&*()_+=\[\]{}|\\:;"\'<>,.?/~`]', name):
                    # messages.error(request, "s") 
                    contaxt={
                        "msg":"Special characters are not allowed in the name."
                }  
                    return render(request,"add_topic.html",contaxt) 
            if not name[0].isupper():
                context = {"msg": "The first character of the name should be capitalized."}
                return render(request, "add_topic.html", context)             
            if not re.match(pattern, name):   
                    contaxt={
                        "msg":"Spaces are not allowed in the name"
                }  
                    return render(request,"add_topic.html",contaxt)  
                      
            if len(name) < 5: 
                    # messages.error(request, "len") 
                    contaxt={
                        "msg":"Name must be at least 5 characters long"
                }  
                    return render(request,"add_topic.html",contaxt)
                   
           
                   
            else:

                topic.objects.create(name=name) 
                messages.success(request,"Successful Add")  
                return redirect('show_topic')
         
    else:
        return render(request,"add_topic.html")    

def show_topic(request):
    tid=topic.objects.order_by("-id")
    tid = [(item, index + 1) for index, item in enumerate(tid)]
    tid1=topic.objects.count()
    show_page=10
    p=tid1/show_page
    p1=math.ceil(p)-2
    paginator = Paginator(tid, show_page)
    page_number = request.GET.get('page')
    tid= paginator.get_page(page_number)
    contaxt={
        "tid":tid,
        "tid1":tid1,
        "p1":p1,
        "show_page":show_page, 
    }
    return render(request,"show_topic.html",contaxt)

def edit_topic(request,id):
    tid=topic.objects.get(id=id)
    if request.POST:
        name=request.POST['name']
        pattern = r"^[A-Z']+[A-Za-z']+$"  # Allow letters, single quotes, hyphens, and spaces
            
        if name=="":
            # messages.success(request,"please data enterd")
            contaxt={
                "msg":"Please fill out this field",
                "tid":tid

            }  
            return render(request,"edit_topic.html",contaxt)
        if any(char.isdigit() for char in name):
            # messages.error(request, "Topic name cannot consist of only digits") 
            contaxt={
                "msg":"Digit are not allowed in the name",
                "tid":tid

            }  
            return render(request,"edit_topic.html",contaxt)
        if re.search(r'[!@#$%^&*()_+=\[\]{}|\\:;"\'<>,.?/~`]', name):
                # messages.error(request, "s") 
                contaxt={
                    "msg":"Special characters are not allowed in the name.",
                    "tid":tid

            }  
                return render(request,"edit_topic.html",contaxt) 
        if not name[0].isupper():
            context = {
                "msg": "The first character of the name should be capitalized.",
                "tid":tid
                }
            return render(request, "edit_topic.html", context)             
        if not re.match(pattern, name):   
                contaxt={
                    "msg":"Spaces are not allowed in the name",
                    "tid":tid
                        
            }  
                return render(request,"edit_topic.html",contaxt)  
                    
        if len(name) < 5: 
                # messages.error(request, "len") 
                contaxt={
                    "msg":"Name must be at least 5 characters long",
                    "tid":tid

            }  
                return render(request,"edit_topic.html",contaxt)
        else:
            tid.name=name
            tid.save()
            messages.success(request,"Successful Update")  
            return redirect('show_topic')
    else:
        contaxt={
            "tid":tid
        }
        return render(request,"edit_topic.html",contaxt)    
   

def delete_topic(request,id):
    tid=topic.objects.get(id=id)
    tid.delete()
    messages.success(request,"Successful Delete")  
    return redirect('show_topic')

def topic_searchview(request):
    query = request.GET.get('query', '')
    products = topic.objects.filter(name__icontains=query).order_by("-id")
    results = [{'row_number': index + 1, 'id': product.id, 'name': product.name,
                'edit_url': reverse('edit_topic', args=[product.id]),
                'delete_url': reverse('delete_topic', args=[product.id])} for index, product in enumerate(products)]
    return JsonResponse(results, safe=False)
# ============================= search ===============================
# def topic_searchview(request):
#     srch = request.GET["srch"]
#     if srch:
#         tid1 = topic.objects.filter(name__contains=srch).count()
#         tid = topic.objects.filter(name__contains=srch)
#         print(tid1)
#         paginator = Paginator(tid, 5)
#         page_number = request.GET.get('page')
#         tid= paginator.get_page(page_number)
#     contaxt={
#         'tid':tid,
#         'tid1':tid1,
#     }    
#     return render(request,"show_topic.html",contaxt)


# ==================== price =====================

def add_price(request):
    if request.POST:
        name=request.POST['name']
        print(type(name))
        try:
            pid=price.objects.get(name=name)
            print(type(pid.name))
            if pid.name==int(name):
                print("ok")
                messages.success(request,"Price Already Exists ")   
                return render(request,"add_price.html")
        except:   
            pattern = r"^[0-9]+$"  # Allow letters, single quotes, hyphens, and spaces
            
            if name=="":
                # messages.success(request,"please data enterd")
                contaxt={
                    "msg":"Please fill out this field"
                    

                }  
                return render(request,"add_price.html",contaxt)  
            if any(char.isalpha() for char  in name):
            # messages.error(request, "Topic name cannot consist of only digits") 
                contaxt={
                    "msg":"Character are not allowed in the name"

                }  
                return render(request,"add_price.html",contaxt) 
            if re.search(r'[!@#$%^&*()_+=\[\]{}|\\:;"\'<>,.?/~`]', name):
                # messages.error(request, "s") 
                contaxt={
                    "msg":"Special characters are not allowed in the name."
                

            }  
                return render(request,"add_price.html",contaxt)    
            if not re.match(pattern, name):   
                contaxt={
                    "msg":"Spaces are not allowed in the name"
                        
            }  
                return render(request,"add_price.html",contaxt)         
            else:      
                price.objects.create(name=name) 
                messages.success(request,"Successful Add")  
                return redirect('show_price')
        # return render(request,"add_price.html") 

    else:
        return render(request,"add_price.html") 

def show_price(request):
    pid=price.objects.order_by("-id")
    pid = [(item, index + 1) for index, item in enumerate(pid)]
    pid1=price.objects.count()
    show_page=5
    p=pid1/show_page
    p1=math.ceil(p)-2
    paginator = Paginator(pid, show_page)
    page_number = request.GET.get('page')
    pid= paginator.get_page(page_number)

    contaxt={
        "pid":pid,
        "pid1":pid1,
        "p1":p1,
        "show_page":show_page, 
    }
    return render(request,"show_price.html",contaxt)


def edit_price(request,id):
    pid=price.objects.get(id=id)
    if request.POST:
        name=request.POST['name']
        try:
            pid=price.objects.get(name=name)
            print(type(pid.name))
            if pid.name==int(name):
                print("ok")
                messages.success(request,"Price Already Exists ")   
                return redirect('show_price')
        except:   
            pattern = r"^[0-9]+$"  # Allow letters, single quotes, hyphens, and spaces
            
            if name=="":
                # messages.success(request,"please data enterd")
                contaxt={
                    "msg":"Please fill out this field",
                    "pid":pid
                }  
                return render(request,"edit_price.html",contaxt)  
            if any(char.isalpha() for char  in name):
            # messages.error(request, "Topic name cannot consist of only digits") 
                contaxt={
                    "msg":"Character are not allowed in the name",
                    "pid":pid

                }  
                return render(request,"edit_price.html",contaxt) 
            if re.search(r'[!@#$%^&*()_+=\[\]{}|\\:;"\'<>,.?/~`]', name):
                # messages.error(request, "s") 
                contaxt={
                    "msg":"Special characters are not allowed in the name.",
                    "pid":pid
                

            }  
                return render(request,"edit_price.html",contaxt)    
            if not re.match(pattern, name):   
                contaxt={
                    "msg":"Spaces are not allowed in the name",
                    "pid":pid
                        
            }  
                return render(request,"edit_price.html",contaxt)  
            print(str(name[0]))    
            if str(name[0])==" ":   
                contaxt={
                    "msg":"123Spaces are not allowed in the name",
                    "pid":pid
                        
            }  
                return render(request,"edit_price.html",contaxt)            
            else:     
                print(type(name))
                print(type(pid.name))
                pid.name=name
                pid.save()
                messages.success(request,"Successful Update")  
                return redirect('show_price')
    else:
        contaxt={
            "pid":pid
        }
        return render(request,"edit_price.html",contaxt) 

def delete_price(request,id):
    pid=price.objects.get(id=id)
    pid.delete()
    messages.success(request,"Successful Delete")  
    return redirect('show_price')

def price_searchview(request):
    query = request.GET.get('query', '')
    products = price.objects.filter(name__icontains=query).order_by("-id")
    results = [{'row_number': index + 1, 'id': product.id, 'name': product.name,
                'edit_url': reverse('edit_price', args=[product.id]),
                'delete_url': reverse('delete_price', args=[product.id])} for index, product in enumerate(products)]
    return JsonResponse(results, safe=False)
# ============================= search ===============================
# def price_searchview(request):
#     srch = request.GET["srch"]
#     if srch:
#         pid1 = price.objects.filter(name__contains=srch).count()
#         pid = price.objects.filter(name__contains=srch)
#         print(pid1)
#         paginator = Paginator(pid, 5)
#         page_number = request.GET.get('page')
#         pid= paginator.get_page(page_number)
#     contaxt={
#         'pid':pid,
#         'pid1':pid1,
#     }  
      
#     return render(request,"show_price.html",contaxt)

# ============================= search ===============================
# def session_searchview(request):
#     srch = request.GET["srch"]
#     if srch:
#         sid1 = session.objects.filter(time__contains=srch).count()
#         sid = session.objects.filter(time__contains=srch)
#         print(sid1)
#         # paginator = Paginator(sid, 5)
#         # page_number = request.GET.get('page')
#         # sid= paginator.get_page(page_number)
#     contaxt={
#         'sid':sid,
#         'sid1':sid1,
#     }  
      
#     return render(request,"show_session.html",contaxt)


# ==================== price =====================

def add_session(request):
    if request.POST:
        time=request.POST['time']
        try:
            sid=session.objects.get(time=time)
            print(type(sid.time))
            if sid.time==int(time):
                print("ok")
                messages.success(request,"Session Already Exists ")   
                return render(request,"add_session.html")
        except:     
            pattern = r"^[0-9]+$"  # Allow letters, single quotes, hyphens, and spaces
            
            if time=="":
                # messages.success(request,"please data enterd")
                contaxt={
                    "msg":"Please fill out this field"
                    

                }  
                return render(request,"add_session.html",contaxt)  
            if any(char.isalpha() for char  in time):
            # messages.error(request, "Topic name cannot consist of only digits") 
                contaxt={
                    "msg":"Character are not allowed in the name"

                }  
                return render(request,"add_session.html",contaxt) 
            if re.search(r'[!@#$%^&*()_+=\[\]{}|\\:;"\'<>,.?/~`]', time):
                # messages.error(request, "s") 
                contaxt={
                    "msg":"Special characters are not allowed in the name."
                

            }  
                return render(request,"add_session.html",contaxt)    
            if not re.match(pattern, time):   
                contaxt={
                    "msg":"Spaces are not allowed in the name"
                        
            }  
                return render(request,"add_session.html",contaxt)
            else:       
                session.objects.create(time=time) 
                messages.success(request,"Successful Add")  
                return redirect('show_session')
        # return render(request,"add_session.html") 

    else:
        return render(request,"add_session.html") 

def show_session(request):
    sid=session.objects.order_by("-id")
    s=sid.count()
    sid1=session.objects.count()
    sid = [(item, index + 1) for index, item in enumerate(sid)]
    show_page=2
    p=sid1/show_page
    p1=math.ceil(p)-2
    paginator = Paginator(sid, show_page)
    page_number = request.GET.get('page')
    sid= paginator.get_page(page_number)

    
 
    contaxt={
        "sid":sid,
        "sid1":sid1,
        "p1":p1,
        "show_page":show_page,

    }
    return render(request,"show_session.html",contaxt)

def edit_session(request,id):
    sid=session.objects.get(id=id)
    if request.POST:
        time=request.POST['time']
        try:
            sid=session.objects.get(time=time)
            print(type(sid.time))
            if sid.time==int(time):
                print("ok")
                messages.success(request,"Session Already Exists ")   
                return redirect('show_session')
                
        except:  
            pattern = r"^[0-9]+$"  # Allow letters, single quotes, hyphens, and spaces

            if time=="":
                    # messages.success(request,"please data enterd")
                    contaxt={
                        "msg":"Please fill out this field",
                        "sid":sid
                        

                    }  
                    return render(request,"edit_session.html",contaxt)  
            if any(char.isalpha() for char  in time):
            # messages.error(request, "Topic name cannot consist of only digits") 
                contaxt={
                    "msg":"Character are not allowed in the name",
                    "sid":sid

                }  
                return render(request,"edit_session.html",contaxt) 
            if re.search(r'[!@#$%^&*()_+=\[\]{}|\\:;"\'<>,.?/~`]', time):
                # messages.error(request, "s") 
                contaxt={
                    "msg":"Special characters are not allowed in the name.",
                    "sid":sid
                

            }  
                return render(request,"edit_session.html",contaxt)    
            if not re.match(pattern, time):   
                contaxt={
                    "msg":"Spaces are not allowed in the name",
                    "sid":sid
                        
            }  
                return render(request,"edit_session.html",contaxt)        
            else:        
                sid.time=time
                sid.save()
                messages.success(request,"Successful Update")  
                return redirect('show_session')
    else:
        contaxt={
            "sid":sid
        }
        return render(request,"edit_session.html",contaxt) 


def delete_session(request,id):
    sid=session.objects.get(id=id)
    sid.delete()
    messages.success(request,"Successful Delete")  
    return redirect('show_session')

def session_searchview(request):
    query = request.GET.get('query', '')
    products = session.objects.filter(time__icontains=query).order_by("-id")
    results = [{'row_number': index + 1, 'id': product.id, 'name': product.time,
                'edit_url': reverse('edit_session', args=[product.id]),
                'delete_url': reverse('delete_session', args=[product.id])} for index, product in enumerate(products)]
    return JsonResponse(results, safe=False)
# ========================= models chart ==================================    

def chart_view(request):
    data = ChartData.objects.all()  # Query your data
    m_count=main_category.objects.count()
    s_count=sub_category.objects.count()
    e_count=expertise.objects.count()
    t_count=topic.objects.count()
    p_count=price.objects.count()
    s1_count=session.objects.count()
    # Extract the data for labels and values
    labels = ['main_category','sub_category','expertise','topic','price','session']
    values = [m_count,s_count,e_count,t_count,p_count,s1_count]

    return render(request, 'chart.html', {'labels': labels, 'values': values})






# ======================================================================


# def person_create_view(request):
#     form = PersonCreationForm()
#     if request.method == 'POST':
#         form = PersonCreationForm(request.POST)
#         if form.is_valid():
#             form.save()
#             return redirect('person_add')
#     return render(request, 'home.html', {'form': form})


# def person_update_view(request, pk):
#     person = get_object_or_404(expertise, pk=pk)
#     form = PersonCreationForm(instance=person)
#     if request.method == 'POST':
#         form = PersonCreationForm(request.POST, instance=person)
#         if form.is_valid():
#             form.save()
#             return redirect('person_change', pk=pk)
#     return render(request, 'home.html', {'form': form})


# AJAX
# def load_cities(request):
#     country_id = request.GET.get('country_id')
#     cities = sub_category.objects.filter(mcategory_id=country_id).all()
#     print(cities)
#     return render(request, 'city_dropdown_list_options.html', {'cities': cities})
    # return JsonResponse(list(cities.values('id', 'name')), safe=False)

# ============================ login ================================

def login(request):
    if 'email' in request.session:
        
        aid=admin_user.objects.get(email=request.session['email'])
        request.session['email']=aid.email



        contaxt={
            'aid':aid
        }

        return render(request,'index.html',contaxt)    
    else:
        try:
            if request.POST:
                email=request.POST['email']
                password=request.POST['password']
                print(email,password)
                aid=admin_user.objects.get(email=email)
                print("ok")
                if aid.email==email :
                    if aid.password==password:
                        request.session['email']=aid.email
                        # id=request.session.get('email')
                        print("ok")
                        # print(id.id)                         
                        return  redirect("index")
                    else:
                        messages.success(request,"Invalid Password")
                        return render(request,"login.html")
                else:
                    messages.success(request,"Invalid Email")
                    return render(request,"login.html")
            else:
                return render(request,'login.html')
        except:
            messages.success(request,"Invalid Email")
            return render(request,'login.html')
           


def logout(request):
    if 'email' in request.session:
        del request.session['email']
        return  redirect("login")
    else:
        return  redirect("login")
def forgot(request,id):        
    if request.POST:
        email=request.POST['email']
        otp=random.randint(1111,9999)

        try:
            uid=admin_user.objects.get(email=email)
            uid.otp=otp
            uid.save()
            # html_message = render_to_string('myapp/colorful_email.html',{'uid':uid})
            send_mail("Forget Password",'Your Otp is'+str(otp),'gohiljayb10@gmail.com',[email])
            contaxt={
                "email":email
            }
            return render(request,"confirm_password.html",contaxt)
        except:
            messages.success(request,"invalid email")    
            
              
            return render(request,"forgot.html")

    contaxt={
                "email":admin_user.objects.get(id=1)
            }
    print(contaxt)  
    return render(request,"forgot.html",contaxt)
    # return render(request,"forgot.html")

def confirm_password(request):
    if request.POST:
        email=request.POST['email']
        otp=request.POST['otp']
        new_password=request.POST['new_password']
        confirm_password=request.POST['confirm_password']

        uid=admin_user.objects.get(email=email)
        if str(uid.otp)==otp:
            if new_password==confirm_password:
                uid.password=new_password
                uid.save()
                contaxt={
                    'email':email,
                    'uid':uid,
                    'smsg':'password Successfully Changed'
                }
                return render(request,"login.html",contaxt)
            else:
                messages.success(request,"Not A Same Password")
                contaxt={
                    "email":email,
                    # 'emsg':"Not A Same Password",
                }
                return render(request,"confirm_password.html",contaxt)
        else:
            messages.success(request,"invalid otp")

            contaxt={
                    "email":email,
                    # 'e_msg':"invalid otp"
                }
            return render(request,"confirm_password.html",contaxt)

    return render(request,"confirm_password.html")

# =========================================== admin ======================

def admin_page(request):
    u_count=appointment.objects.filter(status="upcoming").count()
    c_count=appointment.objects.filter(status="confirmed").count()
    c1_count=appointment.objects.filter(status="canceled").count()
    r_count=refund_req.objects.count()
    contaxt={
        "u_count":u_count,
        "c_count":c_count,
        "c1_count":c1_count,
        "r_count":r_count,

    }
    return render(request,"admin.html",contaxt)

def upcoming_appointment(request):
    u=appointment.objects.filter(status="upcoming").order_by('-order_date')
    uid = [(item, index + 1) for index, item in enumerate(u)]
    uid1=appointment.objects.filter(status="upcoming").count()
    # print(uid1)
    show_page=2
    p=uid1/show_page
    p1=math.ceil(p)-2
    paginator = Paginator(uid, show_page)
    page_number = request.GET.get('page')
    uid= paginator.get_page(page_number)
    

    contaxt={
        "uid":uid,
        "u":u,
        "uid1":uid1,
        "p1":p1,
        "show_page":show_page,

    }
    return render(request,"upcoming_appointment.html",contaxt)

def upcoming_filter(request):
    uid = appointment.objects.filter(status="upcoming")
    uid = [(item, index + 1) for index, item in enumerate(uid)]

    if request.method == 'POST':
        from_date = request.POST.get('from_date')
        to_date = request.POST.get('to_date')
        products =  appointment.objects.filter(order_date__range=(from_date, to_date), status="upcoming")
        results = [{'row_number': index + 1,'id': product.id, 'id1': product.id1, 'menter_name': product.menter_name,
                'mentee_name': product.mentee_name, 'order_date':product.order_date,
                'delete_url': reverse('delete_session', args=[product.id])} for index, product in enumerate(products)]
        return JsonResponse(results, safe=False)
    return JsonResponse({'uid': uid}, safe=False)




def view_data(request, id):
    # Retrieve data based on ID
    uid=appointment.objects.get(id=id)
    contaxt={"uid":uid}
    return render(request, 'view_data.html', contaxt)

def upcoming_searchview(request):
    query = request.GET.get('query', '')
    uid = appointment.objects.filter(status="upcoming")
    uid = [(item, index + 1) for index, item in enumerate(uid)]
    products = appointment.objects.filter(menter_name__icontains=query,status="upcoming")
    # products = appointment.objects.filter(
    #     Q(menter_name__icontains=query) | Q(mentee_name__icontains=query),status="upcoming"
    # ).order_by("-id")
    uid1=appointment.objects.filter(status="upcoming").count()
    show_page=2
    p=uid1/show_page
    p1=math.ceil(p)-2
    paginator = Paginator(products, show_page)
    page_number = request.GET.get('page')
    products= paginator.get_page(page_number)
    results = [{'row_number': index + 1,'id': product.id, 'id1': product.id1, 'menter_name': product.menter_name,
                'mentee_name': product.mentee_name, 'order_date':product.order_date,
                'delete_url': reverse('delete_session', args=[product.id]),"uid1":uid1,"p1":p1,"show_page":show_page,} for index, product in enumerate(products)]
      
    return JsonResponse(results ,safe=False)
    # return render(request, 'upcoming_appintment.html', {'results': results})



def confirm_appointment(request):
    cid=appointment.objects.filter(status="confirmed")
    cid = [(item, index + 1) for index, item in enumerate(cid)]
    cid1=appointment.objects.filter(status="confirmed").count()
    print(cid1)
    adjusted_datetime = timezone.now() + timezone.timedelta(hours=5.5)
    show_page=10
    p=cid1/show_page
    p1=math.ceil(p)-2
    paginator = Paginator(cid, show_page)
    page_number = request.GET.get('page')
    cid= paginator.get_page(page_number)


    contaxt={
        "cid":cid,
        "cid1":cid1,
        "p1":p1,
        "show_page":show_page,
        'adjusted_datetime': adjusted_datetime,

    }
    return render(request,"confirm_appointment.html",contaxt)
def confirm_filter(request):
    cid = appointment.objects.filter(status="confirmed")
    cid = [(item, index + 1) for index, item in enumerate(cid)]

    if request.method == 'POST':
        from_date = request.POST.get('from_date')
        to_date = request.POST.get('to_date')
        products =  appointment.objects.filter(order_date__range=(from_date, to_date), status="confirmed")
        results = [{'row_number': index + 1,'id': product.id, 'id1': product.id1, 'menter_name': product.menter_name,
                'mentee_name': product.mentee_name, 'order_date':product.order_date,
                'delete_url': reverse('delete_session', args=[product.id])} for index, product in enumerate(products)]
        return JsonResponse(results, safe=False)
    return JsonResponse({'cid': cid}, safe=False)


def confirm_searchview(request):
    query = request.GET.get('query', '')
    products = appointment.objects.filter(menter_name__icontains=query,status="confirmed")
    # products = appointment.objects.filter(
    #     Q(menter_name__icontains=query) | Q(mentee_name__icontains=query),status="confirmed"
    # ).order_by("-id")
    results = [{'row_number': index + 1,'id': product.id, 'id1': product.id1, 'menter_name': product.menter_name,
                'mentee_name': product.mentee_name, 'order_date':product.order_date,
                'delete_url': reverse('delete_session', args=[product.id])} for index, product in enumerate(products)]
    return JsonResponse(results, safe=False)

def cancel_appointment(request):
    cid=appointment.objects.filter(status="canceled")
    cid = [(item, index + 1) for index, item in enumerate(cid)]
   
    cid1=appointment.objects.filter(status="canceled").count()

    print(cid1)
    show_page=10
    p=cid1/show_page
    p1=math.ceil(p)-2
    paginator = Paginator(cid, show_page)
    page_number = request.GET.get('page')
    cid= paginator.get_page(page_number)

    contaxt={
        "cid":cid,
        "cid1":cid1,
        "pay":payment,
        "p1":p1,
        "show_page":show_page,

    }
    return render(request,"cancel_appointment.html",contaxt)

def cancel_filter(request):
    cid = appointment.objects.filter(status="canceled")
    cid = [(item, index + 1) for index, item in enumerate(cid)]

    if request.method == 'POST':
        from_date = request.POST.get('from_date')
        to_date = request.POST.get('to_date')
        products =  appointment.objects.filter(order_date__range=(from_date, to_date), status="canceled")
        results = [{'row_number': index + 1,'id': product.id, 'id1': product.id1, 'menter_name': product.menter_name,
                'mentee_name': product.mentee_name, 'order_date':product.order_date,'payment':product.payment,
                'delete_url': reverse('delete_session', args=[product.id])} for index, product in enumerate(products)]
        return JsonResponse(results, safe=False)
    return JsonResponse({'cid': cid}, safe=False)


def cancel_searchview(request):
    query = request.GET.get('query', '')
    products = appointment.objects.filter(menter_name__icontains=query,status="canceled")
    # products = appointment.objects.filter(
    #     Q(menter_name__icontains=query) | Q(mentee_name__icontains=query),status="canceled"
    # ).order_by("-id")

    # products = appointment.objects.filter(menter_name__icontains=query,status="canceled").order_by("-id")
    results = [{'row_number': index + 1,'id': product.id, 'id1': product.id1, 'menter_name': product.menter_name,
                'mentee_name': product.mentee_name, 'order_date':product.order_date,"payment":product.payment,
                'delete_url': reverse('delete_session', args=[product.id])} for index, product in enumerate(products)]
    return JsonResponse(results, safe=False)


def create_refund(request,id):
    aid=appointment.objects.get(id=id)
    print(aid)
    name=request.POST['rid']
    print(name)
    eid=refund_req.objects.filter(api=aid).exists()
    print(eid)
    if name=="refunded":
        refund_req.objects.create(api=aid,id1=aid.id1,appointment_date=aid.order_date,menter_name=aid.menter_name,mentee_name=aid.mentee_name,resone="sorry")
        aid.payment=name
        aid.save()
        
        return redirect("show_refund")
    else:
        print("ok")    
        return render(request,"cancel_appointment.html",{"name":name})

def show_refund(request):
    r=refund_req.objects.all()
    r_count=refund_req.objects.count()

    r = [(item, index + 1) for index, item in enumerate(r)]

   
    contaxt={
        "r":r,
        "r_count":r_count,
    }
    return render(request,"refund_request.html",contaxt)
def refund_searchview(request):
    query = request.GET.get('query', '')
    products = refund_req.objects.filter(menter_name__icontains=query)
    # print(products)
    # products = appointment.objects.filter(
    #     Q(menter_name__icontains=query) | Q(mentee_name__icontains=query),status="canceled"
    # ).order_by("-id")

    # products = appointment.objects.filter(menter_name__icontains=query,status="canceled").order_by("-id")
    results = [{'row_number': index + 1,'id': product.id, 'id1': product.id1, 'menter_name': product.menter_name,
                'mentee_name': product.mentee_name,'appointment_date':product.appointment_date, 'order_date':product.order_date,
                'delete_url': reverse('delete_session', args=[product.id])} for index, product in enumerate(products)]
    return JsonResponse(results, safe=False)

def refund_filter(request):
    # cid = appointment.objects.filter(status="canceled")
    # cid = [(item, index + 1) for index, item in enumerate(cid)]

    if request.method == 'POST':
        from_date = request.POST.get('from_date')
        to_date = request.POST.get('to_date')
        products =  refund_req.objects.filter(appointment_date__range=(from_date, to_date))
        results = [{'row_number': index + 1,'id': product.id, 'id1': product.id1, 'menter_name': product.menter_name,
                'mentee_name': product.mentee_name, 'order_date':product.order_date,'appointment_date':product.appointment_date,
                'delete_url': reverse('delete_session', args=[product.id])} for index, product in enumerate(products)]
        return JsonResponse(results, safe=False)
    return JsonResponse(safe=False)






#--------------------------------------Mentor views--------------



def add_profile(request):
    mid=main_category.objects.all()
    sid = sub_category.objects.all()
    eid = expertise.objects.all()
    
    if request.POST:
        m_id = request.POST['m_id']
        s_id = request.POST['s_id']
        e_id = request.POST['e_id']
        IMG = request.FILES['IMG']
        name = request.POST['name']
        email = request.POST['email']
        headline = request.POST['headline']
        about_you = request.POST['about_you']
        cou = request.POST['cou']
        sta = request.POST['sta']
        cit = request.POST['cit']
        lunguages = request.POST['lunguages']
        links1 = request.POST['links1']
        links2 = request.POST['links2']
        ex_education =request.POST['ex_education']
        add_work = request.POST['add_work']
        add_education = request.POST['add_education']
        topics = request.POST['topics']
        price = request.POST['price']
        durations = request.POST['durations']
        topics_durations = request.POST['topics_durations']
        print(m_id,s_id,e_id)
        m=main_category.objects.get(id=m_id)
        s=sub_category.objects.get(id=s_id)
        e=expertise.objects.get(id=e_id)
        print(m,s)
        uid = Add_profile.objects.create(main=m,
                                         sub=s,
                                         exp=e,
                                         IMG=IMG,
                                         name=name,
                                         email=email,
                                         headline=headline,
                                         about_you=about_you,
                                         cou=cou,
                                         sta=sta,
                                         cit=cit,
                                         lunguages=lunguages,
                                         links1=links1,
                                         links2=links2,
                                         ex_education=ex_education,
                                         add_work=add_work,
                                         add_education=add_education,
                                         topics = topics,
                                         price = price,
                                         durations = durations,
                                         topics_durations = topics_durations,
                                         
        ) 
        return redirect("add_profile")
    else: 
        
        context = {
            'topic_price':topic_price,
            'topic_durations':topic_durations,
            'mid' : mid,
            'sid' : sid,
            'eid' : eid
        }
        return render(request,"add_profile.html",context)
        


def mentor_table(request):
    uid=Add_profile.objects.order_by("-id")
    mid=main_category.objects.all()
    
    uid = [(item, index + 1) for index, item in enumerate(uid)]

    m_id=request.GET.get("m_id")
    print(m_id)
    
    if m_id:
        uid=Add_profile.objects.filter(main=m_id)
    else:
        uid=Add_profile.objects.order_by("-id")
    
    uid = [(item, index + 1) for index, item in enumerate(uid)]
    main_categories = main_category.objects.all()
    sub_categories = sub_category.objects.all()    
    paginator = Paginator(uid, 5)
    page_number = request.GET.get('page')
    uid = paginator.get_page(page_number)
    
    contaxt={
        "uid" : uid,
        "mid" : mid,
        'main_categories':main_categories,
        'sub_categories':sub_categories,
    }
    return render(request,"mentor_table.html",contaxt)






def mentor_deletes(request,id):
    
    uid = Add_profile.objects.get(id=id)
    
    uid.delete()
    
    return redirect("mentor_table")


def MentorReview(request):
    return render(request,"MentorReview.html")
          
     
def Mentor_ViewPage(request,id):
    
    uid = Add_profile.objects.get(id=id)
    
    context = {
        'uid' : uid
    }
    return render(request,"Mentor_ViewPage.html",context)




def Mentor_View_Booking(request):
    return render(request,"Mentor_View_Booking.html")



def searchview(request):
    srch = request.GET["srch"]
    if srch:
        uid = Add_profile.objects.filter(name__contains=srch)
    contaxt={
        
        'uid' : uid
    }    
    return render(request,"mentor_table.html",contaxt)



def live_search(request):
    query = request.GET.get('query', '')
    products = Add_profile.objects.filter(name__icontains=query)
    print(products)
    results = [{'row_number': index + 1, 'id': product.id, 'name': product.name,
                'image_url': product.IMG.url,'cit':product.cit,'sta':product.sta,
                'view_url': reverse('Mentor_ViewPage', args=[product.id]), 
                'block_url': reverse('toggle_block_profile', args=[product.id]),
                'delete_url': reverse('mentor_deletes', args=[product.id])} for index, product in enumerate(products)]
    print(results)
    return JsonResponse(results, safe=False)



def state_city_srch(request):
    uid=Add_profile.objects.order_by("-id")
    mid=main_category.objects.all()
    
    uid = [(item, index + 1) for index, item in enumerate(uid)]

    paginator = Paginator(uid, 5)
    page_number = request.GET.get('page')
    uid= paginator.get_page(page_number)
    main_categories = main_category.objects.all()
    sub_categories = sub_category.objects.all()  
    contaxt={
        "uid" : uid,
        "mid" : mid,
        'main_categories':main_categories,
        'sub_categories':sub_categories,
    }
    return render(request,"state_city_srch.html",contaxt)
    
  
def state_citey_livesrch(request):
    query = request.GET.get('query', '')
    # products = Add_profile.objects.filter(sta__icontains=query)
    products = Add_profile.objects.filter(
        Q(cit__icontains=query) | Q(sta__icontains=query))
    print(products)
    results = [{'row_number': index + 1, 'id': product.id, 'name': product.name,
                'image_url': product.IMG.url,'cit':product.cit,'sta':product.sta,
                'view_url': reverse('Mentor_ViewPage', args=[product.id]), 
                'block_url': reverse('toggle_block_profile', args=[product.id]),
                'delete_url': reverse('mentor_deletes', args=[product.id])} for index, product in enumerate(products)]
    print(results)
    return JsonResponse(results, safe=False)

    
    
    

def toggle_block_profile(request, id):
    mentee1 = Add_profile.objects.get(id=id)

    if mentee1.blocked:
        mentee1.blocked = False
    
    else:
        mentee1.blocked = True
        
        
    mentee1.save()
    return redirect('mentor_table')

def block_profile_list(request):
    
    uid = Add_profile.objects.filter(blocked=True)
    mid=main_category.objects.all()
    
    uid = [(item, index + 1) for index, item in enumerate(uid)]
    
    contaxt={
        "uid" : uid,
        "mid" : mid,
    }
    return render(request,"mentor_table.html",contaxt)



def add_work_form(request):
    
    if request.POST:
        
        company_name = request.POST["company_name"]
        titel = request.POST['titel']
        current_role = request.POST['current_role']
        start_month = request.POST['start_month']
        start_year = request.POST['start_year']
        end_month = request.POST['end_month']
        end_year = request.POST['end_year']
        
        uid = Add_work.objects.create(company_name=company_name,
                                      titel=titel,
                                      current_role=current_role,
                                      start_month=start_month,
                                      start_year=start_year,
                                      end_month=end_month,
                                      end_year=end_year)
        return redirect("add_profile")
    
    else:
        return redirect("add_profile")
        
        
    





#=============================================================================
#**********************---MENTEE FORM---**********************
def mentee_form(request):
    mid=main_category.objects.all()
    sid = sub_category.objects.all()
    eid = expertise.objects.all()
    
    if request.POST:
        mcategory = request.POST['mcategory']
        scategory = request.POST['scategory']
        ecategory = request.POST['ecategory']
        img=request.FILES['img']
        name = request.POST['name']
        email = request.POST['email']
        headline = request.POST['headline']
        about_you = request.POST['about_you']
        cou = request.POST['cou']
        sta = request.POST['sta']
        cit = request.POST['cit']
        languages = request.POST['languages']
       
        ex_education =request.POST['ex_education']
        add_work = request.POST['add_work']
        add_education = request.POST['add_education']
     
        m=main_category.objects.get(id=mcategory)
        s=sub_category.objects.get(id=scategory)
        e=expertise.objects.get(id=ecategory)
      
        mentee.objects.create(mcategory=m,
                                         scategory=s,
                                         ecategory=e,
                                         image=img,
                                         name=name,
                                         email=email,
                                         headline=headline,
                                         about_you=about_you,
                                         cou=cou,
                                         sta=sta,
                                         cit=cit,
                                         languages=languages,
                                         
                                         ex_education=ex_education,
                                         add_work=add_work,
                                         add_education=add_education,
                                         
                                        
                                         
        ) 
        return redirect("show_mentee_data")
    else: 
        
        context = {
            'mid' : mid,
            'sid' : sid,
            'eid' : eid
        }
        
        return render(request,"mentee_form.html",context)







"""*******************LOCATION SEARCH***************************"""
def location_search(request):
    if request.POST:
        city=request.POST['city']
        cit=request.POST['cit']
        uid=mentee.objects.create(
                                city=city,
                                cit=cit,


        )
        uid.save()

    # con={
    #     'uid':uid,
       
    # }
    return render(request,"location_Search.html")





"""*****************----SHOW MENTEE DATA FORM----*********************"""
def show_mentee_data(request):
   
    sid=mentee.objects.order_by("-id")
    s=sid.count()
    sid1=mentee.objects.count()
    sid = [(item, index + 1) for index, item in enumerate(sid)]


    
    main_categories = main_category.objects.all()
    sub_categories = sub_category.objects.all()

    paginator = Paginator(sid, 5)
    page_number = request.GET.get('page')
    sid= paginator.get_page(page_number)
    
    contaxt={
        "sid":sid,
        "sid1":sid1,
        'main_categories':main_categories,
        'sub_categories':sub_categories,

     
    }
    return render(request,"show_mentee_data.html",contaxt)






"""*******************--EDIT MENTEE FORM--*************************"""
def edit_mentee_form(request,id):
    mid=mentee.objects.all()
    sid=mentee.objects.get(id=id)
    mmid=main_category.objects.all()
    ssid = sub_category.objects.all()
    eeid = expertise.objects.all()   
    
    if request.POST:
        mcategory = request.POST['mcategory']
        scategory = request.POST['scategory']
        ecategory = request.POST['ecategory']
        img=request.FILES['img']
        name=request.POST['name']
        email=request.POST['email']
        title=request.POST['title']
        headline=request.POST['headline']
        about_you=request.POST['about_you']
        country=request.POST['country']
        state=request.POST['state']
        city=request.POST['city']
        cou=request.POST['cou']
        sta=request.POST['sta']
        cit=request.POST['cit']
        languages = request.POST['languages']
        
        ex_education=request.POST['ex_education']
        # experti=request.POST['experti']
        add_work=request.POST['add_work']
        add_education=request.POST['add_education']
        m=main_category.objects.get(id=mcategory)
        s=sub_category.objects.get(id=scategory)
        e=expertise.objects.get(id=ecategory)



        if "img1" in request.FILES:
            img=request.FILES['img1']
            
           
            sid.image=img
            sid.name=name
            sid.email=email
            sid.title=title
            sid.headline=headline
            sid.about_you=about_you
            sid.country=country
            sid.state=state
            sid.city=city
            sid.cou=cou
            sid.sta=sta
            sid.cit=cit
            # mid.languages=','.join(languages),
            sid.languages=languages
            sid.ex_education=ex_education
            # mid.experti=experti
            sid.add_work=add_work
            sid.add_education=add_education
            sid.mcategory=m
            sid.scategory=s
            sid.ecategory=e
            sid.save()
            messages.success(request,"Profile Updated Successful")  
            return redirect('show_mentee_data')
        else:
            sid.image=img
            sid.name=name
            sid.email=email
            sid.title=title
            sid.headline=headline
            sid.about_you=about_you
            sid.country=country
            sid.state=state
            sid.city=city
            sid.cou=cou
            sid.sta=sta
            sid.cit=cit
            # mid.languages=','.join(languages),
            sid.languages=languages
            sid.ex_education=ex_education
            # mid.experti=experti
            sid.add_work=add_work
            sid.add_education=add_education
            sid.mcategory=m
            sid.scategory=s
            sid.ecategory=e
            sid.save()    
            messages.success(request,"Profile Updated Successful")  
            return redirect('show_mentee_data') 
    else:
        contaxt={
            "mid":mid,
            "sid":sid,
            'mmid':mmid,
            'ssid':ssid,
            'eeid':eeid,
            
            
        }
        return render(request,'edit_mentee_form.html',contaxt)  






"""***********************----DELETE----*************************"""
def delete_mentee_data(request,id):
    sid=mentee.objects.get(id=id)
    sid.delete()
    # messages.success(request," Deleted Successful")
    return redirect('show_mentee_data')   






"""***********************----VIEW PROFILE----**************************"""
def view_form(request,id):
    uid = mentee.objects.get(id=id)
    
    context = {
        'uid' : uid,
    }
    return render(request,"view_form.html",context)






"""***********************----SEARCH----*******************"""
def search_mentee(request):
    query = request.GET.get('query', '')
    products = mentee.objects.filter(name__icontains=query)
    results = [{'row_number': index + 1, 'id': product.id, 'name': product.name,
                'image_url': product.image.url,'cit':product.cit,'sta':product.sta,
                'view_url': reverse('view_form', args=[product.id]), 
                'block_url': reverse('toggle_block_profile1', args=[product.id]),
                'edit_url': reverse('edit_mentee_form', args=[product.id]),
                'delete_url': reverse('delete_mentee_data', args=[product.id])} for index, product in enumerate(products)]
    return JsonResponse(results, safe=False)






"""***********************----BLOCK UNBLOCK ----*****************"""
def toggle_block_profile1(request, id):
    mentee1 = mentee.objects.get(id=id)

    if mentee1.blocked:
        mentee1.blocked = False
       
    else:
        mentee1.blocked = True
        

    mentee1.save()
    return redirect('show_mentee_data')



# def toggle_block_profile(request, id):
#     mentee1 = Add_profile.objects.get(id=id)

#     if mentee1.blocked:
#         mentee1.blocked = False
    
#     else:
#         mentee1.blocked = True
        
        
#     mentee1.save()
#     return redirect('mentor_table')
"""*****************----VIEW_BOOKING UPCOMING OR HISTORY----*******"""
def view_booking(request,id):
    sid=mentee.objects.get(id=id)

    contaxt={
        "sid":sid,
    
    }
    return render(request,"view_booking.html",contaxt)




"""****************BLOCKED PROFILE LIST SHOW****************************"""
def blocked_profile_list1(request):
    main_categories = main_category.objects.all()

    uid = mentee.objects.filter(blocked=True)
    sid = [(item, index + 1) for index, item in enumerate(uid)]


    contaxt={
        "uid":uid,
        "sid":sid,
        'main_categories':main_categories,
     
    }
    return render(request,"show_mentee_data.html",contaxt)

#===================================================================
   

def state_city_search(request):
    sid=mentee.objects.order_by("-id")
    mid=main_category.objects.all()
    
    sid = [(item, index + 1) for index, item in enumerate(sid)]

    paginator = Paginator(sid, 5)
    page_number = request.GET.get('page')
    sid= paginator.get_page(page_number)
    main_categories = main_category.objects.all()
    sub_categories = sub_category.objects.all()  
    contaxt={
        "sid" : sid,
        "mid" : mid,
        'main_categories':main_categories,
        'sub_categories':sub_categories,
    }
    return render(request,"state_city_search.html",contaxt)



