import os
import pandas as pd
import plotly.express as px
from werkzeug.utils import secure_filename
from flask import current_app
from flask_login import current_user
from functools import wraps
from flask import abort

def secure_file(filename):
    """
    Sécurise un nom de fichier pour éviter les caractères dangereux.
    """
    return secure_filename(filename)

def read_csv(file_path):
    """
    Lit un fichier CSV et le convertit en DataFrame Pandas.
    """
    try:
        df = pd.read_csv(file_path)
        return df
    except Exception as e:
        print(f"Error reading CSV file: {e}")
        return None

def save_csv(df, file_path):
    """
    Sauvegarde un DataFrame Pandas en fichier CSV.
    """
    try:
        df.to_csv(file_path, index=False)
        return True
    except Exception as e:
        print(f"Error saving CSV file: {e}")
        return False

def create_scatter_plot(df, x_column, y_column):
    """
    Génère un graphique de dispersion avec Plotly.
    """
    fig = px.scatter(df, x=x_column, y=y_column)
    return fig.to_html(full_html=False)

def allowed_file(filename):
    """
    Vérifie si le fichier a une extension autorisée.
    """
    ALLOWED_EXTENSIONS = {'csv', 'txt'}
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def admin_required(f):
    """
    Décorateur pour restreindre l'accès aux administrateurs.
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_admin:
            abort(403)
        return f(*args, **kwargs)
    return decorated_function

def save_uploaded_file(upload_folder, file):
    """
    Sauvegarde un fichier téléchargé dans le dossier spécifié.
    """
    if file and allowed_file(file.filename):
        filename = secure_file(file.filename)
        file_path = os.path.join(upload_folder, filename)
        file.save(file_path)
        return file_path
    return None

