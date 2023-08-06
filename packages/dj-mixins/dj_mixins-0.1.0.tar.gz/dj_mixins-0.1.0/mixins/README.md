# mixins

Custom Django mixins for class based views

## Getting started

Install `mixins`:

```shell
pip install dj-mixins
```

Now you can start using the mixins.

## Usage

Let's that we want to implement a view that accepts requests from superusers only. To achieve this we can use `SuperUserMixin`:

```python
""" Views.py """


from django.views.generic import TemplateView
from mixins.mixins import SuperUserMixin


# Create your views here.
class SuperUserView(SuperUserMixin, TemplateView):
    """ A view that accepts request from superusers only """

    template_name = 'myapp/index.html'

```

I hope that you find this useful.
