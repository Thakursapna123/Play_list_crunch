from django.shortcuts import render,redirect
from .models import *
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout
from .custom_twocheckout import *
from .helper import *
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import pyarrow.feather as feather
import pandas as pd
import datetime as dt
from django.http.response import JsonResponse
from django.contrib.auth.decorators import login_required
from django.conf import settings
import secrets, hashlib
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from django.utils import timezone
from datetime import timedelta
from datetime import datetime
import json
#

# Without Login Screen
def home(request):
    bannerData = AdminBannerTemplate.objects.all()
    people = AdminPeopleCommentedTemplate.objects.all()
    return render(request,'crunch/without_login/index.html',{'bannerData':bannerData,'people':people})

def signup(request):
    if request.method == "GET":
        return render(request,'crunch/without_login/auth_signup.html')
    if request.method == 'POST':
        page = "SignUp_Page"
        fullName = request.POST['fullName']
        emailAddress = request.POST['emailAddress']
        password = request.POST['password']
        confirmPassword = request.POST['confirmPassword']
        if(len(password.strip()) <8 or len(confirmPassword.strip()) <8):
            return render(request,'crunch/without_login/auth_signup.html',{'fail':'Password length must be minimum of 8 characters!','name':fullName,'email':emailAddress,'page':page})
        if(password.strip() != confirmPassword.strip()):
            return render(request,'crunch/without_login/auth_signup.html',{'fail':'Password not matched!','fullName':fullName,'emailAddress':emailAddress,'page':page})
        if User.objects.filter(username=emailAddress).exists():
            return render(request, 'crunch/without_login/auth_signup.html',{'fail':"An user with this email already exists!", 'fullName':fullName,'emailAddress':emailAddress,'page':page})
        try:
            user_fk = User.objects.create_user(username=emailAddress, email=emailAddress, password=password.strip(),first_name=fullName)
            user_fk.save()
            user_Profile = userProfile(userFK=user_fk, agree_receive_notify=True, agree_term_n_condition=True)
            user_Profile.save()
            page = "SignIn_Page"
            request.session['login_msg'] = 'Registration Successfull'
            baseURL = settings.BASE_URL
            sendEmailID= emailAddress
            salt = secrets.token_hex(8) + emailAddress
            token = hashlib.sha256(salt.encode('utf-8')).hexdigest()
            user_id = User.objects.get(username=emailAddress)
            time_now = timezone.now()
            token_updated, token_created = UserUniqueToken.objects.update_or_create(user_id=user_id, defaults={"token": token,'datetime':time_now})
            # sendEmail(emailAddress,baseURL,token,"VERIFYEMAIL")
            # request.session['login_msg'] = 'Check your mail to verify your account'
            return redirect("sigin")
        except:
            return render(request,'crunch/without_login/auth_signup.html',{'fullName':fullName,'emailAddress':emailAddress})

def sigin(request):
    if request.method == 'GET':
        msg = ''
        if 'login_msg' in request.session:
            msg = request.session['login_msg']
            del request.session['login_msg']
        return render(request,'crunch/without_login/auth_sigin.html',{'fail':msg})
    if request.method == 'POST':
            username = request.POST['emailAddress']
            password = request.POST['password']
            if username == '' or password == '':
                return render(request,'./auth_sigin.html', {'fail':'Username or Password should not be blank'})
            user = authenticate(username=username, password=password)
            if(user is not None):
                login(request, user)
                if user.first_name:
                    userID = userProfile.objects.filter(userFK=user.id).order_by('-create_at').first()
                    if userID is not None:
                        if(userID.payment_status and userID.subscribed):
                            username = request.user.first_name
                            now = datetime.now()
                            if(userID.subscription_expiry is not None):
                                if now.date() > userID.subscription_expiry.date():
                                    userID.payment_status = False
                                    userID.save()
                                    return redirect("payment")
                                else:
                                    if userID.payment_status:
                                        return redirect("search")
                                    else:
                                        return redirect("payment")
                            # return render(request,'crunch_app/Search1.html',{'username':username})
                        else:
                            return redirect('payment')
                    else:
                        userInstance = User.objects.get(id=request.user.id)
                        userID = userProfile(userFK=userInstance)
                        userID.save()
                        return redirect('payment')

                else:
                    print("RRRR",request.user.is_superuser)
                    if request.user.is_superuser:
                        login(request, user)
                        return redirect("admin_home")
                    else:
                        msg = "Your Account is not Active"
                        return render(request, 'crunch/without_login/auth_sigin.html',{'fail':msg})
            else:
                msg ='Username or Password is incorrect'
                return render(request,'crunch/without_login/auth_sigin.html',{'fail':msg})


