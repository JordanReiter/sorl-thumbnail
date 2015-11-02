from django.utils.html import escape, conditional_escape
from django.utils.safestring import mark_safe
from django.forms.widgets import ClearableFileInput, CheckboxInput

class ClearableImageInput(ClearableFileInput):
    template_with_initial = u'<div class="image-field"><div class="image-currently">%(initial_text)s:</div><div class="image-preview">%(initial)s</div><div class="image-clear">%(clear_template)s</div>%(input_text)s: %(input)s</div>'

    def render(self, name, value, attrs=None):
        from sorl.thumbnail import get_thumbnail
        from sorl.thumbnail.conf import settings
        height = attrs.pop('height', getattr(settings, 'THUMBNAIL_HEIGHT', None))
        width = attrs.pop('width', getattr(settings, 'THUMBNAIL_WIDTH', None))
        substitutions = {
            'initial_text': self.initial_text,
            'input_text': self.input_text,
            'clear_template': '',
            'clear_checkbox_label': self.clear_checkbox_label,
        }
        template = u'%(input)s'
        substitutions['input'] = super(ClearableFileInput, self).render(name, value, attrs)

        if value and hasattr(value, "url"):
            thumbnail_url = value.url
            dimensions = ""
            if height or width:
                geo = ""
                if width:
                    geo += "%d" % width
                if height:
                    geo += "x%d" % height
                try:
                    im = get_thumbnail(value, geo)
                    height = im.height
                    width = im.width
                    thumbnail_url = im.url
                except:
                    pass
                if height:
                    dimensions += ' height="%d"' % height
                if width:
                    dimensions += ' width="%d"' % width
            template = self.template_with_initial
            substitutions['initial'] = (u'<img src="%s"%s />'
                                        % (escape(thumbnail_url),
                                           dimensions))
            if not self.is_required:
                checkbox_name = self.clear_checkbox_name(name)
                checkbox_id = self.clear_checkbox_id(checkbox_name)
                substitutions['clear_checkbox_name'] = conditional_escape(checkbox_name)
                substitutions['clear_checkbox_id'] = conditional_escape(checkbox_id)
                substitutions['clear'] = CheckboxInput().render(checkbox_name, False, attrs={'id': checkbox_id})
                substitutions['clear_template'] = self.template_with_clear % substitutions

        return mark_safe(template % substitutions)
