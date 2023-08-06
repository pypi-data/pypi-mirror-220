# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------
from azureml.dataprep import DataPrepException, UserErrorException


_DATAPREP_EXECEPTION_USER_ERROR_CODES = ('ScriptExecution.StreamAccess.Validation',
                                         'ScriptExecution.StreamAccess.NotFound',
                                         'ScriptExecution.StreamAccess.Authentication',
                                         'ScriptExecution.DatabaseQuery',
                                         'ScriptExecution.Database.TypeMismatch',
                                         'ScriptExecution.Validation',
                                         'ScriptExecution.DatabaseConnection.Authentication',
                                         'ScriptExecution.DatabaseConnection',
                                         'ScriptExecution.Database.TypeMismatch',
                                         'ScriptExecution.WriteStreams.NotFound',
                                         'ScriptExecution.WriteStreams.Authentication',
                                         'ScriptExecution.WriteStreams.Validation',
                                         'ScriptExecution.WriteStreams.AlreadyExists',
                                         'ScriptExecution.Transformation.Validation')


_RSLEX_USER_ERROR_VALUES = ('Microsoft.DPrep.ErrorValues.SourceFileNotFound',
                            'Microsoft.DPrep.ErrorValues.SourceFilePermissionDenied',
                            'Microsoft.DPrep.ErrorValues.InvalidArgument',
                            'Microsoft.DPrep.ErrorValues.ValueWrongKind',
                            'Microsoft.DPrep.ErrorValues.SourcePermissionDenied',
                            'Microsoft.DPrep.ErrorValues.DestinationPermissionDenied',
                            'Microsoft.DPrep.ErrorValues.DestinationDiskFull',
                            'Microsoft.DPrep.ErrorValues.FileSizeChangedWhileDownloading',
                            'Microsoft.DPrep.ErrorValues.StreamInfoInvalidPath',
                            'Microsoft.DPrep.ErrorValues.NoManagedIdentity',
                            'Microsoft.DPrep.ErrorValues.NoOboEndpoint',
                            'Microsoft.DPrep.ErrorValues.StreamInfoRequired')


_RSLEX_USER_ERROR_MSGS = ('InvalidUriScheme',
                          'StreamError(NotFound)',
                          'DataAccessError(NotFound)',
                          'No such host is known',
                          'No identity was found on compute',
                          'Make sure uri is correct',
                          'Invalid JSON in log record',
                          'Invalid table version',
                          'stream did not contain valid UTF-8',
                          'Got unexpected error: invalid data. Kind(InvalidData)',
                          'Only one of version or timestamp can be specified but not both.',
                          'The requested stream was not found. Please make sure the request uri is correct.',
                          'stream did not contain valid UTF-8',
                          'Authentication failed when trying to access the stream',
                          'Unable to find any delta table metadata',
                          'Range requested from the service is invalid for current stream.',
                          'Invalid Parquet file.',
                          'DataAccessError(PermissionDenied)',
                          'OutputError(NotEmpty)',
                          'DestinationError(NotEmpty)')


def _validate_downloads(download_records, ignore_not_found, logger):
    if not download_records:
        return []

    from azureml.dataprep.native import StreamInfo, DataPrepError
    downloaded_files = []
    errors = []
    for record in download_records:
        value = record['DestinationFile']
        if isinstance(value, StreamInfo):
            downloaded_files.append(value.resource_identifier)
        elif isinstance(value, DataPrepError):
            resource_identifier = value.originalValue
            error_code = value.errorCode
            if ignore_not_found and error_code == 'Microsoft.DPrep.ErrorValues.SourceFileNotFound':
                logger.warning(f"'{resource_identifier}' hasn't been downloaded as it was not present at the source. \
                               Download is proceeding.")
            else:
                errors.append((resource_identifier, error_code))
        else:
            raise RuntimeError(f'Unexpected error during file download: {value}')

    if errors:
        _download_error_handler(errors)
    return downloaded_files


def _download_error_handler(errors):
    non_user_errors = [error for error in errors if error[1] not in _RSLEX_USER_ERROR_VALUES]
    if non_user_errors:
        raise RuntimeError(f'System errors occured during downloading: {non_user_errors}')
    errors = '\n'.join(map(str, errors))
    raise UserErrorException(f'Some files have failed to download: {errors}')


def _reclassify_rslex_error(err):
    """
    Reclassifies some errors from outside of MLTable into UserErrorExceptions or RuntimeErrors.
    """
    if isinstance(err, (UserErrorException, RuntimeError)):  # just a safety net
        raise err

    err_msg = err.args[0]
    # first check remaps errors from RSlex to UserErrorExceptions in following ways:
    # - is a DataPrepException whose error_code attribute is in _DATAPREP_EXECEPTION_USER_ERROR_CODES or whose message
    #   attribute contains am error value in _RSLEX_USER_ERROR_VALUES
    # - error message contains any element in _RSLEX_USER_ERROR_MSGS
    if ((isinstance(err, DataPrepException) or hasattr(err, 'error_code'))
        and err.error_code in _DATAPREP_EXECEPTION_USER_ERROR_CODES) \
            or any(user_err_msg in err_msg for user_err_msg in _RSLEX_USER_ERROR_MSGS) \
            or (isinstance(err, DataPrepException)
                and any(user_error_value in err.message for user_error_value in _RSLEX_USER_ERROR_VALUES)):
        raise UserErrorException(err)
    if 'Python expression parse error' in err_msg:
        raise UserErrorException(f'Not a valid python expression in filter. {err_msg}')
    if 'ExecutionError(StreamError(PermissionDenied' in err_msg:
        raise UserErrorException(
            f'Getting permission error please make sure proper access is configured on storage: {err_msg}')
    raise RuntimeError(err_msg)


def _wrap_rslex_function_call(func):
    """
    Maps Exceptions from the calling RSlex function to a UserErrorException or RuntimeError based on error context.
    """
    try:
        return func()
    except Exception as e:
        _reclassify_rslex_error(e)
