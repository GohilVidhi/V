"""
URL configuration for myproject project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from .import views

urlpatterns = [
    # =================== index page  ====================
    path("",views.index,name="index"),
    # path("login",views.login_user,name="login"),
    # path("logout/",views.logoutUser,name="logout"),
    # =================== learning page ====================

    path("form",views.form,name="form"),
    path("table",views.table,name="table"),
    path("chart_view",views.chart_view,name="chart_view"),
    # =================== admin login ====================
    path("login",views.login,name="login"),
    path("logout",views.logout,name="logout"),
    path("forgot",views.forgot,name="forgot"),
    path("confirm_password",views.confirm_password,name="confirm_password"),
    # ====================== main category ===================
    path("add_main_category",views.add_main_category,name="add_main_category"),
    path("show_main_category",views.show_main_category,name="show_main_category"),
    path("delete_main_category/<int:id>",views.delete_main_category,name="delete_main_category"),
    path("edit_main_category/<str:id>",views.edit_main_category,name="edit_main_category"),
    # ================== main category searchview ====================
    path('main_searchview',views.main_searchview,name='main_searchview'),
    # ================== sub category ====================
    path("add_sub_category",views.add_sub_category,name="add_sub_category"),
    path("show_sub_category",views.show_sub_category,name="show_sub_category"),
    path("edit_sub_category/<str:id>",views.edit_sub_category,name="edit_sub_category"),
    path("delete_sub_category/<int:id>",views.delete_sub_category,name="delete_sub_category"),
    path('get_subcategories/', views.get_subcategories, name='get_subcategories'),
    # ================== sub category search ====================
    path('sub_searchview',views.sub_searchview,name='sub_searchview'),
    # ================== expertise ====================
    path("add_expertise",views.add_expertise,name="add_expertise"),
    path("show_expertise",views.show_expertise,name="show_expertise"),
    path("edit_expertise/<str:id>",views.edit_expertise,name="edit_expertise"),
    path("delete_expertise/<int:id>",views.delete_expertise,name="delete_expertise"),
     # ================== expertise search ====================
    path('expertise_searchview',views.expertise_searchview,name='expertise_searchview'),
    # ================== topic ====================
    path("add_topic",views.add_topic,name="add_topic"),
    path("show_topic",views.show_topic,name="show_topic"),
    path("edit_topic/<str:id>",views.edit_topic,name="edit_topic"),
    path("delete_topic/<int:id>",views.delete_topic,name="delete_topic"),
    # ================== topic search ====================
    path('topic_searchview',views.topic_searchview,name='topic_searchview'),
    # ================== price ====================
    path("add_price",views.add_price,name="add_price"),
    path("show_price",views.show_price,name="show_price"),
    path("edit_price/<str:id>",views.edit_price,name="edit_price"),
    path("delete_price/<int:id>",views.delete_price,name="delete_price"),
    # ================== price search ====================
    path('price_searchview',views.price_searchview,name='price_searchview'),
    # ================== sessiom ====================
    path("add_session",views.add_session,name="add_session"),
    path("show_session",views.show_session,name="show_session"),
    path("edit_session/<str:id>",views.edit_session,name="edit_session"),
    path("delete_session/<int:id>",views.delete_session,name="delete_session"),
    # ================== session search ====================
    path('session_searchview',views.session_searchview,name='session_searchview'),
    # ================== admin page  ====================
    path("admin_page",views.admin_page,name="admin_page"),
    # =================== upcoming appointment ====================
    path("upcoming_appointment",views.upcoming_appointment,name="upcoming_appointment"),
    path('upcoming_filter',views.upcoming_filter, name='upcoming_filter'),
    path("upcoming_searchview",views.upcoming_searchview,name="upcoming_searchview"),
    # =================== confirm appointment ====================
    path("confirm_appointment",views.confirm_appointment,name="confirm_appointment"),
    path('confirm_filter',views.confirm_filter, name='confirm_filter'),
    path("confirm_searchview",views.confirm_searchview,name="confirm_searchview"),
    # =================== cancel appointment ====================
    path("cancel_appointment",views.cancel_appointment,name="cancel_appointment"),
    path('cancel_filter',views.cancel_filter, name='cancel_filter'),
    path("cancel_searchview",views.cancel_searchview,name="cancel_searchview"),
    # =================== refund request ====================
    path('create_refund/<int:id>/',views.create_refund, name='create_refund'),
    path('show_refund',views.show_refund, name='show_refund'),
    path("refund_searchview",views.refund_searchview,name="refund_searchview"),
    path("refund_filter",views.refund_filter,name="refund_filter"),
    # =================== single appointment get ====================
    
    path("view_data/<int:id>",views.view_data,name="view_data"),


    

    # ==================
    # path('autocomplete/', views.autocomplete, name='autocomplete'),
    # path('person_create_view', views.person_create_view, name='person_add'),
    # path('<int:pk>/', views.person_update_view, name='person_change'),
    # path('ajax/load-cities/', views.load_cities, name='ajax_load_cities'), 
    
    
    
    
#--------------------------mentor------------------------------


    path("add_profile",views.add_profile,name="add_profile"),
    path("mentor_table",views.mentor_table,name="mentor_table"),
    path("mentor_deletes/<str:id>",views.mentor_deletes,name="mentor_deletes"),
    path("Mentor_ViewPage/<str:id>",views.Mentor_ViewPage,name="Mentor_ViewPage"),
    path("MentorReview",views.MentorReview,name="MentorReview"),
    path('searchview',views.searchview,name='searchview'),
    path('Mentor_View_Booking',views.Mentor_View_Booking,name='Mentor_View_Booking'),
    path('live_search', views.live_search, name='live_search'),
    path('toggle_block_profile/<int:id>/', views.toggle_block_profile, name='toggle_block_profile'),
    path('block_profile_list', views.block_profile_list, name='block_profile_list'),
    path('add_work_form', views.add_work_form, name='add_work_form'),
    path('state_city_srch', views.state_city_srch, name='state_city_srch'),
    path('state_citey_livesrch', views.state_citey_livesrch, name='state_citey_livesrch'),
    






# ============================== MENTEE =============================

    path('mentee_form',views.mentee_form,name='mentee_form'),
    path("show_mentee_data",views.show_mentee_data,name="show_mentee_data"),
    path('edit_mentee_form/<str:id>', views.edit_mentee_form, name='edit_mentee_form'),
    path("delete_mentee_data/<int:id>",views.delete_mentee_data,name="delete_mentee_data"),
    path('search_mentee',views.search_mentee,name='search_mentee'),
    path('view_form/<int:id>/',views.view_form,name='view_form'),
    path('toggle_block_profile1/<int:id>/', views.toggle_block_profile1, name='toggle_block_profile1'),
    path('view_booking/<int:id>/',views.view_booking,name='view_booking'),
    path('location_search',views.location_search,name='location_search'),
    path('blocked_profile_list1',views.blocked_profile_list1,name='blocked_profile_list1'),
    path('state_city_search',views.state_city_search,name='state_city_search'),
    # path('state_citey_livesrch1',views.state_citey_livesrch1,name='state_citey_livesrch1'),


]
