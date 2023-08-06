# Copyright CNRS/Inria/UCA
# Contributor(s): Eric Debreuve (since 2021)
#
# eric.debreuve@cnrs.fr
#
# This software is governed by the CeCILL  license under French law and
# abiding by the rules of distribution of free software.  You can  use,
# modify and/ or redistribute the software under the terms of the CeCILL
# license as circulated by CEA, CNRS and INRIA at the following URL
# "http://www.cecill.info".
#
# As a counterpart to the access to the source code and  rights to copy,
# modify and redistribute granted by the license, users are provided only
# with a limited warranty  and the software's author,  the holder of the
# economic rights,  and the successive licensors  have only  limited
# liability.
#
# In this respect, the user's attention is drawn to the risks associated
# with loading,  using,  modifying and/or developing or reproducing the
# software by the user in light of its specific status of free software,
# that may mean  that it is complicated to manipulate,  and  that  also
# therefore means  that it is reserved for developers  and  experienced
# professionals having in-depth computer knowledge. Users are therefore
# encouraged to load and test the software's suitability as regards their
# requirements in conditions enabling the security of their systems and/or
# data to be ensured and,  more generally, to use and operate it in the
# same conditions as regards security.
#
# The fact that you are presently reading this means that you have had
# knowledge of the CeCILL license and that you accept its terms.

import wtforms as wtfm
from si_fi_o.session.form import form_t as base_form_t

from flask import request as flask_request

_TO_BYTE_STREAM = "to byte stream"
_TO_ARRAY = "to array"


class form_t(base_form_t):
    """"""

    array = wtfm.FileField(label="Piecewise-constant Array")
    stream = wtfm.TextAreaField(label="Byte Stream", render_kw={"cols": 75, "rows": 3})
    submit_to_str = wtfm.SubmitField(
        label="Convert to Byte Stream", name=_TO_BYTE_STREAM
    )
    submit_to_ary = wtfm.SubmitField(
        label="Convert to Piecewise-constant Array", name=_TO_ARRAY
    )

    @staticmethod
    def RequestedToByteStream() -> bool:
        """"""
        # FIXME: Find a better way to guess targeted conversion
        return _TO_BYTE_STREAM in flask_request.form
