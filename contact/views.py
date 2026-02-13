from django.shortcuts import render, redirect
from django.urls import reverse
from django.core.mail import EmailMessage
from django.contrib import messages
from django.conf import settings
from smtplib import SMTPException

from .forms import ContactForm


def contact(request):
    contact_form = ContactForm()

    if request.method == "POST":
        contact_form = ContactForm(data=request.POST)

        if contact_form.is_valid():
            name = contact_form.cleaned_data['name']
            user_email = contact_form.cleaned_data['email']
            content = contact_form.cleaned_data['content']

            email = EmailMessage(
                subject="Laboratorios: Nuevo mensaje de contacto",
                body=f"De {name} <{user_email}>\n\nEscribió:\n\n{content}",
                from_email=settings.DEFAULT_FROM_EMAIL,
                to=["jlla2254@gmail.com"],
                reply_to=[user_email]
            )

            try:
                email.send()
                messages.success(
                    request,
                    "Su mensaje se ha enviado correctamente, en breve nos pondremos en contacto con usted."
                )
                return redirect(reverse('contact'))

            except SMTPException:
                messages.error(
                    request,
                    "Ocurrió un error al enviar el mensaje. Inténtelo más tarde."
                )

    return render(request, "contact/contact.html", {
        'form': contact_form
    })


    
