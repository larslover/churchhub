from django.urls import path
from .views import (
    signup_view,
    login_view,
    logout_view,
    organization_signup_view,
    connect_organization_view,
    find_church_view,
    request_org_access_view,
    org_requests_view,
    approve_org_request_view,
    org_dashboard_view
)

urlpatterns = [
    path("signup/", signup_view, name="signup"),
    path("login/", login_view, name="login"),
    path("logout/", logout_view, name="logout"),

    # Create organization
    path("org-signup/", organization_signup_view, name="org_signup"),

    # User onboarding
    path("connect/", connect_organization_view, name="connect_organization"),
    path("find-church/", find_church_view, name="find_church"),

    # Join requests
    path(
        "request-access/<int:org_id>/",
        request_org_access_view,
        name="request_org_access"
    ),

    # Admin approvals
    path("requests/", org_requests_view, name="org_requests"),

    path(
        "requests/<int:request_id>/approve/",
        approve_org_request_view,
        name="approve_org_request"
    ),



    path("dashboard/", org_dashboard_view, name="org_dashboard"),
    path("requests/", org_requests_view, name="org_requests"),
    path("requests/<int:request_id>/approve/", approve_org_request_view, name="approve_org_request"),
]
