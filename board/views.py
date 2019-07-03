from django.shortcuts import render, get_object_or_404, redirect
from django.views import generic
from . models import Board, Comment
from . forms import BoardForm, CommentForm
from django.contrib import messages
from django.http import HttpResponseRedirect, HttpResponse

class IndexView(generic.ListView):
    context_object_name = 'boards'
    paginate_by = 5 # 한 페이지에 5개 조회

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
    form_class = BoardForm
    success_url = '/board/'


class UpdateView(generic.UpdateView):
    model = Board
    form_class = BoardForm
    success_url = '/board/'
    template_name_suffix = '_update'


class DeleteView(generic.DeleteView):
    model = Board
    success_url = '/board/'
    template_name_suffix = '_delete'


class DetailView(generic.DetailView):
    model = Board
    context_object_name = 'board'

    def get_context_data(self, **kwargs):
        context = super(DetailView, self).get_context_data(**kwargs)
        context['comments'] = Comment.objects.filter(board_id=context['object'].id).all()
        return context


# class CommentWrite(generic.CreateView):
#     model = Comment
#     fields = ['board', 'username', 'content']
#     template_name = 'board/board_detail.html'
#
#     def form_invalid(self, form):
#         messages.error(self.request, '댓글을 입력해주세요!', extra_tags='danger')
#         return HttpResponseRedirect(self.get_success_url())
#
#     def form_valid(self, form):
#         form.save()
#         return HttpResponseRedirect(self.get_success_url())
#
#     def get_success_url(self):
#         return '/board/' + self.request.POST.get('board')


def comment_write(request, board_id):
    if request.method == 'POST' and 'username' in request.POST and 'board' in request.POST:
        form = CommentForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('board:detail', pk=board_id)
    messages.error()
    return redirect('board:detail', pk=board_id)



def comment_delete(request, board_id, comment_id):
    item = get_object_or_404(Comment, pk=comment_id)
    item.delete()
    return redirect('board:detail', pk=board_id)

