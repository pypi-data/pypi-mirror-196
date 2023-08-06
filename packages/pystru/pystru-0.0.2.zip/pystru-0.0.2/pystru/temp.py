from jinja2 import Environment, FileSystemLoader
import os, shutil

def set_environment(folder: str, template:str):
    env = Environment(loader=FileSystemLoader(folder))
    template = env.get_template(template)
    return template

def create_folder_file(templates_dir: str, files: list, folders: list, meta_data: dict, **kwargs):
    for folder in folders:
        os.makedirs(name=folder, exist_ok=True)
    
    for file in files:
        temp = set_environment(folder=templates_dir, template=file)
        with open(file, "w", encoding="utf-8") as f:
            f.write(temp.render(**meta_data))
    
    for dst, src in kwargs.items():
        shutil.copyfile(dst=dst, src=src)