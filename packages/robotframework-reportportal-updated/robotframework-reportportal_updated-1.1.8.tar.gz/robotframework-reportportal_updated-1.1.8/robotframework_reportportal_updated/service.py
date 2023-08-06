"""This module is a Robot service for reporting results to Report Portal."""

#  Copyright (c) 2023 EPAM Systems
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#  https://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License

from dateutil.parser import parse
import logging

from reportportal_client.logs.log_manager import MAX_LOG_BATCH_PAYLOAD_SIZE
from reportportal_client.helpers import (
    dict_to_payload,
    get_launch_sys_attrs,
    get_package_version,
    timestamp
)
from reportportal_client.client import RPClient

from .exception import RobotServiceException
from .static import LOG_LEVEL_MAPPING, STATUS_MAPPING

logger = logging.getLogger(__name__)

TOP_LEVEL_ITEMS = {'BEFORE_SUITE', 'AFTER_SUITE'}


def to_epoch(date):
    """Convert Robot Framework timestamp to UTC timestamp."""
    if not date:
        return None
    try:
        parsed_date = parse(date)
    except ValueError:
        return None
    if hasattr(parsed_date, 'timestamp'):
        epoch_time = parsed_date.timestamp()
    else:
        epoch_time = \
            float(parsed_date.strftime('%s')) + parsed_date.microsecond / 1e6
    return str(int(epoch_time * 1000))


