from django.urls import path
from .views import (
    signup_view,
    login_view,
    logout_view,
    organization_signup_view,
    connect_organization_view,
    find_church_view,
    terms,
    privacy,

   
  
    regenerate_join_code_view,

)

urlpatterns = [

    # ======================
    # AUTH
    # ======================
    path("signup/", signup_view, name="signup"),
    path("login/", login_view, name="login"),
    path("logout/", logout_view, name="logout"),

    # ======================
    # ORGANIZATION SETUP
    # ======================
    path("org-signup/", organization_signup_view, name="org_signup"),

    # ======================
    # ONBOARDING
    # ======================
    path("connect/", connect_organization_view, name="connect_organization"),
    path("find-church/", find_church_view, name="find_church"),

    # ======================
    # JOIN FLOW (SINGLE SOURCE OF TRUTH)
    # ======================
 

    # ======================
    # REQUEST ACCESS
    # ======================


 
   

    # ======================
    # DASHBOARD
    # ======================
  

    path(
        "dashboard/regenerate-code/",
        regenerate_join_code_view,
        name="regenerate_join_code"
    ),
     path("terms/", terms, name="terms"),
    path("privacy/",privacy, name="privacy"),
]