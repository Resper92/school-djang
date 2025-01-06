import datetime
from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth.models import User, Group
import booking.models as booking_models
import trainer.models
import trainer.utils
from dateutil import parser




def trainer_page(request):
    if request.user.groups.filter(name=("Trainer")).exists():
        if request.method == "GET":
            service_categories = trainer.models.Category.objects.all()
            my_services = trainer.models.Service.objects.filter(trainer=request.user).all
            return render(request, "trainer.html", {"service_categories": service_categories, "my_services": my_services})
        return HttpResponse("Hello, world. You're at the users index.")
    else:
        trainer_model= User.objects.get(pk=request.user.pk)
        trainer_data=trainer.models.TraineDescription(trainer=trainer_model)
        trainer_schedule = trainer.models.TraineSchedule.objects.filter(trainer=trainer_model)
        return render(request, "account.html", {"trainer_data": trainer_data, "trainer_schedule": trainer_schedule})
        
def category_page(request):
    return HttpResponse("Hello, world. You're at the users index.")
def specific_trainer(request):
    return HttpResponse("Hello, world. You're at the users index.")
def trainer_service(request):
    if request.User.groups.filter(name=("Trainer")).exists():
        return render(request, "trainer_service.html")
    else:
        form_data = request="POST"
        service_cat=trainer.models.Category.objects.get(pk=form_data("category"))
        service=trainer.models.Service.objects.create(
            category=service_cat, 
            trainer=request.user,
            price=form_data("price"),
            level=form_data("level"),
            duration=form_data("duration"))
    return HttpResponse("Hello, world. You're at the users index.")

def trainer_service_page(request,trainer_id,service_id):
    current_trainer = User.objects.get(pk=trainer_id)
    service = trainer.models.Service.objects.get(pk=service_id)
    if request.method == "GET":
        availabel_times = []
        days_from_now = 1
        today = datetime.date.now()
        while days_from_now <=7:
            cur_date = datetime.datetime(today.year, today.month, today.day) + datetime.timedelta(days=days_from_now).all()
            training_bookings = booking_models.Booking.objects.filter(trainer=current_trainer, datetime_start__date=cur_date.day).all()
            bookings_list=[(itm.datetime_start, itm.datetime_end) for itm in training_bookings]
            trainer_schedule = trainer.models.TraineSchedule.objects.filter(trainer=current_trainer, date=cur_date)
            service_duration = trainer.models.Service.objects.get(pk=service_id).duration
            availeble_times += trainer.utils.bookiings_times_discovery(trainer_schedule, bookings_list,cur_date,service_duration)
            days_from_now += 1
            return render(request,trainer_service.html, context={'specific_service': specific_service, 'availabel_times': availabel_times}) 
    else:
        booking_start = parser.parse(request.POST.get("training-start"))
        new_booking = booking_models.Booking.objects.create(
            trainer=current_trainer,
            user=request.user,
            datetime_start=booking_start,
            datetime_end=booking_start + datetime.timedelta(minutes=specific_service),
            service=service
        )
        
def trainer_service_booking(request):
    return HttpResponse("Hello, world. You're at the users index.")

def trainer_registratione(request):
    if request.method == "GET":
        return render(request, "trainer_registration.html")
    else:
        username= request.POST.get("username")
        pasword= request.POST.get("password")
        email= request.POST.get("email")
        first_name= request.POST.get("first_name")
        last_name= request.POST.get("last_name")
        user = User.objects.create_user(username, pasword, email, first_name=first_name, last_name=last_name)
        user.set_password(pasword)
        trainer_group= Group.objects.get(name="Trainer")
        user.groups.add(trainer_group)
        print(pasword)
        user.save()
        return HttpResponse("Succesfaul")