class RobotService(object):
    """Class represents service that sends Robot items to Report Portal."""

    def __init__(self):
        """Initialize service attributes."""
        self.agent_name = 'robotframework-reportportal'
        self.agent_version = get_package_version(self.agent_name)
        self.rp = None
        self.launch_id = None

    def _get_launch_attributes(self, cmd_attrs):
        """Generate launch attributes including both system and user ones.

        :param list cmd_attrs: List for attributes from the command line
        """
        attributes = cmd_attrs or []
        system_attributes = get_launch_sys_attrs()
        system_attributes['agent'] = (
            '{}|{}'.format(self.agent_name, self.agent_version))
        return attributes + dict_to_payload(system_attributes)

    def init_service(self, endpoint, project, api_key, log_batch_size,
                     pool_size, skipped_issue=True, verify_ssl=True,
                     log_batch_payload_size=MAX_LOG_BATCH_PAYLOAD_SIZE,
                     launch_id=None):
        """Initialize common Report Portal client.

        :param endpoint:               Report Portal API endpoint
        :param project:                Report Portal project
        :param api_key:                API key
        :param log_batch_size:         Number of logs to be sent within one
                                       batch
        :param pool_size:              HTTPAdapter max pool size
        :param skipped_issue:          Mark skipped test items with
                                       'To Investigate', default value 'True'
        :param verify_ssl:             Disable SSL verification.
        :param log_batch_payload_size: Maximum size of logs to be sent within
                                       one batch
        :param launch_id:              a launch id to use instead of starting
                                       own one
        """
        if self.rp is None:
            logger.debug(
                'ReportPortal - Init service: '
                'endpoint={0}, project={1}, api_key={2}'
                .format(endpoint, project, api_key))
            self.launch_id = launch_id
            self.rp = RPClient(
                endpoint=endpoint,
                project=project,
                api_key=api_key,
                is_skipped_an_issue=skipped_issue,
                log_batch_size=log_batch_size,
                retries=True,
                verify_ssl=verify_ssl,
                max_pool_size=pool_size,
                log_batch_payload_size=log_batch_payload_size,
                launch_id=launch_id
            )
            self.rp.start()
        else:
            raise RobotServiceException(
                'RobotFrameworkService is already initialized.')

    def terminate_service(self):
        """Terminate common reportportal client."""
        if self.rp is not None:
            self.rp.terminate()

    def start_launch(self, launch, mode=None, rerun=False, rerun_of=None,
                     ts=None):
        """Call start_launch method of the common client.

        :param launch:         Instance of the Launch class
        :param mode:           Launch mode
        :param rerun:          Rerun mode. Allowable values 'True' of 'False'
        :param rerun_of:       Rerun mode. Specifies launch to be re-runned.
                               Should be used with the 'rerun' option.
        :param ts:             Start time
        :return:               launch UUID
        """
        sl_pt = {
            'attributes': self._get_launch_attributes(launch.attributes),
            'description': launch.doc,
            'name': launch.name,
            'mode': mode,
            'rerun': rerun,
            'rerun_of': rerun_of,
            'start_time': ts or to_epoch(launch.start_time) or timestamp()
        }
        logger.debug(
            'ReportPortal - Start launch: request_body={0}'.format(sl_pt))
        return self.rp.start_launch(**sl_pt)

    def finish_launch(self, launch, ts=None):
        """Finish started launch.

        :param launch: Launch name
        :param ts:     End time
        """
        fl_rq = {
            'end_time': ts or to_epoch(launch.end_time) or timestamp(),
            'status': STATUS_MAPPING[launch.status]
        }
        logger.debug(
            'ReportPortal - Finish launch: request_body={0}'.format(fl_rq))
        if self.launch_id is None:
            self.rp.finish_launch(**fl_rq)

    def start_suite(self, suite, ts=None):
        """Call start_test method of the common client.

        :param suite: model.Suite object
        :param ts:    Start time
        :return:      Suite UUID
        """
        start_rq = {
            'attributes': None,
            'description': suite.doc,
            'item_type': suite.type,
            'name': suite.name,
            'parent_item_id': suite.rp_parent_item_id,
            'start_time': ts or to_epoch(suite.start_time) or timestamp()
        }
        logger.debug(
            'ReportPortal - Start suite: request_body={0}'.format(start_rq))
        return self.rp.start_test_item(**start_rq)

    def finish_suite(self, suite, issue=None, ts=None):
        """Finish started suite.

        :param suite: Instance of the started suite item
        :param issue: Corresponding issue if it exists
        :param ts:    End time
        """
        fta_rq = {
            'end_time': ts or to_epoch(suite.end_time) or timestamp(),
            'issue': issue,
            'item_id': suite.rp_item_id,
            'status': STATUS_MAPPING[suite.status]
        }
        logger.debug(
            'ReportPortal - Finish suite: request_body={0}'.format(fta_rq))
        self.rp.finish_test_item(**fta_rq)

    def start_test(self, test, ts=None):
        """Call start_test method of the common client.

        :param test: model.Test object
        :param ts:   Start time
        """
        # Item type should be sent as "STEP" until we upgrade to RPv6.
        # Details at:
        # https://github.com/reportportal/agent-Python-RobotFramework/issues/56
        start_rq = {
            'attributes': test.attributes,
            'code_ref': test.code_ref,
            'description': test.doc,
            'item_type': 'STEP',
            'name': test.name,
            'parent_item_id': test.rp_parent_item_id,
            'start_time': ts or to_epoch(test.start_time) or timestamp(),
            'test_case_id': test.test_case_id
        }
        logger.debug(
            'ReportPortal - Start test: request_body={0}'.format(start_rq))
        return self.rp.start_test_item(**start_rq)

    def finish_test(self, test, issue=None, ts=None):
        """Finish started test case.

        :param test:  Instance of started test item
        :param issue: Corresponding issue if it exists
        :param ts:    End time
        """
        fta_rq = {
            'attributes': test.attributes,
            'end_time': ts or to_epoch(test.end_time) or timestamp(),
            'issue': issue,
            'item_id': test.rp_item_id,
            'status': STATUS_MAPPING[test.status]
        }
        logger.debug(
            'ReportPortal - Finish test: request_body={0}'.format(fta_rq))
        self.rp.finish_test_item(**fta_rq)

    def start_keyword(self, keyword, ts=None):
        """Call start_test method of the common client.

        :param keyword: model.Keyword object
        :param ts:      Start time
        """
        start_rq = {
            'description': keyword.doc,
            'has_stats': keyword.get_type() in TOP_LEVEL_ITEMS,
            'item_type': keyword.get_type(),
            'name': keyword.get_name(),
            'parent_item_id': keyword.rp_parent_item_id,
            'start_time': ts or to_epoch(keyword.start_time) or timestamp()
        }
        logger.debug(
            'ReportPortal - Start keyword: request_body={0}'.format(start_rq))
        return self.rp.start_test_item(**start_rq)

    def finish_keyword(self, keyword, issue=None, ts=None):
        """Finish started keyword item.

        :param keyword: Instance of started keyword item
        :param issue:   Corresponding issue if it exists
        :param ts:      End time
        """
        fta_rq = {
            'end_time': ts or to_epoch(keyword.end_time) or timestamp(),
            'issue': issue,
            'item_id': keyword.rp_item_id,
            'status': STATUS_MAPPING[keyword.status]
        }
        logger.debug(
            'ReportPortal - Finish keyword: request_body={0}'.format(fta_rq))
        self.rp.finish_test_item(**fta_rq)

    def log(self, message, ts=None):
        """Send log message to Report Portal.

        :param message: model.LogMessage object
        :param ts:      Timestamp
        """
        sl_rq = {
            'attachment': message.attachment,
            'item_id': message.item_id,
            'level': LOG_LEVEL_MAPPING.get(message.level, 'INFO'),
            'message': message.message,
            'time': ts or timestamp()
        }
        self.rp.log(**sl_rq)
