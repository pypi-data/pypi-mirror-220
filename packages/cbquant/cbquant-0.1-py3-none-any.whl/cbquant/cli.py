import argparse
from multiprocessing import Pool
from functools import partial
import os
from zipfile import ZipFile

from tqdm import tqdm

from cbquant.cbquant import find_files
from cbquant.cbquant import extract_parallel, extract_serial
from cbquant.cbquant import process_image
from cbquant.cbquant import write_to_cbz, write_to_cbz_parallel


def main():
    parser = argparse.ArgumentParser(
                        description="""cbqaunt: A Lossy Comic Book Archive 
                        Compressor.""")
    parser.add_argument("input_path", type=str, 
                        help="""Path to the input comic book archive file, 
                        directory, or glob syntax.""")
    parser.add_argument("--height", type=int, default=None, 
                        help="""Height to resize large images to. 
                        Aspect raio is maintained""")
    parser.add_argument("--ncolors", type=int, default=2, 
                        help="Number of colors for images.")
    parser.add_argument("--color_ncolors", type=int, default=None, 
                        help="""Number of colors for color images. 
                        Overrides ncolors.""")
    parser.add_argument("--output_dir", type=str, default=None, 
                        help="""Name and destination of the output file. 
                        Defaults to the same location and name (with quant 
                        added) as the input file. If the directory does not 
                        exist, it will be created.
                        """)
    args = parser.parse_args()

    # Filling in defaults
    if args.color_ncolors is None:
        # If color quant not specified, quantize with ncolors
        args.color_ncolors = args.ncolors

    # Get all files for processing
    files = find_files(args.input_path)
    files.sort()

    for i, file_path in enumerate(files):
        # Default to the same name/output file path with "quant" added
        dirpath, filename = os.path.split(file_path)
        basename, ext = os.path.splitext(filename)
        if args.output_dir is None:
            output_path = os.path.join(dirpath, f"{basename}-quant{ext}")
        else:
            os.makedirs(args.output_dir, exist_ok=True)
            output_path = os.path.join(args.output_dir, f"{basename}-quant{ext}")

        input_zip = ZipFile(file_path)

        # Extract the archive to memory
        print(f"({i}/{len(files)}) Extracting {basename}{ext}")
        cb_files = None
        try:
            cb_files = extract_parallel(input_zip)
        except Exception as e:
            print(e)
            print("Error on parallel extraction.")
            print("Attempting to extract in Serial...")
            cb_files = extract_serial(input_zip)

        # Parallel process all the pages
        print("Processing images...")
        func = partial(process_image, args.height, args.ncolors, args.color_ncolors)
        with Pool() as p:
            cb_quant = dict(tqdm(p.imap(func, cb_files.items()), total=len(cb_files)))

        # Write the quantized archive
        print("Writing file...")
        try:
            write_to_cbz_parallel(cb_quant, output_path)
        except Exception as e:
            print(e)
            print("Error on parallel write-out.")
            print("Attempting to write in Serial...")
            write_to_cbz(cb_quant, output_path)
        
        print("Done")

if __name__ == "__main__":
    main()