"""Functionality to modify parquet files in an S3 bucket"""
from __future__ import annotations

import gc
from dataclasses import dataclass
from typing import Optional
from aiobotocore.session import AioSession

import boto3
import loguru
import pyarrow.parquet as pq
import s3fs

from dai_python_commons.s3_utils import S3Utils


@dataclass
class ParquetFileLocation:
    """
    Class that contains information about parquet files location in S3.

    args:
        source_bucket (str): The bucket where the parquet files to be merged are located.
        source_prefix (str): The prefix (ie 'folder') where the parquet files are located.
        destination_bucket (str): The bucket where the larger parquet file should be located. It can be the same as the
        source bucket.

        destination_prefix (str): The prefix (ie 'folder') where the merged file should be written
        compression (str): Type of compression. Accepted values are 'NONE', 'SNAPPY', 'GZIP', 'BROTLI', 'LZ4', 'ZSTD'
        remove_files_at_destination (bool): whether the files at the destination folder should be removed before
        writing the merged parquet file

        keep_source_files (bool): whether the source files should be kept after merge
        maximum_file_size (int): only parse sets of files which totals (in Bytes) under this limit
    """
    # pylint: disable=R0902
    source_bucket: str
    source_prefix: str
    destination_bucket: str = ""
    destination_prefix: str = ""
    compression: Optional[str] = "SNAPPY"
    remove_files_at_destination: bool = False
    keep_source_files: bool = True
    total_files_size: int = 1024 * 1024 * 1024   # 1GB


