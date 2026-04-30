from django.urls import path
from . import views
app_name = "org_admin"
urlpatterns = [
    path("dashboard/", views.org_dashboard_view, name="org_dashboard"),
    path("requests/", views.org_requests_view, name="org_requests"),
    path("requests/approve/<int:request_id>/", views.approve_org_request_view, name="approve_org_request"),
]