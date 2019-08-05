import os
import string
import random
import logging
import datetime

# DEFAULT_DIRECTORY = output_directory = os.path.join(os.getenv('APPDATA'),
#                                                     os.path.basename(os.path.dirname(os.path.realpath(__file__))))
#
#
# def init_logging(output_directory=DEFAULT_DIRECTORY,
#                  script_alias=''.join(random.choice(string.ascii_lowercase) for x in range(6)),
#                  log_level='INFO',
#                  log_time_format='%Y%m%d%H%M%S%f',
#                  start_time=datetime.datetime.now()):
#     # directory of python file
#     timestamp = start_time.strftime(log_time_format)
#
#     # create log directory path and check path exists
#     log_directory = os.path.join(output_directory,
#                                  script_alias)
#     if output_directory != DEFAULT_DIRECTORY:
#         log_directory = os.path.join(output_directory,
#                                      '%s-resources%slog' % (script_alias,
#                                                             os.sep))
#
#     if not os.path.isdir(log_directory):
#         os.makedirs(log_directory)
#
#     log_file_path = os.path.join(log_directory,
#                                  '%s_%s.log' % (script_alias,
#                                                 timestamp))
#
#     print 'LOGGING AT: %s' % log_file_path
#
#     # setup log
#     logging.basicConfig(filename=log_file_path,
#                         level=log_level,
#                         format='%(asctime)s.%(msecs)03d %(levelname)s:%(message)s',
#                         datefmt='%Y-%m-%d %H:%M:%S', )
#     logging.info('START TIME: %s' % start_time)
#
#     return log_file_path
#
#
# def end_logging(start_time):
#     END_TIME = datetime.datetime.now()
#     DURATION = (END_TIME - start_time)
#     logging.info('END_TIME: %s' % END_TIME)
#     logging.info('DURATION: %s' % DURATION)
#
#
# def Test(start_time):
#     init_logging()
#     terminate(start_time)

