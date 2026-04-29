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

    org_requests_view,
    approve_org_request_view,
    org_dashboard_view,
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
    # ADMIN REQUESTS
    # ======================
    path("requests/", org_requests_view, name="org_requests"),
    path(
        "requests/<int:request_id>/approve/",
        approve_org_request_view,
        name="approve_org_request"
    ),

    # ======================
    # DASHBOARD
    # ======================
    path("dashboard/", org_dashboard_view, name="org_dashboard"),

    path(
        "dashboard/regenerate-code/",
        regenerate_join_code_view,
        name="regenerate_join_code"
    ),
     path("terms/", terms, name="terms"),
    path("privacy/",privacy, name="privacy"),
]