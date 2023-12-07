from django.contrib import messages
from django.contrib.auth.mixins import(
    LoginRequiredMixin,
    PermissionRequiredMixin
)
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.db import IntegrityError
from django.shortcuts import get_object_or_404,render
from django.views import generic
from groups.models import Group,GroupMember,User
from . import models
from django.shortcuts import redirect ,render , get_object_or_404
from django.views.generic import UpdateView, DeleteView

def CreateGroup(request):
    if request.method=="POST":   
        name = request.POST['name']
        # slug = request.POST['slug']
        avatar = request.FILES['avatar']
        description = request.POST['description']          
        group = Group(name=name, avatar=avatar,description=description)
        group.save()        
        messages.success(request, "Chỉnh sửa thành công!")    
        return reverse("groups:all")
    return render(request, "add_new_group.html")

def ListGroups(request):
    group = Group.objects.order_by('-name')
    return render(request, "group.html",{'page_group': group} )
class JoinGroup(LoginRequiredMixin, generic.RedirectView):
    
    def get_redirect_url(self, *args, **kwargs):
        return reverse("groups:all")
        # return reverse("/group")
    def get(self, request, *args, **kwargs):
        group = get_object_or_404(Group,slug=self.kwargs.get("slug"))

        try:
            GroupMember.objects.create(user=self.request.user,group=group)

        except IntegrityError:
            messages.warning(self.request,("Warning, already a member of {}".format(group.name)))

        else:
            messages.success(self.request,"You are now a member of the {} group.".format(group.name))

        return super().get(request, *args, **kwargs)


class LeaveGroup(LoginRequiredMixin, generic.RedirectView):
    
    def get_redirect_url(self, *args, **kwargs):
        return reverse("groups:all")

    def get(self, request, *args, **kwargs):

        try:

            membership = models.GroupMember.objects.filter(
                user=self.request.user,
                group__slug=self.kwargs.get("slug")
            ).get()

        except models.GroupMember.DoesNotExist:
            messages.warning(
                self.request,
                "You can't leave this group because you aren't in it."
            )
        else:
            membership.delete()
            messages.success(
                self.request,
                "You have successfully left this group."
            )
        return super().get(request, *args, **kwargs)
    
def GroupDeleteView(request, id):
    gr_del = Group.objects.get(pk = id)
    if request.method == "POST":
        gr_del.delete()
        return redirect('group')
    return render(request, 'delblog.html',{'do_del':gr_del})

class getMemberGroup(LoginRequiredMixin, generic.RedirectView):
    # def get_redirect_url(self, *args, **kwargs):
    #     return reverse("groups:all")

    # def get(self, request, *args, **kwargs):
    #     try:
    #         membership = models.GroupMember.objects.filter(user=self.request.user,group__slug=self.kwargs.get("slug")).get()

    #     except models.GroupMember.DoesNotExist:
    #         messages.warning(
    #             self.request,
    #             "You can't leave this group because you aren't in it."
    #         )
    #     else:
    #         membership.delete()
    #         messages.success(
    #             self.request,
    #             "You have successfully left this group."
    #         )
    #     return super().get(request, *args, **kwargs)
    def get(self, request, *args, **kwargs):
        group = Group.objects.get(name='my_group')
        users = group.groupmember_set.all().values_list('user', flat=True)
        user_list = User.objects.filter(id__in=users)
        return render(request, 'delblog.html',{'user_list':user_list})