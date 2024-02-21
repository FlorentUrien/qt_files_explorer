import sys
from PySide6.QtWidgets import QApplication, QFileSystemModel, QTreeView, QListView, QDialog, QHBoxLayout, QVBoxLayout, \
    QLabel
from PySide6.QtCore import QDir, Slot, QModelIndex


class Explorer(QDialog):
    """
    Pour programmer un explorateur de fichiers.
    """

    def __init__(self, application: QApplication):
        super().__init__(None)
        self.__app = application
        self.setWindowTitle("Explorateur de fichiers")

        # Le FileSystemModel du tree
        self.__fs = QFileSystemModel()
        self.__fs.setRootPath(QDir.currentPath())
        self.__fs.setFilter(QDir.Filter.AllDirs | QDir.Filter.NoDotAndDotDot)

        # Le label pour indiquer où nous sommes
        self.__chemin = QLabel(QDir.currentPath())

        # La représentation sous forme d'arbres
        self.__tree = QTreeView()
        self.__tree.setModel(self.__fs)
        self.__tree.setRootIndex(self.__fs.index(QDir.currentPath()))

        # Le fileSystemModel de la liste
        self.__fsl = QFileSystemModel()
        self.__fsl.setRootPath(QDir.currentPath())

        # Le label pour indiquer où nous sommes
        self.__info_fichier = QLabel()

        # La représentation sous for de liste
        self.__lv = QListView()
        self.__lv.setModel(self.__fsl)
        self.__lv.setRootIndex(self.__fsl.index(QDir.currentPath()))

        # L'organisation du QDialog
        tree_layout = QVBoxLayout()
        tree_layout.addWidget(self.__chemin)
        tree_layout.addWidget(self.__tree)
        lv_layout = QVBoxLayout()
        lv_layout.addWidget(self.__info_fichier)
        lv_layout.addWidget(self.__lv)

        self.__layout = QHBoxLayout(self)
        # Pour prendre 2x plus de place que le lv_layout
        self.__layout.addLayout(tree_layout, 2)
        self.__layout.addLayout(lv_layout, 1)
        self.setLayout(self.__layout)

        # Si on clique sur un répertoire du tree
        self.__tree.clicked.connect(self.__clic_tree)

        # Si on clique sur un élément de la liste
        self.__lv.clicked.connect(self.__clic_liste)

    @Slot()
    def __clic_tree(self, index: QModelIndex):
        self.__full_path = self.__fs.filePath(index)
        self.__chemin.setText(self.__full_path)
        self.__lv.setRootIndex(self.__fsl.index(self.__full_path))

    @Slot()
    def __clic_liste(self, index: QModelIndex):
        if not (self.__fsl.isDir(index)):
            mess = self.__fsl.filePath(index)
            mess += " (" + str(self.__fsl.size(index)) + " octets )"
            self.__info_fichier.setText(mess)


if __name__ == '__main__':
    # On crée l'application
    app = QApplication(sys.argv)
    explorer = Explorer(app)
    explorer.show()

    sys.exit(app.exec())
