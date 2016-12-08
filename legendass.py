from PySide.QtGui import *
import MaxPlus

import legendass_boundaries
import legendass_controlers

import legendass_entities as ll

reload(legendass_boundaries)

ui = legendass_controlers.MainWidget()
dd = legendass_boundaries.LegendassNode(ui)


app = QApplication.instance()
if not app:
    app = QApplication([])

if __name__ == '__main__':
    MaxPlus.AttachQWidgetToMax(dd.implementation)
    print 'dsdsd'
    dd.implementation.show()
    app.exec_()
