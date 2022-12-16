from django.db.models import Sum
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib import messages

from userapp.models import TagNamesModel, UserRegisterModel

# Create your views here.
def admin_login(request):
    if request.method=='POST':
        name=request.POST.get('admin_name')
        pwd=request.POST.get('admin_password')
        if name=='admin' and pwd=='admin':
            messages.success(request,"login successfull")
            return redirect('admin_dashboard')
        else:
            messages.error(request,'Something Wrong, Please try again.')
            return redirect('index')
    return redirect('index')


def admin_logut(request):
    messages.success(request,'Logged Out Successfully')
    return redirect('index')


def admin_dashboard(request):
    total_users=UserRegisterModel.objects.all().count()
    rejected_users=UserRegisterModel.objects.filter(user_status='Rejected').count()
    accepted_users=UserRegisterModel.objects.filter(user_status='Accepted').count()
    tag_searches=TagNamesModel.objects.all().aggregate(Sum('count'))
    return render(request,'admin/admin-dashboard.html',{
        'total_users':total_users,
        'rejected_users':rejected_users,
        'accepted_users':accepted_users,
        'tag_searches':tag_searches
    })


def admin_searched_tweets_list(request):
    tags = TagNamesModel.objects.all()
    return render(request, 'admin/admin-searched-tweets-list.html',{
        'tags':tags
    })


def admin_view_users(request):
    pending_users=UserRegisterModel.objects.filter(user_status='Pending')
    Accepted_students=UserRegisterModel.objects.filter(user_status='Accepted')
    return render(request, 'admin/admin-view-users.html',{
        'pending_users':pending_users,
        'Accepted_students':Accepted_students
    })


def admin_user_status(request,user_id,status):
    user=get_object_or_404(UserRegisterModel,user_id=user_id)
    if status == 'Accept':
        user.user_status = 'Accepted'
        user.save(update_fields=['user_status'])
    else:
        user.user_status = 'Rejected'
        user.save(update_fields=['user_status'])
    return redirect('admin_view_users')