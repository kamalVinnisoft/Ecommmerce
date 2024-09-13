from django.shortcuts import render
from django.contrib import messages
# Create your views here.
def render_with_messages(request, template_name, context=None, success_message=None, error_message=None):
    if success_message:
        messages.success(request, success_message)
    if error_message:
        messages.error(request, error_message)
        print(error_message,">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
    print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>",success_message,error_message)
    return render(request, template_name, context or {})