from django.shortcuts import render, get_object_or_404, redirect
from django.views import generic
from . models import Board, Comment
from . forms import BoardForm, CommentForm
from django.contrib import messages
from django.http import HttpResponseRedirect, HttpResponse

class IndexView(generic.ListView):
    context_object_name = 'boards'
    paginate_by = 10 # 한 페이지에 10개 조회

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        paginator = context['paginator']
        page_numbers_range = 5  # 한 페이지에 5개의 번호
        max_index = len(paginator.page_range)

        page = self.request.GET.get('page')
        current_page = int(page) if page else 1

        start_index = int((current_page - 1) / page_numbers_range) * page_numbers_range
        end_index = start_index + page_numbers_range
        if end_index >= max_index:
            end_index = max_index

        context['page_range'] = paginator.page_range[start_index:end_index]
        return context

    def get_queryset(self):
        return Board.objects.order_by('-created_at')


class WriteView(generic.CreateView):
    model = Board
    fields = ['title', 'content', 'username']
    success_url = '/board/'


class DetailView(generic.DetailView):
    model = Board
    context_object_name = 'board'

    def get_context_data(self, **kwargs):
        context = super(DetailView, self).get_context_data(**kwargs)
        context['comments'] = Comment.objects.filter(board_id=context['object'].id).all()
        return context


class CommentWrite(generic.CreateView):
    model = Comment
    fields = ['board', 'username', 'content']
    template_name = 'board/board_detail.html'

    def form_invalid(self, form):
        messages.error(self.request, '댓글을 입력해주세요!', extra_tags='danger')
        return HttpResponseRedirect(self.get_success_url())

    def form_valid(self, form):
        form.save()
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return '/board/' + self.request.POST.get('board')

