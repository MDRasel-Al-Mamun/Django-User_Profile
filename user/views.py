from .models import UserProfile
from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required


@login_required(login_url='signin')
def profile(request):
    current_user = request.user
    profile = UserProfile.objects.get(user_id=current_user.id)
    context = {
        'profile': profile,
    }
    return render(request, 'user/profile.html', context)


@login_required(login_url='signin')
def profileUpdate(request):
    profile = UserProfile.objects.get(user__id=request.user.id)
    values = UserProfile.objects.get(user__id=request.user.id)
    context = {
        'profile': profile,
        'values': values
    }
    if request.method == 'POST':
        first_name = request.POST["first_name"]
        last_name = request.POST["last_name"]
        email = request.POST["email"]
        designation = request.POST["designation"]
        birthday = request.POST["birthday"]
        biography = request.POST["biography"]
        address = request.POST["address"]
        phone = request.POST["phone"]
        website_url = request.POST["website_url"]
        facebook_url = request.POST["facebook_url"]
        twitter_url = request.POST["twitter_url"]
        instagram_url = request.POST["instagram_url"]
        github_url = request.POST["github_url"]

        user = User.objects.get(id=request.user.id)
        user.first_name = first_name
        user.last_name = last_name
        user.email = email
        user.save()

        values.designation = designation
        values.birthday = birthday
        values.biography = biography
        values.address = address
        values.phone = phone
        values.website_url = website_url
        values.facebook_url = facebook_url
        values.twitter_url = twitter_url
        values.instagram_url = instagram_url
        values.github_url = github_url
        values.save()

        if "image" in request.FILES:
            image = request.FILES["image"]
            values.image = image
            values.save()

        return redirect('profile')

    return render(request, 'user/update.html', context)


@login_required(login_url='signin')
def change_password(request):
    profile = UserProfile.objects.get(user__id=request.user.id)
    context = {
        'profile': profile,
    }
    if request.method == 'GET':
        return render(request, 'user/change_password.html', context)

    if request.method == 'POST':
        old_password = request.POST['old_password']
        password = request.POST['password']

        user = User.objects.get(id=request.user.id)
        check = user.check_password(old_password)
        if check == True:
            user.set_password(password)
            user.save()
            messages.success(request, 'Password Change Successfully')
            user = User.objects.get(username=user.username)
            login(request, user)
            return redirect('profile')
        else:
            messages.error(request, 'Old password is not metch')
            return render(request, 'user/change_password.html', context)

        return render(request, 'user/change_password.html', context)


@login_required(login_url='signin')
def delete_account(request):
    if request.method == 'POST':
        user = User.objects.get(username=request.user)
        user.is_active = False
        user.save()
        return redirect('signin')
    return render(request, 'user/delete_account.html')
