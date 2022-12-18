from django import forms
from material import Layout, Row


class ForumCreatePost(forms.Form):
    """Form to create a ForumPost"""

    title = forms.CharField(label="Title", max_length=100)
    body = forms.CharField(label="Body", widget=forms.Textarea, required=False)
    is_anonymous = forms.BooleanField(label="Post anonymously?",
                                      help_text="Your post will be anonymous to your peers, but identifiable to staff.",
                                      required=False)

    layout = Layout(Row("title", "is_anonymous"), "body")


class ForumCreateReply(forms.Form):
    """Form to create a ForumReply"""

    body = forms.CharField(label="Reply", widget=forms.Textarea)
    is_anonymous = forms.BooleanField(label="Reply anonymously?",
                                      help_text="Your reply will be anonymous to your peers, but identifiable to staff.",
                                      required=False)

    layout = Layout("body", "is_anonymous")
