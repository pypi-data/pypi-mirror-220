import logging
import time
from itertools import pairwise, chain
from typing import TypeVar

from th2_common.schema.event.event_batch_router import EventBatchRouter
from th2_common.schema.factory.common_factory import CommonFactory
from th2_common_utils import create_event, create_event_id
from th2_grpc_common.common_pb2 import EventBatch

from run_one.action_handlers.abstract_action_handler import AbstractActionHandler
from run_one.action_handlers.context import Context
from run_one.processors.abstract_processor import AbstractProcessor
from run_one.util.config import Config
from run_one.util.util import Action


class Th2ProcessorConfig:
    def __init__(self, **kwargs) -> None:

        self.th2_configs = 'th2_configs'
        if 'th2_configs' in kwargs:
            self.th2_configs = kwargs['th2_configs']

        self.book = 'book'
        if 'book' in kwargs:
            self.book = kwargs['book']

        self.scope = 'scope'
        if 'scope' in kwargs:
            self.scope = kwargs['scope']

        self.use_place_method = False
        if 'use_place_method' in kwargs:
            self.use_place_method = bool(kwargs['use_place_method'])

        self.key_fields = []
        if 'key_fields' in kwargs:
            self.key_fields = kwargs['key_fields']

        self.sleep = 0
        if 'sleep' in kwargs:
            self.sleep = int(kwargs['sleep'])


class Th2Processor(AbstractProcessor):
    def __init__(self, config: Config, processor_config_class=Th2ProcessorConfig):
        self._config = processor_config_class(**config.processor_config)

        self._common_factory = CommonFactory(config_path=self._config.th2_configs)

        self._event_router: EventBatchRouter = self._common_factory.event_batch_router  # type: ignore
        self.root_event_id = create_event_id(book_name=self._config.book, scope=self._config.scope)
        self.root_event = EventBatch(events=[create_event(name='Run One Root Event',
                                                          event_id=self.root_event_id)])
        self._event_router.send(self.root_event)
        Context.set('root_event_id', self.root_event_id)

        self._grpc_router = self._common_factory.grpc_router

        HandlerType = TypeVar('HandlerType', bound=AbstractActionHandler)
        action_handlers = self.load_action_handlers(config.processed_actions)
        class_instance_mapping = {x: x(self._config, self._grpc_router) for x in set(action_handlers.values())}
        self.processed_actions: dict[str, HandlerType] = {action: class_instance_mapping[action_handler]
                                                          for action, action_handler in action_handlers.items()}

        self.logger = logging.getLogger()

    def process(self, test_cases: dict[str, list[Action]]):

        for test_case_name, actions in test_cases.items():

            logging.info(f'Processing {test_case_name} test case')

            test_case_root_event_id = create_event_id(book_name=self._config.book, scope=self._config.scope)
            test_case_event_batch = EventBatch(events=[create_event(name=test_case_name,
                                                                    event_id=test_case_root_event_id,
                                                                    parent_id=self.root_event_id)])
            self._event_router.send(test_case_event_batch)
            Context.set('parent_event_id', test_case_root_event_id)

            for previous_action, current_action in pairwise(chain([None], actions)):

                current_action_type = current_action.extra_data['Action']

                self.logger.info(f'Processing {current_action_type} action '
                                 f'with ID = {current_action.extra_data.get("ID", "empty")}, '
                                 f'message type = {current_action.extra_data.get("MessageType", "none")},'
                                 f'description = {current_action.extra_data.get("Description", "empty")}')

                current_action_handler = self.processed_actions.get(current_action_type)

                if previous_action is not None:
                    previous_action_handler = self.processed_actions.get(previous_action.extra_data['Action'])
                    if current_action_handler is not previous_action_handler:
                        previous_action_handler.on_action_change(previous_action, current_action)

                if current_action_handler is not None:
                    current_action_handler.process(action=current_action)

                time.sleep(self._config.sleep)

            for handler in self.processed_actions.values():
                handler.on_test_case_end()

            Context.clear()

    def close(self):
        self._common_factory.close()
