from django.shortcuts import render, redirect
from django.contrib import messages
from datetime import date
import datetime
from django.core.mail import send_mail
from django.conf import settings

from .models import *
import random
import string


def get_random_string(length):
    # choose from all lowercase letter
    letters = string.ascii_lowercase
    result_str = "".join(random.choice(letters) for i in range(length))
    return result_str


def home(request):
    return render(request, "index.html")


def BuyTicket(request):
    agencies = Agency.objects.all()

    if request.method == "POST":
        agency = request.POST.get("agency")
        agency_profile = Agency.objects.get(name=agency)
        request.session["agency"] = agency_profile.id
        return redirect(f"/buy/step2")

    context = {
        "agencies": agencies,
    }
    return render(request, "buyticket.html", context)


def BuyTicketStepTwo(request):
    try:
        if request.session["agency"] is not None:
            pass
    except:
        return redirect("/buy")

    agency = request.session["agency"]
    agency_profile = Agency.objects.get(id=agency)
    destinations = Destination.objects.filter(agency=agency)

    if request.method == "POST":
        destination = request.POST.get("destination")
        depart_time = request.POST.get("time")
        From = destination.split("-")[0]
        To = destination.split("-")[1]

        now = datetime.datetime.now()
        current_time = now.strftime("%H:%M")

        if current_time > depart_time:
            messages.error(request, "Impossible to get that ticket on this time")
            return redirect(f"/buy/step2")
        else:
            destination_object = Destination.objects.get(
                agency=agency_profile, From=From, To=To
            )
            transaction_object = Transaction.objects.filter(
                departure_time=depart_time, destination=destination_object
            ).count()

            print(destination_object.price)

            if transaction_object > 20:
                messages.error(request, "Bus is full try another time!")
                return redirect(f"/buy/step2")
            else:
                request.session["destination"] = destination_object.id
                request.session["time"] = depart_time
                try:
                    if request.session["user"] is not None:
                        return redirect("/buy/step4")
                    else:
                        return redirect("/buy/step3")
                except:
                    return redirect("/buy/step3")

    context = {
        "destinations": destinations,
    }
    return render(request, "buyticket2.html", context)


def BuyTicketStep3(request):
    passcode = get_random_string(6)

    if request.method == "POST":
        fullname = request.POST.get("fullname")
        email = request.POST.get("email")
        phone = request.POST.get("phone")

        try:
            user_exist = UserProfile.objects.get(email=email)
            messages.error(
                request,
                "User with given email already exists! \nTry Logging in instead!",
            )
            return redirect("/buy/step3")
        except:
            new_user = UserProfile(
                fullname=fullname, email=email, phone=phone, passcode=passcode
            )
            try:
                new_user.save()
                request.session["user"] = email
                try:
                    send_mail(
                        subject="Message | Makutha-Transport",
                        message=f"Dear {email} thank you for creating an account at Makutha-Transports.\nYour Password is {passcode}.\n\nMakutha Transport Team,",
                        from_email=email,
                        recipient_list=[
                            settings.EMAIL_HOST_USER,
                            email,
                        ],
                        fail_silently=False,
                    )
                except:
                    messages.error(
                        request,
                        "A connection error occurred while sending message retry!.",
                    )
                    return redirect("/buy/step4")
                messages.success(request, "Account Created successfully!")
                return redirect("/buy/step4")
            except Exception as e:
                messages.error(request, e)
                return redirect("buy/step3")

    context = {"passcode": get_random_string(6)}
    return render(request, "buyticket3.html", context)


