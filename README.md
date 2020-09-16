# Django User Profile Project

To Create a User Profile System for Django Website

> - <a href="#model">1. Create User Profile Model </a>

> - <a href="#update-form">2. Update User Profile Form </a>

> - <a href="#details">3. Show Profile Details  </a>

> - <a href="#password">4. Change Password </a>

> - <a href="#account">5. Delete Account </a>

## 1. Create User Profile Model <a href="" name="model"> - </a>

1. Create a user app `python manage.py startapp user`
2. Define app - profileProject > settings > base.py - `'user.apps.UserConfig'` 
3. Create url - profileProject > urls.py - `path('user/', include('user.urls')),`
4. Create url file - `user > urls.py`

* user > models.py  

```python
from django.db import models
from django.dispatch import receiver
from django.contrib.auth.models import User
from django.utils.safestring import mark_safe
from django.db.models.signals import post_save


def user_directory_path(instance, filename):
    return 'user/avatars/{0}/{1}'.format(instance.user.id, filename)


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    designation = models.CharField(max_length=200, blank=True)
    birthday = models.DateField(auto_now=False, null=True, blank=True)
    biography = models.TextField(blank=True)
    address = models.CharField(max_length=200, blank=True)
    phone = models.CharField(blank=True, max_length=20)
    image = models.FileField(upload_to=user_directory_path, default='user/user.png')
    website_url = models.URLField(null=True, blank=True)
    facebook_url = models.URLField(null=True, blank=True)
    twitter_url = models.URLField(null=True, blank=True)
    instagram_url = models.URLField(null=True, blank=True)
    github_url = models.URLField(null=True, blank=True)

    def __str__(self):
        return self.user.username

    def full_name(self):
        return self.user.first_name + ' ' + self.user.last_name

    def image_tag(self):
        return mark_safe('<img src="{}" height="50"/>'.format(self.image.url))

    image_tag.short_description = 'Image'


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)

```

* user > admin.py

```python
from django.contrib import admin
from user.models import UserProfile


class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'designation', 'phone', 'image_tag']


admin.site.register(UserProfile, UserProfileAdmin)

```

1. Create a folder `media_root > user`
2. Set Default Image - media_root > user - `user.png`

## 2. Update User Profile Form <a href="" name="update-form"> - </a>

1. Create files - templates > user - `profile.html , update.html`

* user > views.py 

```python

from .models import UserProfile
from django.contrib import messages
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required


@login_required(login_url='signin')
def profile(request):
    context = {}
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

```

* user > urls.py 

```python
from django.urls import path
from .import views

urlpatterns = [
    path('profile/', views.profile, name='profile'),
    path('profile_update/', views.profileUpdate, name='update'),
]

```

* templates > user > update.html

