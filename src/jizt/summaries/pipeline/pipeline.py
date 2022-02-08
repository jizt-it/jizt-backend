# Copyright (C) 2020-2021 Diego Miguel Lozano <contact@jizt.it>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.
#
# For license information on the libraries used, see LICENSE.

"""Summarization pipeline."""

import logging
from datetime import datetime
from .text_processing.preprocessing import TextPreprocessor
from .text_encoding.encoding import SplitterEncoder
from .text_summarization.summarization import Summarizer
from .text_processing.postprocessing import TextPostprocessor
from ..data.summary_dao_singleton import SummaryDAOSingleton
from ..models import Summary
from ..utils.id_generation import generate_summary_id
from ..utils.summary_status import SummaryStatus
from jizt.config import LOG_LEVEL


class SummarizationPipeline:
    """Summarization pipeline.

    This class takes care of the different summarization steps. It also updates
    the summaries stored in the database.

    Args:
    #TODO
    """

    def __init__(self, log_level: int = LOG_LEVEL):
        logging.basicConfig(
            format='%(asctime)s %(name)s %(levelname)-8s %(message)s',
            level=log_level,
            datefmt='%d/%m/%Y %I:%M:%S %p'
        )
        self.logger = logging.getLogger("SummaryDAOPostgresql")
        self.db = SummaryDAOSingleton()
        self.text_preprocessor = TextPreprocessor()
        self.encoder = SplitterEncoder()
        self.summarizer = Summarizer()
        self.text_postprocessor = TextPostprocessor()

    def run(self, request_id: str, summary: Summary):
        """#TODO: document."""
        preprocessed_text = self.text_preprocessor.preprocess(summary.source)
        new_summary_id = generate_summary_id(preprocessed_text, summary.model,
                                             summary.params)
        self.db.update_source(summary.source, preprocessed_text,
                              summary.id_, new_summary_id)
        self.db.update_summary(request_id, status=SummaryStatus.ENCODING.value)
        encoded_text = self.encoder.encode(preprocessed_text)
        self.db.update_summary(request_id, status=SummaryStatus.SUMMARIZING.value)
        raw_summary = self.summarizer.summarize(
            encoded_text,
            **summary.params
        )
        self.db.update_summary(request_id, status=SummaryStatus.POSTPROCESSING.value)
        summary = self.text_postprocessor.postprocess(raw_summary)
        self.db.update_summary(
            request_id,
            status=SummaryStatus.COMPLETED.value,
            output=summary,
            output_length=len(summary),
            ended_at=datetime.now()
        )
