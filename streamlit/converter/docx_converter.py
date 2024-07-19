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

    # Path to LibreOffice executable
    libreoffice_path = r"C:\Program Files\LibreOffice\program\soffice.exe"
    print(3)
    # Command to convert the file to DOCX format using LibreOffice
    command = [libreoffice_path, '--headless', '--convert-to', 'docx', input_file, '--outdir', output_dir]

    # Run the command
    subprocess.run(command, check=True)
    print(4)
    # Check if the output file is created
    if not os.path.isfile(output_file):
        raise RuntimeError(f"Failed to convert {input_file} to DOCX format.")
    print(5, output_file)
    return output_file

