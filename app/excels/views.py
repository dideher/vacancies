import logging
from openpyxl import Workbook, load_workbook
from openpyxl.writer.excel import save_virtual_workbook
from openpyxl.styles import NamedStyle, Font, Border, Side, Alignment
from openpyxl.worksheet.dimensions import ColumnDimension, DimensionHolder, RowDimension
from openpyxl.worksheet import Worksheet
from openpyxl.utils import get_column_letter
from sortedcontainers import SortedSet
from django.contrib.auth.models import User
from django.shortcuts import render
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth.decorators import user_passes_test, login_required
from django.contrib import messages
from django.db.models import QuerySet
from django.http import HttpResponse
from excel_response import ExcelResponse
from .forms import UploadFileForm
from shared import check_user_is_superuser
from main_app.models import Entry, Specialty, EntryVariantType
from schools.models import School
from users.models import Profile
from history.models import HistoryEntry

# Get an instance of a logger
logger = logging.getLogger(__name__)


class AggregatedEntriesReport:

    def __init__(self):

        self.entries: QuerySet[Entry] = Entry.objects.all().order_by("school__school_group__ordering", "school__id")

    def createSpecialtiesTypes(self):
        self.generalEducationSpcTypes = SortedSet()
        self.specialEducationSpcTypes = SortedSet()
        self.miscSpcTypes = SortedSet()

        for entry in self.entries:
            entry_variant = str(EntryVariantType(entry.variant).label)
            entry_specialization = entry.specialty.code
            if entry_variant == 'Γενικής Αγωγής - Πανελλαδικώς Εξεταζόμενα Μαθήματα':
                self.generalEducationSpcTypes.add(f'{entry_specialization} - Γενικής Αγωγής - Πανελλαδικώς Εξεταζόμενα Μαθήματα')
                self.generalEducationSpcTypes.add(
                    f'{entry_specialization} - Γενικής Αγωγής - μη Πανελλαδικώς Εξεταζόμενα Μαθήματα')
                self.generalEducationSpcTypes.add(f'{entry_specialization} - Γενικής Αγωγής (Σύνολο)')
            elif entry_variant == 'Γενικής Αγωγής - μη Πανελλαδικώς Εξεταζόμενα Μαθήματα':
                self.generalEducationSpcTypes.add(
                    f'{entry_specialization} - Γενικής Αγωγής - μη Πανελλαδικώς Εξεταζόμενα Μαθήματα')
            elif 'Ειδικής Αγωγής' in entry_variant:
                self.specialEducationSpcTypes.add(f'{entry_specialization} - {entry_variant}')
            else:
                self.miscSpcTypes.add(f'{entry_specialization} - {entry_variant}')

    def getSchools(self):
        self.generalEducationSchools = list()
        self.specialEducationSchools = list()
        self.miscSchools = list()

        for entry in self.entries:
            entry_variant = str(EntryVariantType(entry.variant).label)
            #school_name = entry.owner.last_name (charis version)
            school_name = entry.school.name
            if entry_variant in ['Γενικής Αγωγής - Πανελλαδικώς Εξεταζόμενα Μαθήματα',
                                 'Γενικής Αγωγής - μη Πανελλαδικώς Εξεταζόμενα Μαθήματα']:
                if school_name not in self.generalEducationSchools:
                    self.generalEducationSchools.append(school_name)
            elif 'Ειδικής Αγωγής' in entry_variant:
                if school_name not in self.specialEducationSchools:
                    self.specialEducationSchools.append(school_name)
            else:
                if school_name not in self.miscSchools:
                    self.miscSchools.append(school_name)

    def createTables(self):
        self.createGEStable()
        self.createSEStable()
        self.createMStable()

    def createMStable(self):
        self.msTable = list()
        header = list()
        header.append('Σχολείο')
        header += self.miscSpcTypes[:]
        header.append("Παρατηρήσεις")

        self.msTable.append(header)
        for sch in self.miscSchools:
            entry = list()
            entry.append(sch)
            sch_values = [0] * len(self.miscSpcTypes)
            school_entries_descriptions = list()

            for vacancy_entry in self.entries:
                entry_variant = str(EntryVariantType(vacancy_entry.variant).label)
                school_name = vacancy_entry.school.name
                entry_type = vacancy_entry.type
                entry_hours = vacancy_entry.hours
                entry_specialization = vacancy_entry.specialty.code
                entry_description: str = vacancy_entry.description

                if school_name != sch:
                    continue

                if entry_variant in ['Γενικής Αγωγής - Πανελλαδικώς Εξεταζόμενα Μαθήματα',
                                     'Γενικής Αγωγής - μη Πανελλαδικώς Εξεταζόμενα Μαθήματα'] \
                        or 'Ειδικής Αγωγής' in entry_variant:
                    continue

                spcType = f'{entry_specialization} - {entry_variant}'
                indexScpType = self.miscSpcTypes.index(spcType)
                if entry_description is not None and len(entry_description.strip()) > 0:
                    school_entries_descriptions.append(f'{entry_specialization} - {entry_description}')

                if entry_type == 'Κενό':
                    sch_values[indexScpType] -= int(entry_hours)
                else:
                    sch_values[indexScpType] += int(entry_hours)

            entry += sch_values
            entry.append("\n".join(school_entries_descriptions))

            self.msTable.append(entry)

    def createSEStable(self):
        self.sesTable = list()
        header = list()
        header.append('Σχολείο')
        header += self.specialEducationSpcTypes[:]
        header.append("Παρατηρήσεις")

        self.sesTable.append(header)
        for sch in self.specialEducationSchools:

            entry = list()
            entry.append(sch)
            sch_values = [0] * len(self.specialEducationSpcTypes)
            school_entries_descriptions = list()

            for vacancy_entry in self.entries:
                entry_variant = str(EntryVariantType(vacancy_entry.variant).label)
                school_name = vacancy_entry.school.name
                entry_type = vacancy_entry.type
                entry_hours = vacancy_entry.hours
                entry_specialization = vacancy_entry.specialty.code
                entry_description: str = vacancy_entry.description

                if school_name != sch:
                    continue

                if 'Ειδικής Αγωγής' in entry_variant:
                    spcType = f'{entry_specialization} - {entry_variant}'
                    indexScpType = self.specialEducationSpcTypes.index(spcType)
                    if entry_description is not None and len(entry_description.strip()) > 0:
                        school_entries_descriptions.append(f'{entry_specialization} - {entry_description}')

                    if entry_type == 'Κενό':
                        sch_values[indexScpType] -= int(entry_hours)
                    else:
                        sch_values[indexScpType] += int(entry_hours)
                else:
                    continue

            entry += sch_values
            entry.append("\n".join(school_entries_descriptions))

            self.sesTable.append(entry)

    def createGEStable(self):
        self.gesTable = list()
        header = list()
        header.append('Σχολείο')
        header += self.generalEducationSpcTypes[:]
        header.append("Παρατηρήσεις")

        self.gesTable.append(header)
        for sch in self.generalEducationSchools:

            entry = list()
            entry.append(sch)
            sch_values = [0] * len(self.generalEducationSpcTypes)
            school_entries_descriptions = list()

            for vacancy_entry in self.entries:
                entry_variant = str(EntryVariantType(vacancy_entry.variant).label)
                school_name = vacancy_entry.school.name
                entry_type = vacancy_entry.type
                entry_hours = vacancy_entry.hours
                entry_specialization = vacancy_entry.specialty.code
                entry_description: str = vacancy_entry.description

                if school_name != sch:
                    continue

                if entry_variant in ['Γενικής Αγωγής - Πανελλαδικώς Εξεταζόμενα Μαθήματα',
                                     'Γενικής Αγωγής - μη Πανελλαδικώς Εξεταζόμενα Μαθήματα']:
                    spcType = f'{entry_specialization} - {entry_variant}'
                    indexScpType = self.generalEducationSpcTypes.index(spcType)
                    if entry_description is not None and len(entry_description.strip()) > 0:
                        school_entries_descriptions.append(f'{entry_specialization} - {entry_description}')

                    if entry_type == 'Κενό':
                        sch_values[indexScpType] -= int(entry_hours)
                    else:
                        sch_values[indexScpType] += int(entry_hours)
                else:
                    continue

                spcType = f'{entry_specialization} - Γενικής Αγωγής (Σύνολο)'
                if spcType in self.generalEducationSpcTypes:
                    indexScpType = self.generalEducationSpcTypes.index(spcType)
                    if entry_type == 'Κενό':
                        sch_values[indexScpType] -= int(entry_hours)
                    else:
                        sch_values[indexScpType] += int(entry_hours)

            entry += sch_values
            entry.append("\n".join(school_entries_descriptions))

            self.gesTable.append(entry)

    def get_workbook(self):

        def style_ws(ws):

            # style header
            for col in range(ws.min_column, ws.max_column + 1):
                ws[get_column_letter(col) + '1'].style = 'header_style'

            # update column dimensions
            dim_holder = DimensionHolder(worksheet=ws)
            for col in range(ws.min_column, ws.max_column + 1):
                dim_holder[get_column_letter(col)] = ColumnDimension(ws, min=col, max=col, auto_size=True)

            ws.column_dimensions = dim_holder
            # update 1st row height
            ws.row_dimensions[1] = RowDimension(ws, height=180)

        self.getSchools()
        self.createSpecialtiesTypes()
        self.createTables()

        workbook = Workbook()

        header_style = NamedStyle(name="header_style")
        header_style.font = Font(bold=True, size=10)
        bd = Side(style='thick', color="000000")
        header_style.border = Border(bottom=bd)
        header_style.alignment = Alignment(textRotation=90, wrapText=True, horizontal="center", vertical="center")
        workbook.add_named_style(header_style)

        # Γενικής Αγωγής

        ws = workbook.active
        ws.title = 'Γενικής Αγωγής'
        ws.set_printer_settings(paper_size=Worksheet.PAPERSIZE_A4, orientation=Worksheet.ORIENTATION_PORTRAIT)

        if len(self.gesTable) > 1:

            for row in self.gesTable:
                ws.append(row)

            style_ws(ws)

        # Ειδικής Αγωγής
        ws = workbook.create_sheet(title='Ειδικής Αγωγής')
        if len(self.sesTable) > 1:

            for row in self.sesTable:
                ws.append(row)

            style_ws(ws)

        # Υπόλοιπα
        ws = workbook.create_sheet(title='Υπόλοιπα')
        if len(self.msTable) > 1:

            for row in self.msTable:
                ws.append(row)

            style_ws(ws)

        return workbook


@login_required
@user_passes_test(check_user_is_superuser)
@csrf_protect
def upload_specialties(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                excel_file = request.FILES["file"]

                workbook = load_workbook(excel_file)
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

                workbook = load_workbook(excel_file)
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

                workbook = load_workbook(excel_file)
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

                workbook = load_workbook(excel_file)
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


@login_required
@user_passes_test(check_user_is_superuser)
def excel_aggregated_entries(request):

    report = AggregatedEntriesReport()
    workbook = report.get_workbook()

    response = HttpResponse(content=save_virtual_workbook(workbook),
                            content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename=kena_aggregated.xlsx'
    return response
