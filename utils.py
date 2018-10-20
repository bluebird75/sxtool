# Copyright 2018 Philippe Fremy
# This software is provided under the BSD 2 clause license; see LICENSE.txt file for more information
import os
import xml.sax as sax
import xml.dom.minidom as dom

from PyQt5.QtWidgets import QActionGroup

from typing import List, Any

class ItemHistory(object) :
    """ Class for storing the history of items added to an object, subclassing is needed """
    
    def __init__(self, fileName : str, maxSize : int):
        self.fileName = fileName # type : str
        self.maxSize = maxSize   # type : int
        if not os.path.exists(fileName) :
            self._createNewTree()
        try:
            self.tree = dom.parse(fileName)
        except sax.SAXParseException :
            self._createNewTree()
            #self.tree = dom.parse(fileName)
        if not self.tree :
            raise Exception( "Error: Couldn't create history file" )
        
    def _getText(self, itemNode:Any ) -> str:
        text = ""   # type: str
        for textNode in itemNode.childNodes :
            if textNode.nodeType == dom.Node.TEXT_NODE :
                 text += textNode.data
        return text.strip(" \n\t")
            
    def _createNewTree(self) -> None:
        self.tree = dom.Document() 
        tag_history = dom.Element("history") 
        self.tree.appendChild(tag_history)
        self.historyFile = open(self.fileName, "w+") 
        self.tree.writexml(self.historyFile, "", "", "") 
        self.historyFile.close()

    def _removeLastItem(self) -> None:
        pass
    
    def _insertItem(self, index:int, item:Any) -> None:
        pass
       
    def addItemToHistory(self,item : str) -> None:
        item = item.strip(" \n\t")
        itemNode= dom.Element("item")
        text = self.tree.createTextNode(item)   # type: str
        itemNode.appendChild(text)              # type: List[str
        items = self.tree.getElementsByTagName("item")
        if len(items) >= self.maxSize :
            self.tree.firstChild.removeChild(items[-1])
            self._removeLastItem()
            items = self.tree.getElementsByTagName("item")
        if not items :
            self.tree.firstChild.appendChild(itemNode)
        else :
            for n in items :
                if self._getText(n) == item :
                    return
            self.tree.firstChild.insertBefore(itemNode,items[0])
        self._insertItem(0,item)

    def save(self) -> None:
        historyFile = open(self.fileName, "w") 
        self.tree.writexml(historyFile, "", "", "") 
        historyFile.close()
        
class ItemHistoryStringList(ItemHistory):
    """ Class for storing text items in a list """
    def __init__(self, stringList:List[str], fileName:str, maxSize:int ):
        ItemHistory.__init__(self, fileName, maxSize )
        self.stringList = stringList    # type: List[str]
        items = self.tree.getElementsByTagName("item")
        for node in items :
            text = self._getText(node)  # type: str
            self.stringList += [text]        

    def _removeLastItem(self) -> None:
        if self.stringList :
            del self.stringList[-1:]
    
    def _insertItem(self, index:int, item:str) -> None:
        self.stringList.insert(index, item)
    
    
class ItemHistoryMenu(ItemHistory):
    """ Class for storing the history of items added to a QMenu """
    
    def __init__(self, fileName:str, maxSize:int, menu:Any, callbackMethod:Any ):
        ItemHistory.__init__(self, fileName, maxSize )
        self.menu = menu
        self.callbackMethod = callbackMethod
        items = self.tree.getElementsByTagName("item")
        self.actionGroup = QActionGroup(None)
        for node in items :
            text = self._getText(node)  # type: str
            a = self.menu.addAction(text)   # type: Any
            self.actionGroup.addAction(a)
        self.actionGroup.triggered.connect( self.actionTriggered )

    def _removeLastItem(self) -> None:
        actionList = self.actionGroup.actions()
        if actionList :
            a = actionList[-1]
            self.menu.removeAction(a)
            self.actionGroup.removeAction(a)
    
    def _insertItem(self, index:int, item) -> None:
        actionList = self.actionGroup.actions()
        actions = []    # type: List[str]
        for a in actionList :
            actions.append(a.text())
            self.actionGroup.removeAction(a)
        self.menu.clear()
        actions = [item] + actions
        for action in actions :
            a = self.menu.addAction(action)
            self.actionGroup.addAction(a)    
        self.actionGroup.triggered.connect( self.actionTriggered )

    def actionTriggered(self, action) -> None:
        self.callbackMethod(action.text())
    
