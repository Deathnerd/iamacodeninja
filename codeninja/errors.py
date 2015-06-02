# -*- coding: utf-8 -*-
from flask import g, render_template
from jinja2.exceptions import TemplateNotFound


class RequestErrors(object):
    # TODO: Proper logging for each error type
    """
    A nice, clean way to keep our page request errors separate from the
    runserver.py code. It's reusable, too!
    """
    def __init__(self, app=None):
        if app:
            self.init_app(app)
        self._template_error_defaults = {"type": "9001",
                                         "message": "It's over 9000!!!"}

    def init_app(self, app):
        """
        Pass your app object to start using this class to manage the errors
        :param app:
        :return:
        """
        self.app = app

        # The 404 page
        self.app.errorhandler(404)(self._page_not_found)

        # The 500 page
        self.app.errorhandler(500)(self._internal_server_error)

        # Template Not Found
        self.app.errorhandler(TemplateNotFound)(self._template_not_found)

    def _page_not_found(self, error):
        """
        The ubiquitous 404 page
        :param error:
        :return:
        """
        template_error = {"type": "404 Not Found",
                          "message": "This page cannot be found. Sorry... :("}
        return render_template("errors/general_error.html", error=template_error)

    def _internal_server_error(self, error):
        """
        For when shit hits the fan. Generally, if it can't be caught by any of the error handlers, then it will end up
        here. As a rule of thumb, you should always try to know what error you might encounter and, if you want this
        handler to take care of it, set up some info in g.request_error and this method will know about it
        :param error:
        :return:
        """
        template_error = {"type": "500 Internal Server Error",
                          "message": "The server is being stupid. Sorry... :("}
        # Check if we know exactly what the error is, which should always be the case. If not, then there's a fire and
        # we need to know!
        if g.request_error is None:
            # A polite, self-deprecating way of saying "Shit's on fire, yo"
            template_error['message'] = "The server is being more than just dumb. Contact support!"
        else:
            # TODO: Utilize the g.request_error property in logging errors
            pass

        return render_template("errors/general_error.html", error=template_error)

    def _template_not_found(self, error):
        """
        Primarily created with displaying user accounts in mind. Since we'll be managing the templates ourselves and
        not be serving anything outside of our control, and since the template names are being stored in the database
        and not modifiable by normal users, this error should almost never ever happen. However, if it does, then this
        method will take care of it
        :param error:
        :return:
        """
        template_error = self._template_error_defaults
        # check where the template is trying to be fetched from
        parts = error.message.split("/")  # split along the directory separators
        if parts[0].lower() == "user":
            template_error['message'] = "The user template '{}' does not exist".format(parts[-1])
            template_error['type'] = "404 Not Found"

        return render_template("errors/general_error.html", error=template_error)