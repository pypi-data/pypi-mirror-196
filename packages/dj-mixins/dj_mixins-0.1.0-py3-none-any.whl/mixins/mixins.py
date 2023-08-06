""" Mixins """


from django.contrib import messages
from django.contrib.auth.mixins import (
    LoginRequiredMixin, PermissionRequiredMixin,
    UserPassesTestMixin
)


class DashboardMixin(LoginRequiredMixin, PermissionRequiredMixin):
    """ Check if the user is authenticated and has the required permission """


class MessageMixin:
    """ Base class to add messages """

    action = 'created'
    success = '{} was {} successfully.'
    error = 'An error occurred while processing.'

    def get_success(self):
        """ Return the success message """

        # Name of the model
        name = self.model._meta.verbose_name.title().capitalize()

        return self.success.format(name, self.action)

    def get_error(self):
        """ Return the success message """

        return self.error


class MessageMixinCreateView(MessageMixin):
    """ Add messages to django.views.generic.CreateView """

    def post(self, request, *args, **kwargs):
        """ Handle post requests """

        # Get the response
        response = super().post(request, *args, **kwargs)

        # Add the message
        messages.success(request, self.get_success())

        # Return the response
        return response


class MessageMixinUpdateView(MessageMixin):
    """ Add messages to django.views.generic.UpdateView """

    action = 'updated'

    def post(self, request, *args, **kwargs):
        """ Handle post requests """

        # Get the object
        self.object = self.get_object()

        # Get the response
        response = super().post(request, *args, **kwargs)

        # Add the message
        messages.success(request, self.get_success())

        # Return the response
        return response


class MessageMixinDeleteView(MessageMixin):
    """ Add messages to django.views.generic.UpdateView """
    action = 'deleted'

    def post(self, request, *args, **kwargs):
        """ Handle post requests """

        messages.success(request, self.get_success())
        return self.delete(request, *args, **kwargs)


class UserRequiredMixin(LoginRequiredMixin):
    """ Add the user field to a model when creating automatically """

    def form_valid(self, form):
        """ Add the user field """

        # Save without committing
        instance = form.save(commit=False)

        # Add the user field
        instance.user = self.request.user

        # Save the model
        instance.save()

        return super().form_valid(form)


class OwnerMixin(LoginRequiredMixin):
    """ Limit the user to view or update their own data """

    def get_queryset(self):
        """ Filter the queryset """

        # Get the queryset
        queryset = super().get_queryset()

        # Filter the queryset
        queryset.filter(user=self.request.user)

        return queryset


class UserMixin(UserPassesTestMixin):
    """ Limit the user to view or update their own user object """

    def test_func(self):
        """ Test function """

        return self.request.user == self.get_object()


class SuperUserMixin(UserPassesTestMixin):
    """ Verify that the current logged in user is a super user """

    def test_func(self):
        """ Test function """

        return self.request.user.is_superuser


class StaffUserMixin(UserPassesTestMixin):
    """ Verify that the current user is a staff user """

    def test_func(self):
        """ Test function """

        return self.request.user.is_staff
