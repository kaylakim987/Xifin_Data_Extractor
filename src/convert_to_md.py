import argparse
from pathlib import Path
from multiprocessing import Pool
from docling.document_converter import DocumentConverter

""" Convert all PDFs to Markdown format. """

converter = None
INPUT_ROOT = None
OUTPUT_ROOT = None

def create_argparser():
    """ Take in command line arguments and parse. """
    parser = argparse.ArgumentParser()

    parser.add_argument("-f",
                        "--files",
                        nargs="+",
                        required=True,
                        help="List of files to convert to md.")
    parser.add_argument("-np",
                        "--num_processes",
                        type=int,
                        default=1,
                        help="Number of worker processes.")
    parser.add_argument("-i",
                        "--input_root",
                        required=True,
                        help="Root directory of input PDFs.")
    parser.add_argument("-o",
                        "--output_root",
                        required=True,
                        help="Root directory of output PDFs.")


    return parser.parse_args()

def init_worker():
    """ Initialize Document Converter for the worker processes. """
    global converter
    converter = DocumentConverter()

def convert_to_md(pdf):
    """ Convert PDFs to Markdown format. """
    # Convert PDF to Markdown
    pdf = Path(pdf)

    try:
        global converter
        result = converter.convert(pdf)

        if hasattr(result.document, "export_to_markdown"):
            md = result.document.export_to_markdown()
        else:
            md = result.document.export_to_text()

        # Write Markdown file to corresponding directory (preserving original structure)
        relative_path = pdf.relative_to(INPUT_ROOT)

        output_path = OUTPUT_ROOT / relative_path.with_suffix(".md")
        output_path.parent.mkdir(parents=True, exist_ok=True)

        output_path.write_text(md, encoding="utf-8")

        return f"SUCCESS: {pdf}"

    except Exception as e:
        return f"ERROR: {pdf} -> {e}"

def process_files(files, num_processes):
    """ Concurrently process a list of files. """
    with Pool(processes=num_processes, initializer=init_worker) as pool:
        for result in pool.imap(convert_to_md, files):
            print(result)

def main():
    global INPUT_ROOT
    global OUTPUT_ROOT

    args = create_argparser()

    INPUT_ROOT = Path(args.input_root)
    OUTPUT_ROOT = Path(args.output_root)

    process_files(args.files, args.num_processes)

if __name__ == "__main__":
    main()