from cubicweb.web.views.csvexport import CSVRsetView
from cubicweb.selectors import is_instance


class ScanCSVView(CSVRsetView):
    __regid__ = 'csvexport'
    title = _('csv export (entities)')
    __select__ = CSVRsetView.__select__ & is_instance('Scan')

    def call(self):
        req = self._cw
        values = {}
        questions = {}
        rows = [('"label"', '"filepath"')]
        for entity in self.cw_rset.entities():
            rows.append([entity.label, entity.full_filepath])
        writer = self.csvwriter()
        writer.writerows(rows)