def term_and_condition(request):
    return render(request,'crunch/without_login/term_n_condition_screen.html')


def privacy_policy(request):
    return render(request,'crunch/without_login/private_policy_screen.html')



def forgot_password(request):
    if request.method == "GET":
        return render(request,'crunch/without_login/auth_forgot_password.html')

    if request.method == 'POST':
        useremail = request.POST['useremail']
        if useremail == '':
            return render(request,'crunch/without_login/auth_forgot_password.html',{'fail':"Enter Registerd Email Address"})
        checkEmail = User.objects.filter(username=useremail)
        print("BJKB",checkEmail)
        if checkEmail:
            request.session['mail_user'] = useremail
            baseURL = settings.BASE_URL
            sendEmailID= useremail
            salt = secrets.token_hex(8) + useremail
            token = hashlib.sha256(salt.encode('utf-8')).hexdigest()
            user_id = User.objects.get(username=useremail)
            time_now = timezone.now()
            token_updated, token_created = UserUniqueToken.objects.update_or_create(user_id=user_id, defaults={"token": token,'datetime':time_now})
            # data = UserUniqueToken(user_id=user_id,token=token)
            # data.save()
            sendEmail(sendEmailID,baseURL,token,"FORGOTPASSWORD")
            return redirect("verify_email")

        else:
            page = "FORGOT_PASSWORD"
            print("Chwcking")
            return render(request,'crunch/without_login/auth_forgot_password.html',{'fail':'Invalid Email Address','page':page,'useremail':useremail})

def verify_user_to_reset_password(request,token,email):
    if request.method == 'GET':
        email_token = token.split("token=")[1]
        user_token = get_object_or_404(UserUniqueToken, token=email_token)  # get object or throw 404
        print(user_token.user_id.email,email,email_token)
        email = email.split("email=")[1]
        if not user_token.user_id.email == email:
            return redirect("auth_sigin")
        time_now = timezone.now()
        if user_token.datetime < (time_now - timedelta(hours=2)):
            return redirect("auth_sigin")
        page = "CHANGE_PASSWORD"
        return redirect("auth_change_password",email_token)

def auth_change_password(request,validate):
    # if 'mail_user' in request.session:
    if request.method == 'GET':
        user_token = get_object_or_404(UserUniqueToken, token=validate)  # get object or throw 404
        page = "CHANGE_PASSWORD"
        # print(request.session['mail_user'])
        return render(request,'crunch/without_login/forgot_password.html',{'page':page,'token':validate})

    if request.method == 'POST':
        newPassword = request.POST['newPassword']
        confnewPassword = request.POST['confnewPassword']
        tokenKey = request.POST['tokenKey']

        if newPassword == confnewPassword:
            data = UserUniqueToken.objects.get(token=tokenKey)
            checkEmail = User.objects.get(username=data.user_id.email)
            print(checkEmail)
            checkEmail.set_password(newPassword)
            checkEmail.save()
            data.delete()
            request.session['login_msg'] = 'Your Account Password has been Changed successfully'
            return redirect("sigin")
        else:
            page = "CHANGE_PASSWORD"
            msg = "Confirm Password Not Match"
            return render(request,'crunch/without_login/forgot_password.html',{'page':page,'msg':msg})
    # else:
    #     return redirect("auth_sigin")









def verify_email(request):
    return render(request,'crunch/without_login//verifyemail.html')

def verify_account(request,token,email):
    if request.method == 'GET':
        email_token = token.split("token=")[1]
        user_token = get_object_or_404(UserUniqueToken, token=email_token)
        email = email.split("email=")[1]
        if not user_token.user_id.email == email:
            return redirect("auth_sigin")
        time_now = timezone.now()
        if user_token.datetime < (time_now - timedelta(hours=2)):
            return redirect("auth_sigin")
        page = "CHANGE_PASSWORD"
        dataEmailVeriFY = User.objects.get(username=email)
        dataEmailVeriFY.last_name = "TRUE"
        dataEmailVeriFY.save()
        request.session['login_msg'] = 'Your Account has been verified successfully'
        return redirect("sigin")

def verify_email(request):
    page = "SEND_EMAIL_CONFIRMATION"
    return render(request,'crunch/without_login//verifyemail.html')








# ###############################################################################
# ###############################################################################
# ###############################################################################

# # With Login Screen

