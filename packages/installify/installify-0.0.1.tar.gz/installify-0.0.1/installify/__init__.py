import os
import shutil
import zipfile
from loadwave import Loader
import urllib.request


def install(url, company_name, program_name):
    loader = Loader('Downloading')
    loader.start()

    zip_name = 'temp.zip'
    urllib.request.urlretrieve(url, zip_name)

    loader.stop()

    with zipfile.ZipFile(zip_name, 'r') as zip_ref:
        new_folder = os.path.join(os.environ['APPDATA'], company_name, program_name)
        os.makedirs(new_folder, exist_ok=True)

        for member in zip_ref.namelist():
            filename = os.path.basename(member)

            if not filename or filename.startswith('.'):
                continue
            source = zip_ref.open(member)
            target = open(os.path.join(new_folder, filename), "wb")
            with source, target:
                shutil.copyfileobj(source, target)

    os.remove(zip_name)
    
    print(f"{program_name} successfully installed.")
