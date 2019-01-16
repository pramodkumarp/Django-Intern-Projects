from django.shortcuts import render, redirect
from BlogApp.forms import *
from BlogApp.models import *
import random, hashlib, socket, platform
from django.contrib import messages
from django.conf import settings
from django.core.mail import send_mail


def signup(request):
    if request.method == "POST":
        user_form = UserForm(request.POST)
        name_form = NameForm(request.POST)
        gender_form = GenderForm(request.POST)
        bd_form = BirthDayForm(request.POST)

        if user_form.is_valid() and name_form.is_valid() and gender_form.is_valid() and bd_form.is_valid():
            name = name_form.cleaned_data['fname']
            surname = name_form.cleaned_data['lname']
            NameTable.objects.create(fname=name, lname=surname)
            name_ref = NameTable.objects.filter(fname=name, lname=surname).last()

            gender = gender_form.cleaned_data['gender']
            GenderTable.objects.create(gender=gender)
            gender_ref = GenderTable.objects.filter(gender=gender).last()

            birthday = bd_form.cleaned_data['birthday']
            birthmonth = bd_form.cleaned_data['birthmonth']
            birthyear = bd_form.cleaned_data['birthyear']
            BirthdayTable.objects.create(birthday=birthday, birthmonth=birthmonth, birthyear=birthyear)
            bd_ref = BirthdayTable.objects.filter(birthday=birthday, birthmonth=birthmonth, birthyear=birthyear).last()

            email = user_form.cleaned_data['email']
            psd = user_form.cleaned_data['confirm_password']
            password = hashlib.md5(psd.encode()).hexdigest()
            email_verification_code = random.randint(10000,1000000)

            ProfilePhotoTable.objects.create(profile_photo="default")
            pp_ref = ProfilePhotoTable.objects.filter(profile_photo="default").last()

            device_name = socket.gethostname()
            ip_address = socket.gethostbyname(socket.gethostname())
            current_os = platform.platform()
            os_quality = platform.system()
            machine_type = platform.machine()
            device_details = platform.uname()

            DeviceDetailsTable.objects.create(device_name=device_name, ip_address=ip_address, current_os=current_os, os_quality=os_quality, machine_type=machine_type, device_details=device_details)

            device_ref = DeviceDetailsTable.objects.filter(device_name=device_name, ip_address=ip_address, current_os=current_os, os_quality=os_quality, machine_type=machine_type, device_details=device_details).last()

            name_obj = NameTable.objects.get(id=name_ref.id)
            gender_obj = GenderTable.objects.get(id=gender_ref.id)
            bd_obj = BirthdayTable.objects.get(id=bd_ref.id)
            pp_obj = ProfilePhotoTable.objects.get(id=pp_ref.id)
            device_obj = DeviceDetailsTable.objects.get(id=device_ref.id)

            UserTable.objects.create(email_address = email, email_verification_code = email_verification_code, password=password, name_table = name_obj, gender_table=gender_obj, birthday_table = bd_obj, profile_completion = 40, pp_table=pp_obj, device_table=device_obj)

            subject = "Demo App Email Verification Code."
            sender = settings.EMAIL_HOST_USER
            receiver = [[email], ]
            body = f"Hello {name} {surname},\nWelcome to my demo testing web application. Thanks for your kind interest and help me to test the app performance.\nYour demo app verification code is {email_verification_code}. Don't share this code with others for your account safety.\nThanks, Engr. Shaumik Ghosh."
            send_mail(subject, body, sender, receiver)

            msg = f"Hello {name} {surname}, An email verification code has been sent to your email from {sender}. Check your email and collect the code with 6 digits then verify your email. Thanks."

            MessageTable.objects.create(message=msg)
            msg_ref = MessageTable.objects.filter(message=msg).last()
            msg_obj = MessageTable.objects.get(id=msg_ref.id)

            user = UserTable.objects.get(email_address=email)
            user.msg_tabl = msg_obj
            user.save()

            request.session['id'] = user.id
            request.session['name'] = user.name_table.fname+" "+user.name_table.lname
            request.session['email'] = email
            request.session['email_validity'] = user.email_validity
            request.session['user_activity'] = user.user_activity
            request.session['rcver_mail'] = receiver[0][0]
            request.session['sender_mail'] = sender
            request.session['profile_completion'] = user.profile_completion
            request.session['gender'] = user.gender_table.gender
            request.session['pp'] = str(user.pp_table.profile_photo)
            request.session['slug_name'] = user.name_table.slug_name
            request.session['message'] = user.msg_tabl.message

            return redirect('profile')
        else:
            print(user_form.errors, name_form.errors, gender_form.errors, bd_form.errors)
        return render(request, 'frontend/public/signup/signup.html', {'user_form':user_form, 'name_form':name_form, 'gender_form':gender_form, 'bd_form':bd_form})
    else:
        user_form = UserForm()
        name_form = NameForm()
        gender_form = GenderForm()
        bd_form = BirthDayForm()
        return render(request, 'frontend/public/signup/signup.html', {'user_form':user_form, 'name_form':name_form, 'gender_form':gender_form, 'bd_form':bd_form})



