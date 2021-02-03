from django.contrib.auth.models import User
from django.shortcuts import render
from django.views.decorators.csrf import csrf_protect
import openpyxl
from excel_response import ExcelResponse
from .forms import UploadFileForm
from main_app.models import Entry, Specialty
from schools.models import School
from users.models import Profile
from django.contrib import messages
from history.models import HistoryEntry


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
            except:
                messages.warning(request, "Κάτι πήγε λάθος...")
                print("Something went wrong!")

        return render(request, 'excels/upload_specialties.html', {'form': form, 'excel_data': excel_data})
    else:
        if request.user.is_superuser:
            form = UploadFileForm()

            return render(request, 'excels/upload_specialties.html', {'form': form})
        else:
            return render(request, 'main_app/error.html')


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
                print("Something went wrong!")

        return render(request, 'excels/add_specialties.html', {'form': form, 'excel_data': excel_data})
    else:
        if request.user.is_superuser:
            form = UploadFileForm()

            return render(request, 'excels/add_specialties.html', {'form': form})
        else:
            return render(request, 'main_app/error.html')


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
                print("Something went wrong!")

        return render(request, 'excels/upload_schools.html', {'form': form, 'excel_data': excel_data})
    else:
        if request.user.is_superuser:
            form = UploadFileForm()

            return render(request, 'excels/upload_schools.html', {'form': form})
        else:
            return render(request, 'main_app/error.html')


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
                print("Something went wrong!")

        return render(request, 'excels/add_schools.html', {'form': form, 'excel_data': excel_data})
    else:
        if request.user.is_superuser:
            form = UploadFileForm()

            return render(request, 'excels/add_schools.html', {'form': form})
        else:
            return render(request, 'main_app/error.html')


def excel_entries(request):
    if request.user.is_superuser:
        entries = Entry.objects.all().order_by('specialty')

        data = list()
        header = ['Ειδικότητα', 'Ώρες', 'Είδος', 'Προτεραιότητα', 'Παρατηρήσεις', 'Χρονική σήμανση', 'Σχολείο']
        data.append(header)
        for entry in entries:
            row = [entry.specialty.code, entry.hours, entry.type, entry.priority, entry.description, entry.date_time,
                   entry.owner.last_name]
            data.append(row)

        return ExcelResponse(data, 'entries')
    else:
        return render(request, 'main_app/error.html', {})


def excel_history(request):
    if request.user.is_superuser:
        entries = HistoryEntry.objects.all().order_by('owner', 'specialty')

        data = list()
        header = ['Σχολείο', 'Ειδικότητα', 'Ώρες', 'Είδος', 'Προτεραιότητα', 'Παρατηρήσεις', 'Χρονική σήμανση']
        data.append(header)
        for entry in entries:
            row = [entry.owner.last_name, entry.specialty.code, entry.hours, entry.type, entry.priority,
                   entry.description, entry.date_time]
            data.append(row)

        return ExcelResponse(data, 'history')
    else:
        return render(request, 'main_app/error.html', {})


def excel_user_history(request):
    entries = HistoryEntry.objects.filter(owner=request.user)

    data = list()
    header = ['Σχολείο', 'Ειδικότητα', 'Ώρες', 'Είδος', 'Προτεραιότητα', 'Παρατηρήσεις', 'Χρονική σήμανση']
    data.append(header)
    for entry in entries:
        row = [entry.owner.last_name, entry.specialty.code, entry.hours, entry.type, entry.priority,
               entry.description, entry.date_time]
        data.append(row)

    return ExcelResponse(data, 'user_history')


def reconnect_users_to_schools():
    profiles = Profile.objects.all()

    for profile in profiles:
            school = School.objects.filter(email=profile.user.email).first()

            if school != None:
                profile.user.last_name = school.name
                profile.user.save()
                profile.verified = True
                profile.save()
                school.connected_to_user = True
                school.save()


def reconnect_nv_users_to_schools():
    profiles = Profile.objects.filter(verified=False)

    for profile in profiles:
            school = School.objects.filter(email=profile.user.email).first()

            if school != None:
                profile.user.last_name = school.name
                profile.user.save()
                profile.verified = True
                profile.save()
                school.connected_to_user = True
                school.save()