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

from si_fi_o.session.form import file_t
from si_fi_o.session.session import session_t as base_session_t

from pca_b_stream.flask.session.form import form_t


class session_t(base_session_t):
    # additional_paths: list[path_t] | None = None
    #
    # def DeleteOutputsFile(self) -> None:
    #     """"""
    #     super().DeleteOutputsFile()
    #
    #     if self.additional_paths is not None:
    #         for path in self.additional_paths:
    #             if path.is_file():
    #                 path.unlink()
    #         self.additional_paths = None

    def IsComplete(self, *, form: form_t = None) -> bool:
        """"""
        # Do not use self[_key] below since reference and/or detection files are missing if the form has been submitted
        # without these files (they are not required fields since the session can supply them) and the session has not
        # received these files yet, e.g. on the first run if not selecting these files.
        if form_t.RequestedToByteStream():
            return isinstance(self.get("array"), file_t)

        return self["stream"].__len__() > 0
