import datetime
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.contrib.auth.models import User, Group
import booking.models as booking_models
import trainer.models 
import trainer.utils
from dateutil import parser
from trainer.forms import   ServiceForm, TrainerScheduleForm,CategoryForm,WeeklyWorkScheduleForm,TrainerForm
from trainer.models import TraineSchedule,TraineDescription,Category,Service
import users.forms as user_forms
def trainer_page(request):
    if request.method == "GET":
        # Controlla se l'utente è un trainer
        if Group.objects.filter(name="Trainer", user=request.user).exists():
            trainer_model = User.objects.get(pk=request.user.pk)
            trainer_data = TraineDescription.objects.filter(trainer=trainer_model).first()
            trainer_schedule = TraineSchedule.objects.filter(trainer=trainer_model)
            context = {
                "trainer_data": trainer_data,
                "trainer_schedule": trainer_schedule,
                "trainer_model": trainer_model
            }
            return render(request, "trainer.html", context)
        else:
            
            trainers = User.objects.filter(groups__name="Trainer")
            all_trainers = []
            for trainer in trainers:
                
                trainer_data = TraineDescription.objects.filter(trainer=trainer).first()
                trainer_schedule = TraineSchedule.objects.filter(trainer=trainer)
                all_trainers.append({
                    "trainer_data": trainer_data,
                    "trainer_schedule": trainer_schedule,
                    "trainer_model": trainer
                })
            
            context = {"all_trainers": all_trainers}
            return render(request, "all_trainers.html", context)


# Categoria Trainer
def category_page(request):
    if request.method == "GET":
        form = CategoryForm()
        
        return render(request, "category.html", {"form": form})
    elif request.method == "POST":
        form = CategoryForm(request.POST)
        if form.is_valid():
            # Logica per salvare la categoria (se necessario)
            return HttpResponse("Category created successfully")
        else:
            return render(request, "category.html", {"form": form})
        
def trainer_details(request, trainer_id):
    trainer = User.objects.get(pk=trainer_id)
    trainer_data = TraineDescription.objects.filter(trainer=trainer).first()
    trainer_schedule = TraineSchedule.objects.filter(trainer=trainer)
    trainer_service = Service.objects.filter(trainer=trainer)
    category = Category.objects.filter(
        id__in=trainer_service.values_list('category_id', flat=True)
    )
    context = {
        "trainer_data": trainer_data,
        "trainer_schedule": trainer_schedule,
        "trainer_model": trainer,
        "trainer_service": trainer_service,
        "category": category
    }
    return render(request, "trainer_details.html", context)

def specific_trainer(request,):
    form1 = trainer()
    if request.method == "GET":
        if Group.objects.filter(name="Trainer", user=request.user).exists():
            trainer_model = User.objects.get(pk=request.user.pk)
            trainer_data = TraineDescription.objects.filter(trainer=trainer_model).first()
            trainer_schedule = form1
            trainer_form = TrainerForm()
            context = {"trainer_data": trainer_data, trainer_schedule : trainer_schedule, 'trainer_model': trainer_model}
            return render(request, "specific_trainer.html", context)

    if request.method == "POST":
        if Group.objects.filter(name="Trainer", user=request.user).exists():
            schedule_form = WeeklyWorkScheduleForm(request.POST)
            if schedule_form.is_valid():
                start_time = schedule_form.cleaned_data['start_time']
                end_time = schedule_form.cleaned_data['end_time']
                days = schedule_form.cleaned_data['days']
                trainer = request.user
                
                next_week_start = datetime.datetime.now() + datetime.timedelta(days=(7 - datetime.datetime.now().weekday()))
                next_week_end = next_week_start + datetime.timedelta(days=6)
                TraineSchedule.objects.filter(
                    trainer=trainer, 
                    datatime_start__date__range=[next_week_start, next_week_end]
                ).delete()

                # Crea i nuovi orari
                for day in days:
                    day_index = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'].index(day)
                    day_date = next_week_start + datetime.timedelta(days=day_index)
                    datatime_start = datetime.datetime.combine(day_date, start_time)
                    datatime_end = datetime.datetime.combine(day_date, end_time)
                    TraineSchedule.objects.create(
                        trainer=trainer,
                        datatime_start=datatime_start,
                        datatime_end=datatime_end
                    )
                return redirect("specific_trainer")  # Torna alla pagina del trainer

    return render(request, "specific_trainer.html", {
        "trainer_form": trainer_form,
        "schedule_form": schedule_form,
        "trainer_schedule": trainer_schedule,
})

# Servizi del Trainer
def trainer_service(request):
    if request.method == "GET":
        if request.user.groups.filter(name="Trainer").exists():
            return render(request, "trainer_service.html")
        else:
            form = ServiceForm()
            return render(request, "trainer_service_form.html", {"form": form})
    elif request.method == "POST":
        form = ServiceForm(request.POST)
        if form.is_valid():
            service = form.save(commit=False)
            service.trainer = request.user
            service.save()
            return redirect("trainer_page",{"form": form})
        else:
            return render(request, "")

# Pagina Servizio Trainer
def trainer_service_page(request, trainer_id, service_id):
    current_trainer = User.objects.get(pk=trainer_id)
    specific_service = trainer.models.Service.objects.get(pk=service_id)
    if request.method == "GET":
        available_times = []
        days_from_now = 1
        today = datetime.datetime.now()
        while days_from_now <= 7:
            cur_date = datetime.datetime(today.year, today.month, today.day) + datetime.timedelta(days=days_from_now)
            training_bookings = booking_models.Booking.objects.filter(trainer=current_trainer,datetime_start__date=cur_date.date()).all()
            bookings_list = [itm for itm in training_bookings]
            trainer_schedule = trainer.models.TraineSchedule.objects.filter(trainer=current_trainer,datatime_start__date=cur_date.date())
            service_durations = {specific_service.id: specific_service.duration}  # Passa la durata del servizio
            available_times += trainer.utils.bookings_times_discovery(trainer_schedule, bookings_list, cur_date, service_durations)
            days_from_now += 1
            print(bookings_list)
        return render(request,"trainer_service_page.html", {"specific_service": specific_service, "available_times": available_times})
    elif request.method == "POST":
        booking_start = parser.parse(request.POST.get("training-start"))
        current_user = User.objects.get(pk=request.user.pk)
        booking_models.Booking.objects.create(
            trainer=current_trainer,
            service=specific_service,
            datetime_start=booking_start,
            user=current_user,
            datetime_end=booking_start + datetime.timedelta(minutes=specific_service.duration)
        )
        return redirect("trainer_service_page", trainer_id=trainer_id, service_id=service_id)

# Registrazione Trainer
def trainer_registratione(request):
    if request.method == "GET": 
        form = user_forms.registerForm()
        return render(request, "trainer_registration.html", context={"form": form})
    elif request.method == "POST":
        form = user_forms.registerForm(request.POST)
        if form.is_valid():
            create_trainer = form.save()
            add_trainer_group = Group.objects.get(name="Trainer")
            create_trainer.groups.add(add_trainer_group)
            create_trainer.save()
            return redirect("login_page")