```html

<form class="border border-light p-5" id="validation-form" enctype="multipart/form-data" action="" method="POST">

<p class="h4 mb-4 text-center ">Update Profile</p>

{% csrf_token %}
{% include 'partials/_messages.html' %}

<div class="row">
    <div class="col-md-8">
    <!-- First name -->
    <div class="col-md-12">
        <label for="first_name" class="text-muted">First name *</label>
        <input type="text" name="first_name" class="form-control" placeholder="Your first name" value="{{user.first_name}}">
    </div>

    <!-- Last name -->
    <div class="col-md-12">
        <label for="last_name" class="text-muted  mt-3">Last name *</label>
        <input type="text" name="last_name" class="form-control" placeholder="Your last name" value="{{user.last_name}}">
    </div>

    <!-- E-mail -->
    <div class="col-md-12">
        <label for="email" class="text-muted  mt-3">E-mail *</label>
        <input type="email" name="email" class="form-control" placeholder="email@example.com" value="{{user.email}}">
    </div>
    </div>
    <div class="col-md-4">
    <div class="profile-images-card">
        <div class="profile-images">
        <img src="{{values.image.url}}" id="upload-img">
        </div>
        <div class="custom-file">
        <label class="btn btn-info" for="fileupload">Upload Profile</label>
        <input type="file" name="image" value="{{values.image}}" id="fileupload">
        </div>
    </div>
    </div>
</div>

<!-- Designation -->
<div class="col">
    <label for="designation" class="text-muted  mt-3">Designation *</label>
    <input type="text" id="designation" name="designation" class="form-control"
    placeholder="Web designer & developer" value="{{values.designation}}">
</div>

<!-- Birthday -->
<div class="col">
    <label for="birthday" class="text-muted  mt-3">Birthday *</label>
    <input type="date" id="birthday" name="birthday" class="form-control"
    value="{{values.birthday|date:'Y-m-d'}}">
</div>

<!-- Biography -->
<div class="col">
    <label for="biography" class="text-muted  mt-3">Biography *</label>
    <textarea class="form-control" name="biography" id="biography" rows="3" cols="30"
    placeholder="Tell something about yourself">{{values.biography}}</textarea>
</div>

<!-- Address -->
<div class="col">
    <label for="address" class="text-muted  mt-3">Address *</label>
    <input type="text" id="address" name="address" class="form-control" placeholder="1234/A Main St. UK" value="{{values.address}}">
</div>

<!-- Phone -->
<div class="col">
    <label for="phone" class="text-muted  mt-3">Phone *</label>
    <input type="text" id="phone" name="phone" class="form-control" placeholder="+880 172xxxxxxx" value="{{values.phone}}">
</div>

<!-- Website Url -->
<div class="col">
    <label for="website_url" class="text-muted  mt-3">Website Url *</label>
    <input type="url" id="website_url" name="website_url" class="form-control"
    placeholder="https://mywebsite.com/" value="{{values.website_url}}">
</div>

<!-- Facebook Url -->
<div class="col">
    <label for="facebook_url" class="text-muted  mt-3">Facebook Url *</label>
    <input type="url" id="facebook_url" name="facebook_url" class="form-control"
    placeholder="https://www.facebook.com/" value="{{values.facebook_url}}">
</div>

<!-- Twitter Url -->
<div class="col">
    <label for="twitter_url" class="text-muted  mt-3">Twitter Url *</label>
    <input type="url" id="twitter_url" name="twitter_url" class="form-control"
    placeholder="https://twitter.com/" value="{{values.twitter_url}}">
</div>

<!-- Instagram Url -->
<div class="col">
    <label for="instagram_url" class="text-muted  mt-3">Instagram Url *</label>
    <input type="url" id="instagram_url" name="instagram_url" class="form-control"
    placeholder="https://www.instagram.com/" value="{{values.instagram_url}}">
</div>

<!-- Github Url -->
<div class="col">
    <label for="github_url" class="text-muted  mt-3">Github Url *</label>
    <input type="url" id="github_url" name="github_url" class="form-control"
    placeholder="https://github.com/" value="{{values.github_url}}">
</div>

<!-- Update Profile button -->
<button class="btn btn-info my-4 btn-block" name="update" type="submit">
    Upate Profile
</button>
</form>
```

1. Image field on form are created with `Jquery & Bootstrap`
2. static > js > main.js

```js
$(document).ready(function () {
  $('#fileupload').change(function (event) {
    var x = URL.createObjectURL(event.target.files[0]);
    $('#upload-img').attr('src', x);
    console.log(event);
  });
});

```
3. static > css > style.css 

```css
.profile-images-card {
  margin: auto;
  display: table;
}

.profile-images {
  width: 150px;
  height: 150px;
  border-radius: 50%;
  overflow: hidden;
}

.profile-images img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.custom-file input[type='file'] {
  display: none;
}

.custom-file label {
  cursor: pointer;
  text-align: center;
  display: table;
  margin: auto;
  margin-top: 10px;
}

```
4. Link to Url - `<a href="{% url 'update' %}" class="dropdown-item">Edit Profile</a>` 


## 3. Show Profile Details <a href="" name="details"> - </a>

* user > views.py 

```python
@login_required(login_url='signin')
def profile(request):
    current_user = request.user
    profile = UserProfile.objects.get(user_id=current_user.id)
    context = {
        'profile': profile,
    }
    return render(request, 'user/profile.html', context)
```

* templates > user > profile.html

