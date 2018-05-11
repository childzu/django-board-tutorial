from django.views.generic import ListView
from boards.models import Board, Post, Topic
from django.shortcuts import get_object_or_404, redirect, render
from django.db.models import Count

class PostListView(ListView):
    model = Post
    context_object_name = 'posts'
    template_name = 'post/topic_posts.html'
    paginate_by = 5

    def get_context_data(self, **kwargs):
        # self.topic.views += 1
        # self.topic.save()
        session_key = 'viewed_topic_{}'.format(self.topic.pk)  # <-- here
        if not self.request.session.get(session_key, False):
            self.topic.views += 1
            self.topic.save()
            self.request.session[session_key] = True           # <-- until here

        kwargs['topic'] = self.topic
        return super().get_context_data(**kwargs)

    def get_queryset(self):
        self.topic = get_object_or_404(Topic, board__pk=self.kwargs.get('pk'), pk=self.kwargs.get('topic_pk'))
        queryset = self.topic.posts.order_by('created_at')
        return queryset
