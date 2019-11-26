import os.path
import tempfile

from werkzeug.utils import secure_filename


def save_csv(form):
    """ An utility function to save a file in the /tmp directory,
    returning its path for further processing """
    csv = form.csv.data
    path = os.path.join(tempfile.gettempdir(),
                        secure_filename(csv.filename))
    csv.save(path)
    return path
