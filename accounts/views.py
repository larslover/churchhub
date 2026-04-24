from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from .forms import CustomUserCreationForm


def signup_view(request):
    if request.method == "POST":
        post_data = request.POST.copy()

        country_code = post_data.get("country_code", "").strip()
        local_phone = post_data.get("local_phone", "").strip().replace(" ", "").replace("-", "")

        post_data["phone"] = f"{country_code}{local_phone}"

        form = CustomUserCreationForm(post_data)

        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("home")
    else:
        form = CustomUserCreationForm()

    return render(request, "registration/signup.html", {"form": form})


def login_view(request):
    if request.method == "POST":
        identifier = request.POST.get("identifier", "").strip()
        password = request.POST.get("password", "")
        country_code = request.POST.get("country_code", "").strip()

        # If not email, treat as phone
        if "@" not in identifier:
            identifier = identifier.replace(" ", "").replace("-", "")
            identifier = f"{country_code}{identifier}"

        user = authenticate(request, username=identifier, password=password)

        if user is not None:
            login(request, user)
            return redirect("home")
        else:
            messages.error(request, "Invalid login credentials.")

    return render(request, "registration/login.html")


def logout_view(request):
    logout(request)
    return redirect("login")