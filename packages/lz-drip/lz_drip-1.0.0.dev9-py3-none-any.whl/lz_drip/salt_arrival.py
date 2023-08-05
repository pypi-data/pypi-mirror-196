"""Define the SaltArrival class"""

from typing import List, Tuple

import logging

from drip import Dropper

from psquared_client import display, PSquared

from .bundle import find_bundles, Bundle
from .file_utils import (
    read_config,
    select_bypass,
    select_destination,
    select_nosalt,
    select_park,
    select_pipeline,
    select_source,
    select_threshold,
)
from .pipeline_db import PipelineDB
from .psquared_utils import (
    select_configuration,
    select_config_version,
    select_scheduler,
    select_url,
)


class SaltArrival(Dropper):  # pylint: disable=too-many-instance-attributes
    """
    This class provides the concrete implementation use by a Feeder
    instance to copy SPADE bundles from one directory into an area
    organized by their canonical path values.
    """

    def __init__(self, config_file: str, section: str):
        """
        Creates an instance of this class.

        Args:
            config_file: the Path to the configuration file.
            section: the section of the configuration file to use.
        """
        config = read_config(config_file, section)

        self.__src = select_source(config)
        self.__dst = select_destination(config)
        self.__nosalt = select_nosalt(config)
        self.__threshold = select_threshold(config)
        self.__bypass = select_bypass(config)
        self.__park = select_park(config)
        self.__pipeline = select_pipeline(config)
        if not self.__bypass or self.__pipeline:
            self.__pipeline_db = PipelineDB()
            url = select_url(config)
            self.__psquared = PSquared(url, dump=logging.DEBUG == logging.root.level)
            self.__psquared_configuration = select_configuration(config)
            self.__config_version = select_config_version(config)
            self.__scheduler = select_scheduler(config)
        logging.debug("Begin SaltArrival configuration:")
        logging.debug("    %s = %s", "source", self.__src)
        logging.debug("    %s = %s", "destination", self.__dst)
        logging.debug("    %s = %s", "salt bypass destination", self.__nosalt)
        logging.debug("    %s = %s", "threshold", self.__threshold)
        logging.debug("    %s = %s", "bypass salting", self.__bypass)
        if self.__pipeline:
            logging.debug(
                "    %s = %s",
                "park bundles, during bypass",
                '(superseded by "pipeline=True")',
            )
        else:
            logging.debug("    %s = %s", "park bundles, during bypass", self.__park)
        logging.debug("    %s = %s", "pipline bundles, during bypass", self.__pipeline)
        if not self.__bypass or self.__pipeline:
            logging.debug("  Begin PSquared configuration:")
            logging.debug("      %s = %s", "url", url)
            logging.debug(
                "      %s = %s", "configuration", self.__psquared_configuration
            )
            logging.debug("      %s = %s", "version", self.__config_version)
            logging.debug("      %s = %s", "scheduler", self.__scheduler)
            logging.debug("  End PSquared configuration:")
        logging.debug("End SaltArrival configuration:")

    def after_dropping(self) -> None:
        """
        Called after a set of `drop` calls.
        """
        if not self.__bypass or self.__pipeline:
            self.__pipeline_db.end_transaction()

    def assess_condition(self) -> Tuple[int, str]:
        """
        Assess whether a drip should be executed or not.

        Returns:
            The maximum number if items that can be dropped and an
                explanation of any limitations.
        """
        return self.__threshold, ""

    def before_dropping(self, count: int) -> None:
        """
        Called before a set of `drop` calls.

        Args:
            count: the number of `drop` calls that will be made in
                the set.
        """
        if not self.__bypass or self.__pipeline:
            self.__pipeline_db.begin_transaction()

    def drop(self, item) -> None:
        """
        "Drops" the supplied item, i.e. acts on that item.

        Args:
            item: The item to be dropped.
        """
        if not self.__bypass or self.__pipeline:
            # Only record bundles that will be processed.
            if not self.__pipeline_db.bundle_entry(
                item.name(),
                str(item.canonical_path()),
                item.data_name(),
                item.metadata_name(),
                item.done_name(),
            ):
                logging.warning('Bundle "%s" can not enter pipeline, so not moved')
                return

        if self.__bypass:
            item.move(self.__nosalt)
        if not self.__bypass or self.__park or self.__pipeline:
            item.move_to_canonical(self.__dst)
            self._submit_salt_process(item)

    def fill_cache(self) -> List[Bundle]:
        """
        Fills a List with the current set of bundles to be moved.

        Returns:
            The new list of bundles to be moved.
        """
        return find_bundles(self.__src)

    def _submit_salt_process(self, bundle: Bundle) -> None:
        """
        Submits the supplied file to be processed by the Salting Service.

        Args:
            item: The path to the file to be processed by the Salting
                Service.
        """
        if self.__bypass and not self.__pipeline:
            return
        name = bundle.name()
        logging.debug('Submitting "%s" to PSquared', name)
        items = []
        items.append(name)
        report, version = self.__psquared.submit_items(
            self.__psquared_configuration,
            self.__config_version,
            items,
            scheduler=self.__scheduler,
        )
        if None is version:
            raise ValueError("No valid version was found")
        if None is not report:
            display.info(self.__psquared_configuration, version, report, items)