def BuyTicketStep4(request):
    context = {}
    try:
        if request.session["user"] is None:
            messages.error(request, "Session expired!")
            return redirect("/")
        else:
            destination_object = Destination.objects.get(
                id=request.session["destination"]
            )

            time = request.session["time"]
            user_profile = UserProfile.objects.get(email=request.session["user"])
            context = {
                "destination": destination_object,
                "user": user_profile,
                "time": time,
            }

    except Exception as e:
        messages.error(request, e)
        return redirect("/buy")

    if request.method == "POST":
        try:
            new_transaction = Transaction(
                user=user_profile,
                departure_time=time,
                destination=destination_object,
                date=date.today(),
            )

            new_transaction.save()
            request.session["agency"] = None
            request.session["destination"] = None

            try:
                send_mail(
                    subject="MAKUTHA-Transports",
                    message=f"Dear {user_profile.fullname},\nThank you for placing an order for buying  ticket {destination_object.From}-{destination_object.To}  with us!\n\nNow you have to pay an amount of {destination_object.price} Frw using MOMO PAY by dialing *182*8*1*638441! Then you will get your ticket in 2minutes of time!\n\nThanks for Travelling with us!\n\nMAKUTHA-Transport Team,",
                    from_email=settings.EMAIL_HOST_USER,
                    recipient_list=[
                        user_profile.email,
                        "nsengitech@gmail.com",
                        "makuthab@gmail.com",
                    ],
                    fail_silently=False,
                )
            except:
                messages.error(
                    request, "A connection error occurred while sending message retry!."
                )
                return redirect("/buy/step4")
            messages.success(request, "Transaction recorded, Now proceed to payments!")
            return redirect("/confirmation")

        except Exception as e:
            messages.error(request, e)
            return redirect("/buy/step4")

    return render(request, "buyticket4.html", context)


def Confirmation(request):
    context = {}
    try:
        if request.session["user"] is None:
            messages.error(request, "Session Expired!")
            return redirect("/login")
        else:
            try:
                user_object = UserProfile.objects.get(email=request.session["user"])

                last_transaction = Transaction.objects.filter(user=user_object).first()

                context = {
                    "last_transaction": last_transaction,
                }
                if request.method == "POST":
                    transaction_id = request.POST.get("transaction_id")
                    screenshot = request.POST.get("screenshot") or None

                    last_transaction.transaction_id = transaction_id
                    last_transaction.proof = screenshot
                    last_transaction.status = "Under Review"
                    last_transaction.save()
                    messages.success(
                        request,
                        "Information saved successfully!\nOur Team is reviewing your payment!",
                    )

                    return redirect("/profile")
            except Exception as e:
                messages.error(e)
                return redirect("/confirmation")
    except:
        messages.error(request, "session expired!")
        return redirect("/")
    return render(request, "confirmation.html", context)


def MyProfile(request):
    context = {}
    try:
        if request.session["user"] is None:
            messages.error(request, "Session Expired!")
            return redirect("/")
        user_profile = UserProfile.objects.get(email=request.session["user"])
        transactions = Transaction.objects.filter(user=user_profile)
        context = {
            "user": user_profile,
            "transactions": transactions,
        }
    except:
        messages.error(request, "Session Expired!")
        return redirect("/")

    return render(request, "myprofile.html", context)


def Login(request):
    if request.method == "POST":
        email = request.POST.get("email")
        passcode = request.POST.get("password")
        try:
            user = UserProfile.objects.get(email=email, passcode=passcode)
            print()
            if user is not None:
                request.session["user"] = email
                return redirect("/")
            else:
                messages.error(request, "User not found!")
        except Exception as e:
            messages.error(request, e)
            return redirect("/login")
    return render(request, "login.html")

def ForgotPassword(request):
    if request.method =='POST':
        email = request.POST.get('email')
        try:
            user_exist = UserProfile.objects.get(email=email)
            try:
                    send_mail(
                        subject="Message | Makutha-Transport",
                        message=f"Dear {email}\nYour Password is {user_exist.passcode}.\n\nMakutha Transport Team,",
                        from_email=email,
                        recipient_list=[
                            settings.EMAIL_HOST_USER,
                            user_exist.email,
                        ],
                        fail_silently=False,
                    )
                    messages.success(request, f"Check your passcode on your email {user_exist.email}!")
                    return redirect("/login")
            except:
                messages.error(
                        request,
                        "A connection error occurred while sending message retry!.",
                    )
                return redirect("/")
            
        except:
                messages.error(request,'User with given email was not found!')
                return redirect('/login')


def Logout(request):
    try:
        if request.session["user"] is None:
            return redirect("/login")
        else:
            request.session["user"] = None
            request.session["agency"] = None
            request.session["destination"] = None
            return redirect("/")
    except:
        return redirect("/login")
