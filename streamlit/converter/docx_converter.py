import subprocess
import os
import requests

def convert_to_docx(input_file, output_dir):
    input_file = os.path.join('/shared_data', os.path.basename(input_file))
    output_dir = '/shared_data'

    print(1, 'input', input_file)
    if not os.path.isfile(input_file):
        raise FileNotFoundError(f"The file {input_file} does not exist.")
    print(2)

    if not os.path.isdir(output_dir):
        os.makedirs(output_dir)

    base_name = os.path.splitext(os.path.basename(input_file))[0]
    output_file = os.path.join(output_dir, base_name + '.docx')

    if os.name == 'nt':  # Windows
        libreoffice_path = r"C:\Program Files\LibreOffice\program\soffice.exe"
        command = [libreoffice_path, '--headless', '--convert-to', 'docx', input_file, '--outdir', output_dir]
        print(3, 'LibreOffice path:', libreoffice_path)
        print(4, 'Running command:', ' '.join(command))
        subprocess.run(command, check=True)
    else:  # Linux and others
        print('linux running~~~~~')
        url = "http://libreoffice:8800/convert"
        data = {'input_file': input_file, 'output_dir': output_dir}
        response = requests.post(url, json=data)
        if response.status_code != 200:
            raise RuntimeError(f"Failed to convert {input_file} to DOCX format. Error: {response.json()}")
        output_file = response.json().get('output_file')
    
    print(6, 'Output file created successfully:', output_file)
    return output_file