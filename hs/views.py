from django.shortcuts import render, redirect, get_object_or_404
from accounts.models import User


def hs_space(request):
    return render(request, 'hs/hs_space.html')


def list_all_members(request):
    return render(request, 'hs/all_members.html', {
        'users': User.objects.all(),
        'active': 'all_members',
    })
