import logging
from sys import exit
from typing import Callable, List, Tuple

import click

from copernicus_marine_client.catalogue_parser.request_structure import (
    NativeRequest,
)
from copernicus_marine_client.utils import FORCE_DOWNLOAD_CLI_PROMPT_MESSAGE


def download_native(
    username: str,
    password: str,
    native_request: NativeRequest,
    download_header: Callable,
    create_filenames_out: Callable,
) -> Tuple[List[str], List[str], str]:
    message, endpoint_url, filenames_in, total_size = download_header(
        str(native_request.dataset_url),
        native_request.regex,
        username,
        password,
    )
    filenames_out = create_filenames_out(
        filenames_in=filenames_in,
        output_directory=native_request.output_directory,
        no_directories=native_request.no_directories,
        overwrite=native_request.overwrite,
    )
    logging.info(message)
    if not total_size:
        logging.info("No data to download")
        exit(1)
    if native_request.show_outputnames:
        logging.info("Output filenames:")
        for filename_out in filenames_out:
            logging.info(filename_out)
    if not native_request.force_download:
        click.confirm(FORCE_DOWNLOAD_CLI_PROMPT_MESSAGE, abort=True)
    return (filenames_in, filenames_out, endpoint_url)
