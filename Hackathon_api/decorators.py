from django.contrib.auth import authenticate
from django.shortcuts import redirect
from django.http import JsonResponse
from django.contrib.auth import authenticate
import json

def authorized_users_only(group_index,allowed_roles=[]):
    def decorator(view_func):
        def wrapper_func(request,*awgs,**kwags):
            if request.method == 'POST':
                json_data = json.loads(request.POST['credentials'])
                username = json_data.get('username')
                password = json_data.get('password')
                user = authenticate(username = username,password = password)
                try:
                    if user.groups.exists():
                        group = user.groups.all()[group_index].name
                        if group in allowed_roles:
                            return view_func(request,*awgs,**kwags)
                        else:
                            return JsonResponse({'authentication_error': "access denied"})
                except Exception as e:
                    return JsonResponse({'authentication_group_error': str(e)})
        return wrapper_func
    return decorator