```django
<div class="card">
    <div class="card-header">
        <h5 class="card-title mb-0">{{ profile.full_name }}</h5>
    </div>
    <div class="card-body">
        <div class="row">
            <div class="col-12 col-sm-12 col-md-5 col-lg-4 col-xl-3 col-xxl-3 text-center">
                <img src="{{ profile.image.url }}" width="180" height="180" class="rounded-circle mt-2" alt="{{ profile.full_name }}">
            </div>
            <div class="col-12 col-sm-12 col-md-7 col-lg-8 col-xl-9 col-xxl-9 pt-4 pl-4">
                <strong>About me</strong>

                {% if profile.biography %}
                    <p>{{ profile.biography }}</p>
                {% else %}
                    <p>
                    Lorem ipsum dolor sit amet consectetur adipisicing elit. Ex doloribus magnam in nisi ut maxime,consectetur unde quibusdam voluptates culpa natus ipsam voluptate quisquam omnis odit perferendis quos qui asperiores.
                    </p>
                {% endif %}

            </div>
        </div>
        <table class="table my-5">
            <tbody>
                <tr>
                    <th>Name</th>
                    <td>{{ profile.full_name }}</td>
                </tr>
                <tr>
                    <th>Designation</th>
                {% if profile.designation %}
                    <td>{{ profile.designation }}</td>
                {% else %}
                    <td>None</td>
                {% endif %}
                </tr>
                <tr>
                    <th>Email</th>
                    <td>{{ profile.user.email }}</td>
                </tr>
                <tr>
                    <th>Birthday</th>
                    <td>{{ profile.birthday }}</td>
                </tr>
                <tr>
                    <th>Address</th>
                {% if profile.address %}
                    <td>{{ profile.address }}</td>
                {% else %}
                    <td>None</td>
                {% endif %}
                </tr>
                <tr>
                    <th>Phone</th>
                {% if profile.phone %}
                    <td>{{ profile.phone }}</td>
                {% else %}
                    <td>None</td>
                {% endif %}
                </tr>
                <tr>
                    <th>Status</th>
                    <td><span class="">Active</span></td>
                </tr>
            </tbody>
        </table>
        <div class="row">
            <div class="social-icon col-md-8">
                <a href="{{ profile.website_url }}" class="text-warning mx-2">
                    <i class="fas fa-atlas fa-2x"></i>
                </a>
                <a href="{{ profile.facebook_url }}" class="text-primary mx-2">
                    <i class="fab fa-facebook-square fa-2x"></i>
                </a>
                <a href="{{ profile.twitter_url }}" class="text-info mx-2">
                    <i class="fab fa-twitter-square fa-2x"></i>
                </a>
                <a href="{{ profile.instagram_url }}" class="text-danger mx-2">
                    <i class="fab fa-instagram-square fa-2x"></i>
                </a>
                <a href="{{ profile.github_url }}" class="text-dark mx-2">
                    <i class="fab fa-github-square fa-2x"></i>
                </a>
            </div>
        </div>
    </div>
</div>
```
1. Link to Url - `<a href="{% url 'profile' %}" class="dropdown-item">Profile</a>` 

## 4. Change Password <a href="" name="password"> - </a>

1. Create file - templates > user - `change_password.html`

* user > views.py 

```python
from django.contrib.auth import login


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

```
* user > urls.py

```py
urlpatterns = [
    path('change_password/', views.change_password, name='change_password'),
]

```
* templates > user > change_password.html

```html
<form class="border border-light p-5" id="validation-form" method="POST">

    <p class="h4 mb-4 text-center ">Change Password</p>

    {% csrf_token %}
    {% include 'partials/_messages.html' %}

    <!-- Old Password -->
    <div class="col">
        <input type="password" name="old_password" class="form-control mt-4" placeholder="Old Password *">
    </div>

    <!-- Password -->
    <div class="col">
        <input type="password" id="passwordField" name="password" class="form-control mt-4" placeholder="New Password *">
    </div>

    <!-- Confirm Password -->
    <div class="col">
        <input type="password" id="" name="confirm_password" class="form-control mt-4"
        placeholder="Confirm Password *">
    </div>

    <!-- Set Password button -->
    <button class="btn btn-info my-4 btn-block" name="change_password" type="submit">
        Save Password
    </button>
</form>
```

1. Link to Url - `<a href="{% url 'change_password' %}" class="list-group-item"> Change Password </a>`

## 5. Delete Account <a href="" name="account"> - </a>

1. Create file - templates > user - `delete_account.html`

* user > views.py 

```python
@login_required(login_url='signin')
def delete_account(request):
    if request.method == 'POST':
        user = User.objects.get(username=request.user)
        user.is_active = False
        user.save()
        return redirect('signin')
    return render(request, 'user/delete_account.html')
```

* user > urls.py 

```python
urlpatterns = [
    path('delete_account/', views.delete_account, name='delete_account'),
]
```

* templates > user > delete_account.html

```html
<div class="text-center mt-5 pt-5">
    <h1>
        <span>Delete Account !</span>
    </h1>
    <h3 class="pt-3">
        Are you sure you want to delete your account?
    </h3>
    <div class="py-2"></div>
    <h6>
        *Important - your account data will remain available for 20 days
    </h6>
    <form action="{% url 'delete_account' %}" method="post">
        {% csrf_token %}
        <button type="submit" role="button" class="btn btn-danger mt-4">
        Confirm Delete
        </button>
    </form>
    <p class="pt-4">Not sure to dalete your account?
        <a class="btn btn-info btn-sm ml-2" href="{% url 'profile' %}">Back to Profile</a>
    </p>
    <p>Need to any help?
        <a class="btn btn-secondary btn-sm  ml-2" href="{% url 'signin' %}">Help Center</a>
    </p>
</div>
```
1. Link to Url - `<a href="{% url 'delete_account' %}" class="list-group-item"> Delete account </a>`

## Run This Demo -

Steps:

1. Clone/pull/download this repository
2. Create a virtualenv with `virtualenv venv` and install dependencies with `pip install -r requirements.txt`
3. Configure your .env variables
5. Collect all static files `python manage.py collectstatic`