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

from datetime import datetime
from .schemas import Summary
from .utils.supported_models import SupportedModel
from .utils.supported_languages import SupportedLanguage
from .utils.summary_status import SummaryStatus
from typing import Dict, Any

# TODO: Implement
MOCK_SUMMARY = Summary(
    id_="12345",
    source="The source.",
    output="The output.",
    model=SupportedModel.T5_LARGE,
    params={},
    status=SummaryStatus.PREPROCESSING,
    started_at=datetime.now(),
    ended_at=None,
    language=SupportedLanguage.ENGLISH
)

# TODO: Implement
MOCK_WARNINGS = {
    "warnings": {
        "top_k": ["example warning"]
    }
}



def generate_summary(
    source: str,
    model: str,
    params: dict,
    language: str,
    cache: dict
) -> Dict[Summary, Dict[str, Any]]:
    """Generate summary.

    For info on the params, see :class:`schemas.PlainTextRequestSchema`.

    Returns:
        :obj:`Dict[Summary, Dict[str, Any]]`: a dictionary containing the
        summary and the warnings derived from the summary generation
        (:obj:`None` if there are no warnings).
    """
    MOCK_WARNINGS.update(
        {"source": source,
        "model": model,
        "params": params,
        "language": language,
        "cache": cache}
    )
    return MOCK_SUMMARY, MOCK_WARNINGS


def get_summary(summary_id: str) -> Dict[Summary, Dict[str, Any]]:
    """Get a generated summary.

    Args:
        summary_id (:obj:`str`):
            The id of the requested summary.

    Returns:
        :obj:`Dict[Summary, Dict[str, Any]]`: a dictionary containing the
        summary and the warnings derived from the summary generation
        (:obj:`None` if there are no warnings).
    """
    return MOCK_SUMMARY, MOCK_WARNINGS
