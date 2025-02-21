from fpdf import FPDF
import os

def file_conversion(args):
    input_directory = args.input_directory
    convert_all_text_files(input_directory)

def convert_all_text_files(directory):
    for filename in os.listdir(directory):
        if filename.endswith(".txt"):
            input_file = os.path.join(directory, filename)
            output_file = os.path.join(directory, os.path.splitext(filename)[0] + ".pdf")
            output_file = get_unique_filename(output_file)
            convert_text_to_pdf(input_file, output_file)

def get_unique_filename(output_file):
    base, extension = os.path.splitext(output_file)
    counter = 1
    new_output_file = output_file

    while os.path.exists(new_output_file):
        new_output_file = f"{base}_{counter}{extension}"
        counter += 1

    return new_output_file

def convert_text_to_pdf(input_file, output_file):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    with open(input_file, 'r') as file:
        for line in file:
            pdf.cell(200, 10, txt=line, ln=True)

    pdf.output(output_file)
    print(f"Converted {input_file} to {output_file}")

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Convert text files in a directory to PDF")
    parser.add_argument("-d", "--input_directory", required=True, help="Input directory containing text files")
    args = parser.parse_args()
    file_conversion(args)