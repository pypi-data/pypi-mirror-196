from PyQt5 import QtWidgets
from oasys.menus.menu import OMenu

from orangecanvas.scheme.link import SchemeLink

class HALFSRWToolsMenu(OMenu):

    def __init__(self):
        super().__init__(name="HALF-SRW Tools")

        self.openContainer()
        self.addContainer("HALF-SRW")
        self.addSubMenu("HALF-SRW Tool 1")
        self.addSubMenu("HALF-SRW Tool 2")
        self.addSeparator()
        self.addSubMenu("HALF-SRW Tool 3")
        self.closeContainer()

    def executeAction_1(self, action):
        self.showWarningMessage("HALF-SRW Tool 1")

    def executeAction_2(self, action):
        self.showWarningMessage("HALF-SRW Tool 2")

    def executeAction_3(self, action):
        self.showWarningMessage("HALF-SRW Tool 3")

    def showConfirmMessage(self, message):
        msgBox = QtWidgets.QMessageBox()
        msgBox.setIcon(QtWidgets.QMessageBox.Question)
        msgBox.setText(message)
        msgBox.setInformativeText(
            "Element will be omitted.\nDo you want to continue importing procedure (a broken link will appear)?")
        msgBox.setStandardButtons(QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)
        msgBox.setDefaultButton(QtWidgets.QMessageBox.No)
        ret = msgBox.exec_()
        return ret

    def showWarningMessage(self, message):
        msgBox = QtWidgets.QMessageBox()
        msgBox.setIcon(QtWidgets.QMessageBox.Warning)
        msgBox.setText(message)
        msgBox.setStandardButtons(QtWidgets.QMessageBox.Ok)
        msgBox.exec_()

    def showCriticalMessage(self, message):
        msgBox = QtWidgets.QMessageBox()
        msgBox.setIcon(QtWidgets.QMessageBox.Critical)
        msgBox.setText(message)
        msgBox.setStandardButtons(QtWidgets.QMessageBox.Ok)
        msgBox.exec_()

    #################################################################
    #
    # SCHEME MANAGEMENT
    #
    #################################################################

    def getWidgetFromNode(self, node):
        return self.canvas_main_window.current_document().scheme().widget_for_node(node)

    def createLinks(self, nodes):
        previous_node = None
        for node in nodes:
            if not (isinstance(node, str)) and not previous_node is None and not (isinstance(previous_node, str)):
                link = SchemeLink(source_node=previous_node, source_channel="Beam", sink_node=node, sink_channel="Input Beam")
                self.canvas_main_window.current_document().addLink(link=link)
            previous_node = node

    def getWidgetDesc(self, widget_name):
        return self.canvas_main_window.widget_registry.widget(widget_name)

    def createNewNode(self, widget_desc):
        return self.canvas_main_window.current_document().createNewNode(widget_desc)

    def createNewNodeAndWidget(self, widget_desc):
        messages = []

        try:
            node = self.createNewNode(widget_desc)
            widget = self.getWidgetFromNode(node)

            # here you can put values on the attrubutes

        except Exception as exception:
            messages.append(exception.args[0])

        return widget, node, messages    