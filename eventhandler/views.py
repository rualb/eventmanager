from django.http import JsonResponse, HttpResponse
from django.shortcuts import render

# Create your views here.
from django.views.generic import DetailView, ListView, UpdateView, View, FormView, CreateView

from django.core.paginator import Paginator, EmptyPage
from django.core import serializers
from eventmanager.forms import FilterForm
from django.utils.translation import gettext_lazy as _


import json

from . import models

from .forms import EventRecordForm
from .models import EventRecord

from django.shortcuts import render
from .models import EventRecord

from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import permission_required

from django.shortcuts import get_object_or_404
from django.forms.models import model_to_dict

from django.db.models import Q


class EventRecordDetail(DetailView):
    model = EventRecord
    template_name = 'detail.html'

    def get_context_data(self, **kwargs):
        context = super(EventRecordDetail, self).get_context_data(**kwargs)
        context['form'] = EventRecordForm(model_to_dict(self.object))
        return context


# class EventRecordCopy(CreateView):
#     model = EventRecord
#     template_name = 'form.html'
#     form_class = EventRecordForm

#     def form_valid(self, form):
#         form.instance.user = self.request.user
#         return super(EventRecordCopy, self).form_valid(form)


class ValidatedPaginator(Paginator):
    def validate_number(self, number):
        try:
            return super(ValidatedPaginator, self).validate_number(number)
        except EmptyPage:
            if number > 1:
                return self.num_pages
            else:
                raise


def normalize_query(query_string):
    # query_string,
    #                 findterms=re.compile(r'"([^"]+)"|(\S+)').findall,
    #                 normspace=re.compile(r'\s{2,}').sub):
    # '''
    # Splits the query string in invidual keywords, getting rid of unecessary spaces and grouping quoted words together.
    # Example:
    # >>> normalize_query('  some random  words "with   quotes  " and   spaces')
    #     ['some', 'random', 'words', 'with quotes', 'and', 'spaces']
    # '''
    # return [normspace('', (t[0] or t[1]).strip()) for t in findterms(query_string)]
    return [query_string]


def get_query(query_string, search_fields):

    query = None  # Query to search for every search term
    terms = normalize_query(query_string)
    for term in terms:
        or_query = None  # Query to search for a given term in each field
        for field_name in search_fields:
            q = Q(**{"%s__icontains" % field_name: term})
            if or_query is None:
                or_query = q
            else:
                or_query = or_query | q
        if query is None:
            query = or_query
        else:
            query = query & or_query
    return query


class EventRecordCopy(CreateView):
    model = EventRecord
    template_name = 'form.html'
    form_class = EventRecordForm

    initial = {}

    def get_context_data(self, **kwargs):
        context = super(EventRecordCopy, self).get_context_data(**kwargs)
        return context

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        # kwargs['user'] = self.request.user
        return kwargs

    def get_initial(self):
        _initial = super(EventRecordCopy, self).get_initial()
        obj = get_object_or_404(self.model, pk=self.kwargs.get('pk'))
        obj_data = model_to_dict(obj, exclude=['id', 'pk'])
        _initial.update(obj_data)
        return _initial


class EventRecordCreate(CreateView):
    model = EventRecord
    template_name = 'form.html'
    form_class = EventRecordForm

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(EventRecordCreate, self).form_valid(form)


class EventRecordUpdate(UpdateView):
    model = EventRecord
    template_name = 'form.html'
    form_class = EventRecordForm

    def get_context_data(self, **kwargs):
        context = super(EventRecordUpdate, self).get_context_data(**kwargs)

        return context

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(EventRecordUpdate, self).form_valid(form)


class EventRecordListView(ListView):

    model = EventRecord
    paginator_class = ValidatedPaginator
    paginate_by = 10  # if pagination is desired
    # context_object_name = 'items'
    template_name = 'model_list.html'
    ordering = ['-id']

    filter_initial = {
        'filter': '',
        'orderby': '-id',
    }

    orderby_list = {
        '-id': 'Index Desc',
        'id': 'Index Asc',
    }

    filter_list = [

        'specode',
        'textf1',
        'textf2',
        'textf3',
        'textf4',

    ]

 

    def get_paginator(self,   *args, **kwargs):
        pg = super(EventRecordListView, self).get_paginator(*args, **kwargs)
        return pg

    def get(self, request, *args, **kwargs):

        filter = self.request.GET.get('filter')

        return super(EventRecordListView, self).get(request, *args, **kwargs)

    def get_ordering(self):
        ordering = self.request.GET.get('orderby', '-id')
        return ordering

    def get_paginate_by(self, queryset):
        return self.paginate_by

    def get_queryset(self):
        result = super(EventRecordListView, self).get_queryset()
        #
        filter = self.request.GET.get('filter', '').strip()
        if filter:
            entry_query = get_query(filter, self.filter_list)
            result = result.filter(entry_query)

        return result

    def get_context_data(self, **kwargs):

        data = {}

        for k, v in self.filter_initial.items():
            data[k] = v
        for k, v in (self.request.GET or {}).items():
            data[k] = v

        form = FilterForm(data=data)

        context = super().get_context_data(**kwargs)

        context['url_rec_create'] = 'eventrecord_create'
        context['url_rec_detail'] = 'eventrecord_detail'
        context['url_rec_copy'] = 'eventrecord_copy'
        context['url_rec_edit'] = 'eventrecord_edit'
        context['form_filter'] = form
        context['orderby_list'] = {
            '-id': str(_('Nr'))+': '+str(_('Order Desc')),
            'id': str(_('Nr'))+': '+str(_('Order Asc')),
        }

        context['title'] = _('Event Records')

        record_format = _(
            'Event Record: Nr: {id}, Type: {specode}, Title: {textf2}')

        for itm in context['object_list']:
            itm.formated = models.model_format(itm, record_format)

        return context
