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


"""Services for '/summaries' endpoint."""

__version__ = '0.1.0'

import copy
import logging
from datetime import datetime
from typing import Dict, Any
from fastapi import BackgroundTasks
from jizt.config import LOG_LEVEL
from jizt.supported_languages import SupportedLanguage
from .pipeline.pipeline import SummarizationPipeline
from .data.summary_dao_singleton import SummaryDAOSingleton
from .models import PlainTextRequestSchema, Summary
from .utils.summary_status import SummaryStatus
from .utils.id_generation import generate_request_id, generate_summary_id

logging.basicConfig(
    format='%(asctime)s %(name)s %(levelname)-8s %(message)s',
    level=LOG_LEVEL,
    datefmt='%d/%m/%Y %I:%M:%S %p'
)
logger = logging.getLogger("SummaryService")
db = SummaryDAOSingleton()
summarization_pipeline = SummarizationPipeline()


def generate_summary(
    request: PlainTextRequestSchema,
    background_tasks: BackgroundTasks
) -> Dict[Summary, Dict[str, Any]]:
    """Generate summary.

    For info on the params, see :class:`models.PlainTextRequestSchema`.

    Returns:
        :obj:`Dict[Summary, Dict[str, Any]]`: a dictionary containing the
        summary and the warnings derived from the summary generation
        (:obj:`None` if there are no warnings).
    """
    source, model, params, language, cache = request.dict().values()

    request_id = generate_request_id(source, model, params)
    summary_id = generate_summary_id(source, model, params)
    if db.request_exists(request_id):
        summary, warnings = db.get_summary_by_request_id(request_id)
        count = db.increment_summary_count(request_id)
        logger.debug(
            f'Summary already exists: [id] {summary.id_}, [source] '
            f'{summary.source[:50]}, [output] '
            f'{summary.output[:50] if summary.output is not None else None}, '
            f'[model] {summary.model}, [params] {summary.params}, [status] '
            f'{summary.status}, [started_at] {summary.started_at}, [ended_at] '
            f'{summary.ended_at}, [language] {summary.language}'
        )
        logger.debug(f"Current summary count: {count}.")
    else:
        summary = Summary(
            id_=summary_id,
            source=source,
            output=None,
            model=model,
            params=params,
            status=SummaryStatus.PREPROCESSING,
            started_at=datetime.now(),
            ended_at=None,
            language=SupportedLanguage(language)
        )
        # TODO: warnings = data.pop('warnings', None)
        warnings = None
        db.insert_initial_request(request_id, summary, cache, warnings)
        logger.debug(
            f'New summary created: [id] {summary.id_}, [source] '
            f'{summary.source[:50]}, [output] '
            f'{summary.output[:50] if summary.output is not None else None}, '
            f'[model] {summary.model}, [params] {summary.params}, [status] '
            f'{summary.status}, [started_at] {summary.started_at}, [ended_at] '
            f'{summary.ended_at}, [language] {summary.language}'
        )
        background_tasks.add_task(
            summarization_pipeline.run,
            request_id,
            summary
        )
    summary = copy.copy(summary)  # TODO: remove (for now we store the summaries in memory)
    summary.id_ = request_id  # we return the request id
    return summary, warnings


def get_summary(request_id: str) -> Dict[Summary, Dict[str, Any]]:
    """Get a generated summary.

    Args:
        request_id (:obj:`str`):
            The id of the requested summary.

    Returns:
        :obj:`Dict[Summary, Dict[str, Any]]`: a dictionary containing the
        summary and the warnings derived from the summary generation
        (:obj:`None` if there are no warnings).
    """
    return db.get_summary_by_request_id(request_id)
