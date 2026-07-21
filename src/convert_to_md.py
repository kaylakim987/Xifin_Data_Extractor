import argparse
import logging
from pathlib import Path
from multiprocessing import Pool
from docling.document_converter import DocumentConverter
from logging_config import setup_logger

""" Convert all PDFs to Markdown format. """

converter = None
INPUT_ROOT = None
OUTPUT_ROOT = None
logger = None

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
    global logger

    logger = setup_logger()
    converter = DocumentConverter()

    logger.info("DocumentConverter initialized")

def convert_to_md(pdf):
    """ Convert PDFs to Markdown format. """
    global converter
    global logger

    # Convert PDF to Markdown
    pdf = Path(pdf)

    try:
        logger.info("Starting PDF=%s", pdf)
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

        logger.info("SUCCESS PDF=%s OUTPUT=%s", pdf, output_path)

        return f"SUCCESS: {pdf}"

    except Exception as e:
        logger.info("Exception PDF=%s -> %s", pdf, e)
        return f"ERROR: {pdf} -> {e}"

def process_files(files, num_processes):
    """ Concurrently process a list of files. """
    with Pool(processes=num_processes, initializer=init_worker) as pool:
        for result in pool.imap(convert_to_md, files):
            logger.info(result)

def main():
    global INPUT_ROOT
    global OUTPUT_ROOT
    global logger

    args = create_argparser()

    INPUT_ROOT = Path(args.input_root)
    OUTPUT_ROOT = Path(args.output_root)

    logger = setup_logger()

    process_files(args.files, args.num_processes)

if __name__ == "__main__":
    main()