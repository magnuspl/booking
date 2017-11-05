import csv
from django.contrib.auth.decorators import login_required
from django.http import StreamingHttpResponse
from .models import Membership, SportsGroup
from django.shortcuts import get_object_or_404
from datetime import date
from django.db.models import Q


class Echo(object):
    """An object that implements just the write method of the file-like
    interface.
    """
    def write(self, value):
        """Write the value by returning it, instead of storing in a buffer."""
        return value


@login_required
def download_members(request, slug):
    """A view that streams a large CSV file."""
    # Generate a sequence of rows. The range is based on the maximum number of
    # rows that can be handled by a single sheet in most spreadsheet
    # applications.
    # rows = (["Row {}".format(idx), str(idx)] for idx in range(65536))
    if request:
        pass

    group = get_object_or_404(SportsGroup, slug=slug)
    members = Membership.objects.filter(group=group.pk)
    header = ['FIRST NAME', 'SECOND NAME', 'EMAIL', 'PHONE', 'PAID']

    formatted_members = []
    for member in members:
        new_member = [
            member.person.first_name,
            member.person.last_name,
            member.person.email,
            member.person.phone,
            member.paid,
        ]
        formatted_members.append(new_member)

    sorted_formatted_members = sorted(formatted_members, key=lambda e: e[1])
    rows = [header] + sorted_formatted_members
    today = date.today().__str__()

    response = list_to_csv_http_response(rows)
    response['Content-Disposition'] = 'attachment; filename=""' + slug + '"members""' + today + '".csv"'
    return response

# https://stackoverflow.com/questions/739776/django-filters-or

def download_yearly_group_members(request, slug):
    group = get_object_or_404(SportsGroup, slug=slug)
    # 10 = whole year, 20 = half year
    # Entry.objects.filter(pub_date__month=12)
    # pub_date__gte=datetime.date(2005, 1, 30)

    current_year = datetime.date.today().year
    start_date = datetime.date(current_year, 8, 1)
    end_date = datetime.date(current_year+1, 1, 31)

    

    members = Membership.objects.filter(group=group.pk,
        expiry_date__date__range=(start_date, end_date))


def list_to_csv_http_response(inputList):
    pseudo_buffer = Echo()
    writer = csv.writer(pseudo_buffer, delimiter=';')
    response = StreamingHttpResponse((
        writer.writerow(row) for row in inputList),
                                     content_type="text/csv")
    return response