def search(request):
    if request.user.is_authenticated and not request.user.is_superuser:
        userID = userProfile.objects.filter(userFK=request.user.id).order_by('-create_at').first()
        if(userID.payment_status and userID.subscribed):
            return render(request,'crunch/with_login/Search.html',{"username":str(request.user.first_name.split(" ")[0])})
        else:
            return redirect("payment")
    else:
        return redirect("home")

def user_profile(request):
    if request.user.is_authenticated and not request.user.is_superuser:
        if request.method == 'GET':
            userID = userProfile.objects.filter(userFK=request.user.id).order_by('-create_at').first()
            # if(userID.payment_status and userID.subscribed):
            userData = User.objects.get(id=request.user.id)
            paymentHistory = userProfile.objects.filter(userFK=request.user.id).exclude(subscription_start=None)
            return render(request,'crunch/with_login/User_profile.html',{'last_payment':userID,'paymentHistory':paymentHistory,'userData':userData,"username":str(request.user.first_name.split(" ")[0])})
            # else:
            #     return redirect('home')
        if request.method == 'POST':
            userName = request.POST['userName']
            # userEmail = request.POST['userEmail']
            userData = User.objects.get(id=request.user.id)
            userData.first_name = userName
            # userData.email = userEmail
            userData.save()
            paymentHistory = userProfile.objects.filter(userFK=request.user.id)
            return render(request,'crunch/with_login/User_profile.html',{'paymentHistory':paymentHistory,'userData':userData,"username":str(request.user.first_name.split(" ")[0])})
    else:
        return redirect('home')




def payment(request):
    if request.user.is_authenticated and not request.user.is_superuser:
        if request.method == 'GET':
            userID = userProfile.objects.filter(userFK=request.user.id).order_by('-create_at').first()
            if(userID.payment_status and userID.subscribed):
                return redirect('search')
            else:
                return render(request,'crunch/with_login/price_screen.html',{"username":str(request.user.first_name.split(" ")[0])})
    else:
        return redirect("home")

def search_results(request):
    if request.user.is_authenticated and not request.user.is_superuser:
        if request.method == 'GET':
            searcString = request.GET['searchText']
            checked_value = request.GET['checked_value']
            sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id="9c2297d43caa4bd59cd9a1845f1977e7",
                                                            client_secret="d39757a0f70f4058adb2ddd8ee2a4f12"))
            offsetNO = [i for i in range(0,10000,50)]
            # , searcString + ' a',searcString +  ' b' +  ' c',searcString +  ' d',searcString +  ' e',searcString +  ' f',searcString +  ' g',searcString +  ' h',searcString +  ' i',searcString +  ' j',searcString +  ' k'
            # additional_words = [searcString + ' a',searcString +  ' b' +  ' c',searcString +  ' d',searcString +  ' m',searcString +  ' s',searcString +  ' r']
            additional_words = [searcString,searcString + ' a']
            all_result = []
            for i_search in additional_words:
                dataCollectList = serachPlayList(request,offsetNO,i_search,sp,checked_value)
                all_result  = all_result + dataCollectList

            df = pd.DataFrame(all_result)
            dt_India = dt.datetime.utcnow() + dt.timedelta(hours=5, minutes=30)
            Indian_year = dt_India.year
            Indian_date = dt_India.day
            Indian_month = dt_India.month
            print("NNNN==>>>")
            try:
                file_path = '/home/ubuntu/django/spotifyproject/seachDataFrame/' + searcString + '_' + str(Indian_date) + '_' + str(Indian_month) + '_' + str(Indian_year)
                feather.write_feather(df, file_path)
                print("%$^$^&$^&^^&$^$")
            except:
                file_path = 'seachDataFrame/' + searcString + '_' + str(Indian_date) + '_' + str(Indian_month) + '_' + str(Indian_year)
                feather.write_feather(df, file_path)
                print("!@!@@#@###")
            print("###########")
            if len(all_result) != 0:
                len_data = len(all_result)
                return JsonResponse({'data':all_result,'len_data':len_data,'status_code':"RESULT"})
            if len(all_result) == 0:
                return JsonResponse({'data':[],'len_data':0,'status_code':"NO_DATA"})
    else:
        return redirect("home")


# @login_required(login_url='/auth_sigin')
def logout_home(request):
    if request.user.is_authenticated and not request.user.is_superuser:
        logout(request)
        return redirect("home")
    else:
        return redirect("home")


