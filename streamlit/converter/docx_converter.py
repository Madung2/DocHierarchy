import subprocess
import os

def convert_to_docx(input_file, output_dir):
    print(1, 'input', input_file)
    # Check if input file exists
    if not os.path.isfile(input_file):
        raise FileNotFoundError(f"The file {input_file} does not exist.")
    print(2)

    # Create output directory if it doesn't exist
    if not os.path.isdir(output_dir):
        os.makedirs(output_dir)

    # Define the output file path
    base_name = os.path.splitext(os.path.basename(input_file))[0]
    output_file = os.path.join(output_dir, base_name + '.docx')

    # Determine the OS and set the LibreOffice path accordingly
    if os.name == 'nt':  # Windows
        libreoffice_path = r"C:\Program Files\LibreOffice\program\soffice.exe"
        command = [libreoffice_path, '--headless', '--convert-to', 'docx', input_file, '--outdir', output_dir]
    else:  # Linux and others
        print('linux running~~~~~')
        libreoffice_path = "/usr/bin/libreoffice"
        command = [
            libreoffice_path,
            '--headless',
            '--convert-to', 'docx',
            input_file,
            '--outdir', output_dir,
           '--accept=socket,host=libreoffice,port=2002;urp;'
        ]
    
    print(3, 'LibreOffice path:', libreoffice_path)

    # Command to convert the file to DOCX format using LibreOffice

    # Run the command
    print(4, 'Running command:', ' '.join(command))
    subprocess.run(command, check=True)

    # Check if the output file is created
    print(5, 'Checking if output file was created:', output_file)
    if not os.path.isfile(output_file):
        raise RuntimeError(f"Failed to convert {input_file} to DOCX format.")
    
    print(6, 'Output file created successfully:', output_file)
    return output_file