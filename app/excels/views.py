import logging
import openpyxl

from django.contrib.auth.models import User
from django.shortcuts import render
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth.decorators import user_passes_test, login_required
from excel_response import ExcelResponse
from .forms import UploadFileForm
from shared import check_user_is_superuser
from main_app.models import Entry, Specialty, EntryVariantType
from schools.models import School
from users.models import Profile
from django.contrib import messages
from history.models import HistoryEntry

# Get an instance of a logger
logger = logging.getLogger(__name__)


@login_required
@user_passes_test(check_user_is_superuser)
@csrf_protect
def upload_specialties(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                excel_file = request.FILES["file"]

                workbook = openpyxl.load_workbook(excel_file)
                worksheet = workbook.active
                excel_data = list()
                for row in worksheet.iter_rows():
                    row_data = list()
                    for cell in row:
                        if cell.value is None:
                            text = ""
                        else:
                            text = str(cell.value).strip()

                        row_data.append(text)
                    excel_data.append(row_data)

                Specialty.objects.all().delete()

                for row in excel_data[1:]:
                    Specialty.objects.create(code=row[0], lectic=row[1])
            except Exception as e:
                messages.warning(request, "Κάτι πήγε λάθος...")
                logger.exception("Something went wrong!")

        return render(request, 'excels/upload_specialties.html', {'form': form, 'excel_data': excel_data})
    else:
        form = UploadFileForm()
        return render(request, 'excels/upload_specialties.html', {'form': form})


@login_required
@user_passes_test(check_user_is_superuser)
@csrf_protect
def add_specialties(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                excel_file = request.FILES["file"]

                workbook = openpyxl.load_workbook(excel_file)
                worksheet = workbook.active
                excel_data = list()
                for row in worksheet.iter_rows():
                    row_data = list()
                    for cell in row:
                        if cell.value is None:
                            text = ""
                        else:
                            text = str(cell.value).strip()

                        row_data.append(text)
                    excel_data.append(row_data)

                for row in excel_data[1:]:
                    Specialty.objects.create(code=row[0], lectic=row[1])
            except:
                messages.warning(request,
                                 "Κάτι πήγε λάθος... Μάλλον οι εγγραφές που μόλις φόρτωσες υπήρχαν ήδη στον πίνακα.")
                logger.exception("Something went wrong!")

        return render(request, 'excels/add_specialties.html', {'form': form, 'excel_data': excel_data})
    else:
        form = UploadFileForm()
        return render(request, 'excels/add_specialties.html', {'form': form})


@login_required
@user_passes_test(check_user_is_superuser)
@csrf_protect
def upload_schools(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                excel_file = request.FILES["file"]

                workbook = openpyxl.load_workbook(excel_file)
                worksheet = workbook.active
                excel_data = list()
                for row in worksheet.iter_rows():
                    row_data = list()
                    for cell in row:
                        if cell.value is None:
                            text = ""
                        else:
                            text = str(cell.value).strip()

                        row_data.append(text)
                    excel_data.append(row_data)

                School.objects.all().delete()
                Profile.objects.all().update(verified=False)
                User.objects.all().update(last_name='')

                for row in excel_data[1:]:
                    School.objects.create(name=row[0], email=row[1], principal=row[2], phone=row[3], address=row[4])

                reconnect_users_to_schools()
            except:
                messages.warning(request, "Κάτι πήγε λάθος...")
                logger.exception("Something went wrong!")

        return render(request, 'excels/upload_schools.html', {'form': form, 'excel_data': excel_data})
    else:
        form = UploadFileForm()
        return render(request, 'excels/upload_schools.html', {'form': form})


@login_required
@user_passes_test(check_user_is_superuser)
@csrf_protect
def add_schools(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                excel_file = request.FILES["file"]

                workbook = openpyxl.load_workbook(excel_file)
                worksheet = workbook.active
                excel_data = list()
                for row in worksheet.iter_rows():
                    row_data = list()
                    for cell in row:
                        if cell.value is None:
                            text = ""
                        else:
                            text = str(cell.value).strip()

                        row_data.append(text)
                    excel_data.append(row_data)

                for row in excel_data[1:]:
                    School.objects.create(name=row[0], email=row[1], principal=row[2], phone=row[3], address=row[4])

                reconnect_nv_users_to_schools()
            except:
                messages.warning(request,
                                 "Κάτι πήγε λάθος... Μάλλον οι εγγραφές που μόλις φόρτωσες υπήρχαν ήδη στον πίνακα.")
                logger.exception("Something went wrong!")

        return render(request, 'excels/add_schools.html', {'form': form, 'excel_data': excel_data})
    else:
        form = UploadFileForm()
        return render(request, 'excels/add_schools.html', {'form': form})


@login_required
@user_passes_test(check_user_is_superuser)
def excel_entries(request):

    entries = Entry.objects.all().order_by('specialty')

    data = list()
    header = [
        'Σχολείο', 'Ειδικότητα', 'Είδος', 'Τύπος', 'Ώρες',
        'Παρατηρήσεις', 'Χρονική σήμανση'
    ]
    data.append(header)
    for entry in entries:
        row = [
            entry.owner.last_name, entry.specialty.code, entry.type,
            str(EntryVariantType(entry.variant).label), entry.hours,
            entry.description, entry.date_time,
        ]
        data.append(row)

    return ExcelResponse(data, 'entries')


@login_required
@user_passes_test(check_user_is_superuser)
def excel_history(request):

    entries = HistoryEntry.objects.all().order_by('owner', 'specialty')

    data = list()
    header = [
        'Σχολείο', 'Ειδικότητα', 'Είδος', 'Τύπος', 'Ώρες',
        'Παρατηρήσεις', 'Χρονική σήμανση'
    ]
    data.append(header)
    for entry in entries:
        row = [
            entry.owner.last_name, entry.specialty.code, entry.type,
            str(EntryVariantType(entry.variant).label), entry.hours,
            entry.description, entry.date_time
        ]
        data.append(row)

    return ExcelResponse(data, 'history')


@login_required
@user_passes_test(check_user_is_superuser)
def excel_user_history(request):
    entries = HistoryEntry.objects.filter(owner=request.user)

    data = list()
    header = ['Σχολείο', 'Ειδικότητα', 'Ώρες', 'Είδος', 'Παρατηρήσεις', 'Χρονική σήμανση']
    data.append(header)
    for entry in entries:
        row = [entry.owner.last_name, entry.specialty.code, entry.hours, entry.type,
               entry.description, entry.date_time]
        data.append(row)

    return ExcelResponse(data, 'user_history')


def reconnect_users_to_schools(user=None):
    # type: (User) -> List[Profile]
    if user is None:
        # we are working for all users
        profiles = Profile.objects.all()  # type: list[Profile]
    else:
        profiles = [user.profile, ]  # type: list[Profile]

    # store the associated (actually processed) users/profile in a list
    associated_users = list()

    for profile in profiles:
        try:
            school = School.objects.get(email=profile.user.email)  # type: School

            profile.user.last_name = school.name
            profile.user.save()

            profile.verified = True
            profile.school = school
            profile.save()

            associated_users.append(profile)
        except School.DoesNotExist:
            pass

    return associated_users


def reconnect_nv_users_to_schools():
    profiles = Profile.objects.filter(verified=False)  # type: list[Profile]

    for profile in profiles:
        try:
            school = School.objects.get(email=profile.user.email)  # type: School

            profile.user.last_name = school.name
            profile.user.save()

            profile.verified = True
            profile.save()
        except School.DoesNotExist:
            pass