def profile(request):
    if request.method == "POST":
        code = EmailConfirmCode(request.POST)
        address = AddressForm(request.POST)
        imgform = UploadImage(request.POST, request.FILES)
        postForm = PostForm(request.POST, request.FILES)

        if code.is_valid():
            user_id = request.POST['id']
            code = code.cleaned_data['code']
            user = UserTable.objects.get(id=user_id)
            if user.email_verification_code.__eq__(code):
                msg = f"Hello {user.name_table.fname} {user.name_table.lname}, Your email is successfully verified! Your account completed {user.profile_completion}%. Sorry to inform you, Settings and ViewProfile won't be activated till 100% profile completion. Thanks."

                MessageTable.objects.create(message=msg)
                msg_ref = MessageTable.objects.filter(message=msg).last()
                msg_obj = MessageTable.objects.get(id=msg_ref.id)
                user.email_validity = 1
                user.msg_tabl = msg_obj
                user.save()

                request.session['id'] = user.id
                request.session['name'] = user.name_table.fname + " " + user.name_table.lname
                request.session['email'] = user.email_address
                request.session['email_validity'] = user.email_validity
                request.session['user_activity'] = user.user_activity
                request.session['profile_completion'] = user.profile_completion
                request.session['gender'] = user.gender_table.gender
                request.session['pp'] = str(user.pp_table.profile_photo)
                request.session['slug_name'] = user.name_table.slug_name
                request.session['message'] = user.msg_tabl.message

                return redirect('profile')
            else:
                code = EmailConfirmCode()
                messages.error(request, "Verification code didn't match", {'form': code})
        else:
            print(code.errors)

        if address.is_valid():
            user_id = request.POST['id']
            vlg = address.cleaned_data['village']
            cty = address.cleaned_data['city']
            zp = address.cleaned_data['zip']
            cntry = address.cleaned_data['country']
            AddressTable.objects.create(village=vlg, city=cty, zip=zp, country=cntry)
            address_ref = AddressTable.objects.filter(village=vlg, city=cty, zip=zp, country=cntry).last()

            user = UserTable.objects.get(id=user_id)
            adrst = AddressTable.objects.get(id=address_ref.id)

            user.address_table = adrst
            user.profile_completion = 80

            msg = f"Thanks {user.name_table.fname} {user.name_table.lname}, last process was done successfully! Your account completed {user.profile_completion}%, You may upload your photo or skip this step to complete yout profile 100%. Sorry to inform you, Settings and ViewProfile won't be activated till 100% profile completion."

            MessageTable.objects.create(message=msg)
            msg_ref = MessageTable.objects.filter(message=msg).last()
            msg_obj = MessageTable.objects.get(id=msg_ref.id)

            user.msg_tabl = msg_obj
            user.save()

            request.session['id'] = user.id
            request.session['name'] = user.name_table.fname + " " + user.name_table.lname
            request.session['email'] = user.email_address
            request.session['email_validity'] = user.email_validity
            request.session['user_activity'] = user.user_activity
            request.session['profile_completion'] = user.profile_completion
            request.session['gender'] = user.gender_table.gender
            request.session['pp'] = str(user.pp_table.profile_photo)
            request.session['slug_name'] = user.name_table.slug_name
            request.session['message'] = user.msg_tabl.message

            return redirect('profile')
        else:
            print(address.errors)

        if imgform.is_valid():
            user_id = request.POST['id']
            image = imgform.cleaned_data['upimage']
            img = ProfilePhotoTable(
                profile_photo=image
            )
            img.save()
            image_ref = ProfilePhotoTable.objects.filter(profile_photo=image).last()
            image_obj = ProfilePhotoTable.objects.get(id=image_ref.id)

            user = UserTable.objects.get(id=user_id)
            user.pp_table = image_obj
            user.profile_completion = 100

            msg = f"Thanks {user.name_table.fname} {user.name_table.lname}, Your account is {user.profile_completion}% completed. Therefore, Settings and ViewProfile is activated now. But your profile is under review. It will be reviewed manually. Once your profile is approved you will be able to create posts, like and comments."

            MessageTable.objects.create(message=msg)
            msg_ref = MessageTable.objects.filter(message=msg).last()
            msg_obj = MessageTable.objects.get(id=msg_ref.id)
            user.msg_tabl = msg_obj
            user.save()

            request.session['id'] = user.id
            request.session['name'] = user.name_table.fname + " " + user.name_table.lname
            request.session['email'] = user.email_address
            request.session['email_validity'] = user.email_validity
            request.session['user_activity'] = user.user_activity
            request.session['profile_completion'] = user.profile_completion
            request.session['gender'] = user.gender_table.gender
            request.session['pp'] = str(user.pp_table.profile_photo)
            request.session['slug_name'] = user.name_table.slug_name
            request.session['message'] = user.msg_tabl.message

            return redirect('profile')
        else:
            print(imgform.errors)

        return render(request, 'frontend/user/profile/profile.html', {'form': code, 'address':address, 'imgform':imgform, 'postForm':postForm})
    else:
        if request.session.has_key("id"):
            code = EmailConfirmCode()
            address = AddressForm()
            imgform = UploadImage()
            postForm = PostForm()
            return render(request, 'frontend/user/profile/profile.html', {'form':code, 'address':address,'imgform':imgform, 'postForm':postForm})
        else:
            return redirect('login')


