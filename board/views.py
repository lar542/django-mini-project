from django.shortcuts import render, get_object_or_404, redirect
from django.views import generic
from . models import Board, Comment, BoardLikePoint
from . forms import BoardForm, CommentForm, BoardLikePointForm
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from conf import settings


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


# 게시글 작성
class WriteView(LoginRequiredMixin, generic.CreateView):
    login_url = settings.LOGIN_URL
    model = Board
    form_class = BoardForm
    success_url = '/board/'


# 게시글 수정
class UpdateView(LoginRequiredMixin, generic.UpdateView):
    login_url = settings.LOGIN_URL
    model = Board
    form_class = BoardForm
    success_url = '/board/'
    template_name_suffix = '_update'


# 게시글 삭제
class DeleteView(LoginRequiredMixin, generic.DeleteView):
    login_url = settings.LOGIN_URL
    model = Board
    success_url = '/board/'
    template_name_suffix = '_delete'


# 게시글 조회
class DetailView(generic.DetailView):
    model = Board
    context_object_name = 'board'

    def get_context_data(self, **kwargs):
        context = super(DetailView, self).get_context_data(**kwargs)
        board_id = context['object'].id
        context['comments'] = Comment.objects.filter(board_id=board_id).all()
        point = BoardLikePoint.objects.filter(board_id=board_id, username=self.request.user.username)
        if point.count():
            context['point'] = point[0].like_point
        return context


# 게시글 추천
def board_like(request):
    if not request.user.is_authenticated:
        messages.error(request, '로그인이 필요합니다!')
        return redirect('user:login')
    username = request.POST.get('username')
    board_id = request.POST.get('board')
    query_set = BoardLikePoint.objects.filter(board=board_id, username=username)
    if query_set.count():
        query_set.delete()
    form = BoardLikePointForm(request.POST)
    if form.is_valid():
        form.save()
        return redirect('board:detail', pk=board_id)


# 댓글 작성
def comment_write(request, board_id):
    if not request.user.is_authenticated:
        messages.error(request, '로그인이 필요합니다!')
        return redirect('user:login')
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('board:detail', pk=board_id)
    return redirect('board:detail', pk=board_id)


def comment_delete(request, board_id, comment_id):
    item = get_object_or_404(Comment, pk=comment_id)
    item.delete()
    return redirect('board:detail', pk=board_id)

