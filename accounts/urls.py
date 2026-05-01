from django.urls import path
from .views import (
    signup_view,
    login_view,
    logout_view,
    organization_signup_view,
    connect_organization_view,
    find_church_view,
    request_access_view,
    regenerate_join_code_view,
    terms,
    privacy,
)

urlpatterns = [

    # AUTH
    path("signup/", signup_view, name="signup"),
    path("login/", login_view, name="login"),
    path("logout/", logout_view, name="logout"),

    # ORG SETUP
    path("org-signup/", organization_signup_view, name="org_signup"),

    # ONBOARDING
    path("connect/", connect_organization_view, name="connect_organization"),
    path("find-church/", find_church_view, name="find_church"),

    # REQUEST ACCESS
    path(
        "request-access/<int:org_id>/",
        request_access_view,
        name="request_access"
    ),

    # DASHBOARD
    path(
        "dashboard/regenerate-code/",
        regenerate_join_code_view,
        name="regenerate_join_code"
    ),

    # LEGAL
    path("terms/", terms, name="terms"),
    path("privacy/", privacy, name="privacy"),
]