def resetpassword(request):
    if request.user.is_authenticated and not request.user.is_superuser:
        if request.method == 'GET':
            return render(request,'crunch/with_login/resetpassword.html',{"username":str(request.user.first_name.split(" ")[0])})
        if request.method == 'POST':
            crPass = request.POST['currentPassword']
            newPass = request.POST['newPassword']
            confPass = request.POST['confNewPassword']
            userAuth = authenticate(username=request.user.username, password=crPass)
            if(userAuth is  None):
                fail = "Current Password is not correct"
                return render(request,'crunch/with_login/resetpassword.html',{"username":str(request.user.first_name.split(" ")[0]),'fail':fail})

            if newPass != confPass:
                fail = "New Password and Confirm Password Should be same .."
                return render(request,'crunch/with_login/resetpassword.html',{"username":str(request.user.first_name.split(" ")[0]),'fail':fail})

            if newPass == crPass:
                fail = "New Password and Old Password should not be same"
                return render(request,'crunch/with_login/resetpassword.html',{"username":str(request.user.first_name.split(" ")[0]),'fail':fail})

            if(userAuth is not  None):
                userAuth.set_password(newPass)
                userAuth.save()
                return redirect('search')
    else:
        return redirect('home')


def thankyou_page(request):
    if request.user.is_authenticated and not request.user.is_superuser:
        try:
            refrenceNO = request.GET['refno']
            # Merchant_Code = "252114441478"
            # Secret_Code = "]yOsv|^Z6SFH(~bITM!l"
            Merchant_Code = "251211912911"
            Secret_Code = "l^P(MOT#U8yV%IJTn)eF"

            HEADER_DATA = get_headers(Merchant_Code,Secret_Code)
            METHOD = "GET"
            PARAMS = get_params()
            ENDPOINT = "orders/" + refrenceNO
            response = cal_api(ENDPOINT, PARAMS, METHOD,HEADER_DATA)
            response = json.loads(response)
            if response["Status"] == "COMPLETE":
                data = userProfile(
                    userFK=User.objects.get(id=request.user.id),
                    subscribed =True,
                    subscription_refrence= response['Items'][0]['ProductDetails']['Subscriptions'][0]['SubscriptionReference'],
                    currency=response['PaymentDetails']['Currency'],
                    recurring_billing=response['PaymentDetails']['PaymentMethod']['RecurringEnabled'],
                    price=response["NetPrice"],
                    subscription_type ='Full Playlist Access',
                    subscription_start = response['Items'][0]['ProductDetails']['Subscriptions'][0]['SubscriptionStartDate'],
                    subscription_expiry =response['Items'][0]['ProductDetails']['Subscriptions'][0]['ExpirationDate'],
                    payment_status = True,
                    paymentDate =response['OrderDate'],
                    order_ID =response['RefNo'],
                )
                data.save()
            return render(request,'crunch/with_login/thankyou.html',{"username":str(request.user.first_name.split(" ")[0])})
        except:
            return redirect('sigin')
    else:
        return redirect("home")



def cancel_subscription(request, ref):
    if request.user.is_authenticated and not request.user.is_superuser:
        refrenceNO = ref.strip()
        # Merchant_Code_pre = "252114441478"
        # Secret_Code_pre = "]yOsv|^Z6SFH(~bITM!l"
        Merchant_Code = "251211912911"
        Secret_Code = "l^P(MOT#U8yV%IJTn)eF"
        HEADER_DATA = get_headers(Merchant_Code,Secret_Code)
        METHOD = "DELETE"
        PARAMS = get_params()
        ENDPOINT = "subscription/" + refrenceNO + "/renewal/"
        response = cal_api(ENDPOINT, PARAMS, METHOD,HEADER_DATA)

        response = json.loads(response)
        print("BKJ",response)
        # data = userProfile.objects.get(order_ID=refrenceNO)
        # data.recurring_billing = False
        # data.save()
        return redirect('user_profile')
    else:
        return redirect('home')


# ###################################################################################
#####################################################################################
#####################################################################################

# Admin Theme Settings
# #######################


def admin_home(request):
    if request.user.is_authenticated and request.user.is_superuser:
        page = "ADMIN_TEMPLATE"
        users = User.objects.filter(is_superuser=False)
        return render(request,'admin_template/admin.html',{'fail':'Invalid User','page':page,'user_data':users})
    else:
        return redirect("home")



