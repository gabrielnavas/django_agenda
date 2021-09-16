from django.shortcuts import render, get_object_or_404, redirect
from .models import Contact, Category
from django.http import Http404, HttpResponseBadRequest
from django.db.models import Q, Value
from django.db.models.functions import Concat
from django.core.paginator import Paginator
from django.contrib import messages


def index(request):
    contacts = Contact.objects.order_by('-id').filter(
        is_show=True,
    )
    paginator = Paginator(contacts, per_page=20)

    page_number = request.GET.get('page')
    contacts = paginator.get_page(page_number)

    return render(request, 'contacts/index.html', {
        'contacts': contacts
    })


def show_contact(request, contact_id):
    contact = get_object_or_404(Contact, id=contact_id)
    if not contact.is_show:
        raise Http404()

    return render(request, 'contacts/show_contact.html', {
        'contact': contact
    })


def search(request):
    term = request.GET.get('term')
    fields = Concat('name', Value(' '), 'last_name')

    if not term or term is None:
        messages.add_message(request, messages.ERROR,
                             f"Digite um nome, ou sobrenome por exemplo.")
        return render(request, 'contacts/search.html', {
            'empty_list': True
        })

    contacts = Contact.objects.annotate(
        full_name=fields,
    ).filter(
        full_name__icontains=term
    )
    print(contacts.query)

    if len(contacts) == 0:
        messages.add_message(request, messages.WARNING,
                             f"'{term}' não encontrado.")
        return render(request, 'contacts/search.html', {
            'empty_list': True
        })

    paginator = Paginator(contacts, per_page=20)

    page_number = request.GET.get('page')
    contacts = paginator.get_page(page_number)

    return render(request, 'contacts/search.html', {
        'contacts': contacts
    })
