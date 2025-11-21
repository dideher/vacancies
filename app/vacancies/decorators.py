from functools import wraps
from django.http import HttpResponseForbidden
from django.template.response import TemplateResponse


def block_if(condition_func, response=None):
    """
    Decorator that blocks the view from executing if condition_func(request) returns True.

    Parameters:
        condition_func: callable(request) -> bool
        response: Optional HTTP response to return when blocked.
                  Defaults to HttpResponseForbidden.
    """
    def decorator(view_func):
        @wraps(view_func)
        def wrapper(request, *args, **kwargs):
            if condition_func(request):
                return response or HttpResponseForbidden("Action not allowed.")
            return view_func(request, *args, **kwargs)
        return wrapper

    return decorator


def block_if_templated(condition_func, template_name=None, context=None, status=403):
    """
    Decorator that blocks a view if condition_func(request) returns True.
    If a template is provided, it renders the template as the response.

    Parameters:
        condition_func: callable(request) -> bool
        template_name: Optional template name to render
        context: Optional context dict for the template
        status: HTTP status code (default: 403)
    """

    def decorator(view_func):
        @wraps(view_func)
        def wrapper(request, *args, **kwargs):

            result = condition_func(request)

            if isinstance(result, tuple):
                should_render, extra_context = result
            else:
                should_render, extra_context = result, {}

            effective_context = {}
            effective_context.update(context or {})
            effective_context.update(extra_context or {})

            if should_render:
                # Return an UNRENDERED TemplateResponse to preserve lifecycle
                return TemplateResponse(request, template_name, effective_context)

            return view_func(request, *args, **kwargs)

        return wrapper

    return decorator