def admin_edit_user(request,id):
    if request.user.is_authenticated and request.user.is_superuser:
        if request.method == 'GET':
            req_id = id
            users = User.objects.get(id=id)
            print(users)
            page = 'EDIT_PROFILE'
            return render(request,'admin_template/edit_profile.html',{'fail':'Invalid User','page':page,'user_data':users})
        if request.method == 'POST':
            req_id = id
            users = User.objects.get(id=id)
            users.first_name = request.POST['fullName']
            users.last_name = request.POST['shortName']
            users.save()
            page = 'EDIT_PROFILE'
            return render(request,'admin_template/edit_profile.html',{'fail':'Invalid User','page':page,'user_data':users})
    else:
        return redirect("home")





def admin_view_user(request,id):
    if request.user.is_authenticated and request.user.is_superuser:
        page = "ADMIN_TEMPLATE"
        userID = userProfile.objects.filter(userFK=id)
        return render(request,'admin_template/detail_view.html',{'fail':'Invalid User','page':page,'user_data':userID})
    else:
        return redirect("home")


def admin_cms(request):
    if request.user.is_authenticated and request.user.is_superuser:
        if request.method == 'GET':
            banner = AdminBannerTemplate.objects.all()
            return render(request,'admin_template/cms.html',{'banner':banner})
    else:
        return redirect("home")



def admin_edit_banner(request,id):
    if request.user.is_authenticated and request.user.is_superuser:
        if request.method == 'GET':
            bannerData = AdminBannerTemplate.objects.all()
            return render(request,'admin_template/admin_edit_banner.html',{'bannerData':bannerData})
        if request.method == 'POST':
            bannerHeadLine = request.POST['bannerHeadLine']
            bannerText = request.POST['bannerText']
            bannerSubText = request.POST['bannerSubText']

            dataID = User.objects.get(id=request.user.id)
            data = AdminBannerTemplate.objects.get(id=id)
            data.bannerHeadText=bannerHeadLine
            try:
                 bannerImage = request.FILES['bannerImage']
                 data.document=bannerImage
            except:
                pass

            data.bannerText=bannerText
            data.save()
            return redirect('admin-cms')
    else:
        return redirect("home")


def admin_delete_user(request,id):
    if request.user.is_authenticated and request.user.is_superuser:
        page = "ADMIN_TEMPLATE"
        req_id = id
        users = User.objects.get(id=id)
        users.delete()
        return redirect("admin_home")
    else:
        return redirect("home")



@login_required(login_url='/auth_sigin')
def people_comments(request):
    if request.user.is_authenticated and request.user.is_superuser:
        if request.method == 'GET':
            people = AdminPeopleCommentedTemplate.objects.all()
            return render(request,'admin_template/people-commented.html',{'people':people})
    else:
        return redirect("home")

@login_required(login_url='/auth_sigin')
def add_people_comments(request):
    if request.user.is_authenticated and request.user.is_superuser:
        if request.method == 'GET':
            return render(request,'admin_template/add_people_commented.html')
        if request.method == 'POST':
            name = request.POST['name']
            title = request.POST['title']
            about = request.POST['about']
            imagesrc = request.FILES['imagesrc']
            dataID = User.objects.get(id=request.user.id)
            data = AdminPeopleCommentedTemplate(user_id=dataID,
            name=name,document=imagesrc,text=title,about=about)
            data.save()
            return redirect("people-comments")
    else:
        return redirect("home")


def admin_people_edit(request,id):
    if request.user.is_authenticated and request.user.is_superuser:
        if request.method == 'GET':
            data = AdminPeopleCommentedTemplate.objects.get(id=id)
            return render(request,'admin_template/admin_people_edit.html',{'data':data})
        if request.method == 'POST':
            print("KKHKHKJ")
            name = request.POST['name']
            title = request.POST['title']
            about = request.POST['about']

            data = AdminPeopleCommentedTemplate.objects.get(id=id)
            data.name=name
            data.text=title
            try:
                 imagesrc = request.FILES['imagesrc']
                 data.document=imagesrc
            except:
                pass

            data.about=about
            data.save()
            return redirect("people-comments")
    else:
        return redirect("home")

def admin_people_delete(request,id):
    if request.user.is_authenticated and request.user.is_superuser:
        req_id = id
        users = AdminPeopleCommentedTemplate.objects.get(id=id)
        users.delete()
        return redirect("people-comments")
    else:
        return redirect('home')


def payment(request):
    amount = prices.objects.all()
    context = {'amount':amount}
    return render(request ,'crunch/with_login/price_screen.html', context)

def payment2(request):
    amt = prices.objects.all()
    context = {'amt':amt}
    return render(request ,'crunch/without_login/index.html', context)



def checkout_page(request):
    return render(request,'crunch/with_login/checkout.html')








