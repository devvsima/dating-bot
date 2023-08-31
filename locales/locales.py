import gettext
import os

localedir = os.path.join(os.path.abspath("/path/to/locales"), "locales")
translate = gettext.translation("domain_name", localedir, ["ru"])
_ = translate.gettext

print(_("some_text"))
print(_("some_text_2"))
