from rest_framework.renderers import JSONRenderer
import json


class ProfileRenderer(JSONRenderer):
    charset = 'utf-8'

    def render(self, data, accepted_media_type=None, renderer_context=None):
        status_code = renderer_context["response"].status_code
        errors = data.get("errors", None)

        if errors is not None:
            return super(ProfileRenderer, self).render(data)
        return json.dumps({"status_code": status_code, "banking_profile": data})


class ProfilesRenderer(JSONRenderer):
    charset = 'utf-8'

    def render(self, data, accepted_media_type=None, renderer_context=None):
        status_code = renderer_context["response"].status_code
        errors = data.get("errors", None)

        if errors is not None:
            return super(ProfilesRenderer, self).render(data)
        return json.dumps({"status_code": status_code, "banking_profiles": data})
