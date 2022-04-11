from wtforms.widgets import PasswordInput, CheckboxInput, TextInput, FileInput, RadioInput, TextArea, Select
from wtforms.widgets.html5 import EmailInput
from wtforms.widgets.html5 import URLInput


class VerifyInputMixin:
    def __init__(self, error_class=u"is-invalid", *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.error_class = error_class

    def __call__(self, field, **kwargs):
        if field.errors:
            c = kwargs.pop("class", "") or kwargs.pop("class_", "")
            kwargs["class"] = u"%s %s" % (self.error_class, c)
        return super().__call__(field, **kwargs)


class VerifyTextArea(VerifyInputMixin, TextArea):
    pass


class VerifyEmail(VerifyInputMixin, EmailInput):
    pass


class VerifyPassword(VerifyInputMixin, PasswordInput):
    pass


class VerifyBoolean(VerifyInputMixin, CheckboxInput):
    pass


class VerifyText(VerifyInputMixin, TextInput):
    pass


class VerifyFile(VerifyInputMixin, FileInput):
    pass


class VerifyRadio(VerifyInputMixin, RadioInput):
    pass


class VerifySelect(VerifyInputMixin, Select):
    pass


class VerifyURL(VerifyInputMixin, URLInput):
    pass
