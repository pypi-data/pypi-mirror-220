from __future__ import annotations

import logging
from datetime import datetime
from typing import TYPE_CHECKING, Any

import yaml
from fastapi.templating import Jinja2Templates as FastAPIJinja2Templates
from opentelemetry import trace
from opentelemetry.trace import SpanKind
from starlette.datastructures import URL
from starlette.routing import Router
from starlette.templating import pass_context

logger = logging.getLogger(__name__)
tracer = trace.get_tracer(__name__)

if TYPE_CHECKING:
    pass

def filter_yaml(value: Any, sort_keys=True, indent=2) -> str:
    return yaml.dump(value, sort_keys=sort_keys, indent=indent, allow_unicode=True)

def filter_time_ago(dt: datetime) -> str:
    now = datetime.utcnow()
    diff = now - dt
    days = diff.days
    seconds = diff.seconds
    if days > 0:
        return f"{days} days ago" if days > 1 else f"{days} day ago"
    elif seconds > 3600:
        hours = seconds // 3600
        return f"{hours} hours ago" if hours > 1 else f"{hours} hour ago"
    elif seconds > 60:
        minutes = seconds // 60
        return f"{minutes} minutes ago" if minutes > 1 else f"{minutes} minute ago"
    else:
        return f"{seconds} seconds ago" if seconds > 1 else f"{seconds} second ago"


class Jinja2Templates(FastAPIJinja2Templates):

    def _create_env(self, *args, **kwargs) -> "jinja2.Environment":
        from mweb import config
        templates_config = config.get("mweb", {}).get("templates", {})
        cache_size = templates_config.get("cache_size", 1000)
        kwargs["cache_size"] = cache_size

        env = super()._create_env(*args, **kwargs)

        @pass_context
        def url(context: dict, name: str, **path_params: Any) -> URL:
            request = context["request"]
            router: Router = request.scope["router"]
            try:
                url_path = router.url_path_for(name, **path_params)
            except AssertionError as e:
                raise ValueError(f"Could not generate url for '{name}' with params {path_params}: {e}") from e
            return url_path

        env_config = templates_config.get("env", {})
        env.globals.update(env_config.get("globals", {}))

        env.globals["url"] = url

        env.filters["json"] = env.filters["tojson"]
        env.filters["time_ago"] = filter_time_ago
        env.filters["yaml"] = filter_yaml

        return env

    def TemplateResponse(self, name, *args, **kwargs):
        with tracer.start_as_current_span(f"template.render", kind=SpanKind.INTERNAL) as span:  # type: trace.Span
            span.set_attribute("template.name", name)
            return super().TemplateResponse(name, *args, **kwargs)