def resend_verification_code(request, name):
    name = NameTable.objects.get(slug_name=name)
    user = UserTable.objects.get(id=name.id)
    code = random.randint(10000,1000000)

    msg = f"The email verification code has been resent to your email from {settings.EMAIL_HOST_USER}. Check your email and collect the code with 6 digits then verify your email. Thanks."

    MessageTable.objects.create(message=msg)
    msg_ref = MessageTable.objects.filter(message=msg).last()
    msg_obj = MessageTable.objects.get(id=msg_ref.id)
    user.msg_tabl = msg_obj
    user.email_verification_code = code
    user.save()

    subject = "Demo App Email Verification Code."
    sender = settings.EMAIL_HOST_USER
    receiver = [[user.email_address], ]
    body = f"Hello {user.name_table.fname} {user.name_table.lname},\nWelcome to my demo testing web application. Thanks for your kind interest and help me to test the app performance.\nYour demo app verification code is {code}. Don't share this code with others for your account safety.\nThanks, Engr. Shaumik Ghosh."
    send_mail(subject, body, sender, receiver)

    request.session['id'] = user.id
    request.session['name'] = user.name_table.fname + " " + user.name_table.lname
    request.session['email'] = user.email_address
    request.session['email_validity'] = user.email_validity
    request.session['user_activity'] = user.user_activity
    request.session['profile_completion'] = user.profile_completion
    request.session['gender'] = user.gender_table.gender
    request.session['pp'] = str(user.pp_table.profile_photo)
    request.session['slug_name'] = user.name_table.slug_name
    request.session['message'] = user.msg_tabl.message

    return redirect('profile')



def skip_uploading_image(request, name):
    name = NameTable.objects.get(slug_name=name)
    user = UserTable.objects.get(id=name.id)

    user.profile_completion = 100

    msg = f"Thanks {user.name_table.fname} {user.name_table.lname}, Your account is {user.profile_completion}% completed. Therefore, Settings and ViewProfile is activated now. But your profile is under review. It will be reviewed manually. Once your profile is approved you will be able to create posts, like and comments."

    MessageTable.objects.create(message=msg)
    msg_ref = MessageTable.objects.filter(message=msg).last()
    msg_obj = MessageTable.objects.get(id=msg_ref.id)

    user.msg_tabl = msg_obj
    user.save()

    request.session['id'] = user.id
    request.session['name'] = user.name_table.fname + " " + user.name_table.lname
    request.session['email'] = user.email_address
    request.session['email_validity'] = user.email_validity
    request.session['user_activity'] = user.user_activity
    request.session['profile_completion'] = user.profile_completion
    request.session['gender'] = user.gender_table.gender
    request.session['pp'] = str(user.pp_table.profile_photo)
    request.session['slug_name'] = user.name_table.slug_name
    request.session['message'] = user.msg_tabl.message

    messages.success(request, 'You have choiced to keep default profile Image. No problem you are allowed to change your profile picture browsing settings if wanna do in the future, Thanks.')

    return redirect('profile')


def login(request):
    if request.method=="POST":
        loginform = LoginForm(request.POST)
        if loginform.is_valid():
            try:
                given_email = loginform.cleaned_data['email']
                password = loginform.cleaned_data['password']
                given_password = hashlib.md5(password.encode()).hexdigest()
                lgn = UserTable.objects.get(email_address=given_email, password=given_password)

                if lgn.email_address.__eq__(given_email) and lgn.password.__eq__(given_password):
                    request.session['id'] = lgn.id
                    request.session['name'] = lgn.name_table.fname + " " + lgn.name_table.lname
                    request.session['email'] = lgn.email_address
                    request.session['email_validity'] = lgn.email_validity
                    request.session['user_activity'] = lgn.user_activity
                    request.session['profile_completion'] = lgn.profile_completion
                    request.session['gender'] = lgn.gender_table.gender
                    request.session['pp'] = str(lgn.pp_table.profile_photo)
                    request.session['slug_name'] = lgn.name_table.slug_name
                    request.session['message'] = lgn.msg_tabl.message

                    return redirect('profile')
            except:
                messages.error(request, "Email or Password Error!")
                return redirect('login')
        else:
            print(loginform.errors)
        return render(request, 'frontend/public/login/login.html', {'form':loginform})
    else:
        loginform = LoginForm()
        return render(request, 'frontend/public/login/login.html', {'form':loginform})


def logout(request):
    request.session.clear()
    request.session.flush()
    return redirect('login')


#   python manage.py migrate