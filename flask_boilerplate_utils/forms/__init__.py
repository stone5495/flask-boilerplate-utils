from wtforms.validators import Optional, ValidationError
import os

class ValidFileFormat(Optional):
    """
    Determines whether or not a file is valid for uploading
    by checking with flask-uploads.

    @param  fileupload  a FileUpload object from flask-uploads
    @param  message message to display upon validation error.

    @throws ValidationError if the uploaded data is not valid.
    """

    def __init__(self, fileupload, *args, **kwargs):
        self.fileupload = fileupload
        self.message = 'The selected file cannot be uploaded. Only %s are allowed.' % (
                ', '.join([t.lower() for t in fileupload._config.allow])
            )
        if 'message' in kwargs:
            self.message = kwargs['message']

    def __call__(self, form, field):
        filename, extension = os.path.splitext(field.data.filename)
        if not self.fileupload.extension_allowed(extension[1:].lower()):
            raise ValidationError(self.message)


class Unique(object):
    """
    Database Unique Validator for WTForms / SQLAlchemy.
    Throws ValidationError if the data alread exists in
    the database for the specified field.

    @param  model   SQL Alchemy ORM Model to target
    @param  field   SQL Alchemy ORM Field to compare
                    ie, Model.field
    @param  message message to display upon validation error.

    @throws ValidationError if the specified data already 
            exists in the database
    """
    def __init__(self, model, field, *args, **kwargs):
        self.model = model
        self.field = field
        self.message = 'A record with this information already exists.'
        if 'message' in kwargs:
            self.message = kwargs['message']

    def __call__(self, form, field):
        if self.model.query.filter(self.field == field.data).count() > 0:
            raise ValidationError(self.message)