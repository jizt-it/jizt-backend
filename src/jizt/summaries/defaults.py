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

"""Default summarization parameters."""

__version__ = '0.1.3'

from pydantic import BaseModel
from typing import Optional


class T5DefaultParams(BaseModel):
    """T5 Model default summarization parameters.

    For the attributes, see
    :class:`jizt.summaries.pipeline.text_summarization.summarization.Summarizer`.
    """

    # The max length of the summary will be at most # this percentage of the
    # source length.
    relative_max_length: Optional[float] = 0.4
    # Same for the min length
    relative_min_length: Optional[float] = 0.1
    do_sample: Optional[bool] = True
    early_stopping: Optional[bool] = None
    num_beams: Optional[int] = 4
    temperature: Optional[float] = None
    top_k: Optional[int] = None
    top_p: Optional[float] = None
    repetition_penalty: Optional[float] = None
    length_penalty: Optional[float] = None
    no_repeat_ngram_size: Optional[int] = 4


class SummarizationDefaults(BaseModel):
    """Class containing the default summarization parameters.

    Attributes:
        model_params (:obj:`BaseModel`, `optional`, defaults to :obj:`T5DefaultParams`):
            The default parameters of the summarization model.
        min_words_source (:obj:`int`):
            The minimum number of words a text has to have to be summarized. This
            prevents trying to summarize very short texts, which will yield bad
            results.
    """

    model_params: BaseModel = T5DefaultParams()
    min_words_source: int = 20
