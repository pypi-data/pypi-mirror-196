#dredger documentation
This module is used to download uspto patent applications and grant files. USPTO publishes all granted patents of the week on tuesday and all applications on Thursday.

Additionally the module has two important date functions (date_on_day & weekday_count)

The function takes following inputs(two)
- [Mandatory] Type of file to be downloaded i.e. applications or grants or pdfs[string]
- [Optional] Date (function will automatically calculates the last Tuesday of Thursday)