class ParquetUtils:
    """
    Class that provides functionality for manipulating parquet files
    """
    # pylint: disable=no-member
    VALID_COMPRESSION_TYPES = {'NONE', 'SNAPPY', 'GZIP', 'BROTLI', 'LZ4', 'ZSTD'}

    @staticmethod
    def s3_merge_files_in_place(boto3_session: boto3.Session,
                                parquet_file_location: ParquetFileLocation,
                                logger: loguru.Logger,
                                compression: Optional[str] = "SNAPPY",
                                keep_source_files: bool = False) -> int:
        """
         Merge many small parquet files into one larger parquet file. In place.

        :param boto3_session: Boto3 session
        :param parquet_file_location: s3 bucket and prefix location where parquet files will be merged
        :param logger: The logger
        :param compression: Type of compression. Accepted values are 'NONE', 'SNAPPY', 'GZIP', 'BROTLI', 'LZ4', 'ZSTD'
        :param keep_source_files: True to keep the source files, False to delete them.
        :return:
        """
        data_path = f"s3://{parquet_file_location.source_bucket}/{parquet_file_location.source_prefix}"
        logger.info(f"Merging files from {data_path} to {data_path}, compression: {compression}")

        # this is a bit of hack, one should probably find a better way to do this
        botoc_session = boto3_session._session # pylint: disable=protected-access
        aio_session = AioSession(session_vars=botoc_session.session_var_map)
        f_s = s3fs.S3FileSystem(session=aio_session)

        boto_s3_client = boto3_session.client("s3")
        num_rows = 0

        file_paths_iter = S3Utils.iter_file_paths_in_prefix(boto_s3_client=boto_s3_client,
                                                  bucket_name=parquet_file_location.source_bucket,
                                                  prefix=parquet_file_location.source_prefix,
                                                  logger=logger,
                                                  max_size=parquet_file_location.total_files_size)
        for file_paths in file_paths_iter:
            if len(file_paths) <2:
                logger.info(f"file paths is less than 2 files, no reason to merge: {file_paths}")
                continue
            logger.info(f"Reading and merging {file_paths}")

            full_s3_paths = [f's3://{parquet_file_location.source_bucket}/{file_path["Key"]}' for file_path in file_paths]

            # partitioning=None ensures we do not add a column dt when parsing
            # our parquet files that usually have a "hive-like" partitioned dt
            # path, which we do not wish to add to the set when consolidating.
            # The type in the interface is wrong, source code does handle the None
            pq_table = pq.read_table(full_s3_paths, filesystem=f_s, partitioning=None)  # type: ignore
            num_rows += pq_table.num_rows
            logger.debug(f"Shape of the table {pq_table.shape}")

            logger.debug(f"Writing to the destination {data_path}")
            try:
                pq.write_to_dataset(pq_table, data_path, filesystem=f_s, compression=compression)
                logger.info(f"Done merging, {pq_table.num_rows} rows were written at {data_path}")
                if not keep_source_files:
                    logger.info('Removing source files')
                    logger.debug(f'Removing these files {file_paths}')
                    S3Utils.delete_objects(
                        boto_s3_client=boto_s3_client,
                        bucket_name=parquet_file_location.source_bucket,
                        to_delete=file_paths,
                        logger=logger
                    )
            except Exception:
                logger.exception(f'Caught error when trying to merge parquet files: {file_paths}')
                raise

            # Explicitly clear data from memory
            del pq_table
            gc.collect()

        if num_rows == 0:
            logger.warning(f"No files found at {data_path}, nothing to merge")

        return num_rows

    @staticmethod
    def s3_merge_files(boto3_session: boto3.Session, parquet_file_location: ParquetFileLocation,
                       logger: loguru.Logger) -> int:
        """
        Merge many small parquet files into one larger parquet file. From source to destination.
        Exception will be raised if source is equals to destination.

        :param boto3_session: Boto3 session
        :param parquet_file_location: ParquetFileLocation contains info about the files location in the s3 bucket
        :param logger: The logger
        :return: Number of rows in the parquet file
        """
        source_bucket = parquet_file_location.source_bucket
        source_prefix = parquet_file_location.source_prefix
        remove_files_at_destination = parquet_file_location.remove_files_at_destination

        ParquetUtils._source_and_destination_not_same(parquet_file_location)

        source_data_path = f"s3://{parquet_file_location.source_bucket}/{parquet_file_location.source_prefix}"
        destination_data_path = f"s3://{parquet_file_location.destination_bucket}/{parquet_file_location.destination_prefix}"

        logger.info(f"Merging files from {source_data_path} to {destination_data_path},"
                    f" compression: {parquet_file_location.compression}, "
                    f"remove_files_at_destination={parquet_file_location.remove_files_at_destination}")

        # check if there are any files present
        s3_client = boto3_session.client('s3')
        file_paths = S3Utils.file_paths_in_prefix(boto_s3_client=s3_client,
                                                  bucket_name=source_bucket,
                                                  prefix=source_prefix,
                                                  logger=logger)
        if len(file_paths) == 0:
            logger.warning(f"No files found at {source_data_path}, nothing to merge")
            return 0

        if remove_files_at_destination:
            ParquetUtils._remove_files(parquet_file_location, destination_data_path, logger, s3_client)

        logger.debug(f"Reading data from {source_data_path}")
        # this is a bit of hack, one should probably find a better way to do this
        botoc_session = boto3_session._session  # pylint: disable=protected-access
        aio_session = AioSession(session_vars=botoc_session.session_var_map) # type: ignore
        f_s = s3fs.S3FileSystem(session=aio_session)
        full_s3_paths = [f's3://{source_bucket}/{file_path["Key"]}' for file_path in file_paths]
        pq_table = pq.read_table(full_s3_paths, filesystem=f_s, partitioning=None) # type: ignore
        logger.debug(f"Shape of the table {pq_table.shape}")

        try:
            logger.debug(f"Writing to the destination {destination_data_path}")
            pq.write_to_dataset(pq_table,
                                destination_data_path,
                                filesystem=f_s,
                                compression=parquet_file_location.compression
            )

            logger.info(f"Done merging, {pq_table.num_rows} rows were written at {destination_data_path}")
            if not parquet_file_location.keep_source_files:
                logger.info('Removing source files')
                logger.debug(f'Removing these files {file_paths}')
                S3Utils.delete_objects(
                    boto_s3_client=s3_client,
                    bucket_name=source_bucket,
                    to_delete=file_paths,
                    logger=logger
                )
        except Exception:
            logger.exception(f'Caught error when trying to merge parquet files: {file_paths}')
            raise

        return pq_table.num_rows

    @staticmethod
    def _remove_files(parquet_file_location, destination_data_path, logger, s3_client):
        """removes files at the destination bucket, assigned in the parquet_file_location"""
        logger.debug(f"Removing all files at {destination_data_path}")
        S3Utils.delete_objects_by_prefix(boto_s3_client=s3_client, bucket_name=parquet_file_location.destination_bucket,
                                         prefix=parquet_file_location.destination_prefix, logger=logger)

    @staticmethod
    def _source_and_destination_not_same(parquet_file_location):
        """checks that source bucket and destination bucket is not the same"""
        if parquet_file_location.source_bucket == parquet_file_location.destination_bucket and \
                parquet_file_location.source_prefix.rstrip('/') == parquet_file_location.destination_prefix.rstrip('/'):
            raise ValueError('Source and destination cannot be the same!')
