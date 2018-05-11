from django.views.generic import ListView
from boards.models import Board, Post, Topic
from django.shortcuts import get_object_or_404, redirect, render
from django.db.models import Count

class TopicListView(ListView):
    model = Topic
    context_object_name = 'topics'
    template_name = 'topic/topics.html'
    paginate_by = 7

    def get_context_data(self, **kwargs):
        kwargs['board'] = self.board
        return super().get_context_data(**kwargs)

    def get_queryset(self):
        self.board = get_object_or_404(Board, pk=self.kwargs.get('pk'))
        queryset = self.board.topics.order_by('-last_updated').annotate(replies=Count('posts') - 1)
        return queryset
