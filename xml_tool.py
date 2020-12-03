# -*- coding:utf8 -*- # 避免中文乱码
import os

import xml.dom.minidom
parent_file = os.getcwd()
xml_file = parent_file + "\\Manager.xml"


class XmlTool:
    def parse_xml(self):
        try:
            # 解析xml文件
            xmlDoc = xml.dom.minidom.parse(xml_file)
        except Exception as e :
            return None,None
        # 获取根节点
        rootNode = xmlDoc.documentElement
        FileMessages = rootNode.getElementsByTagName('FileMessage')
        return xmlDoc,FileMessages

    def read_message(self):
        messageLists = []
        xmlDoc,FileMessages = self.parse_xml()
        if xmlDoc:
            for file_message in FileMessages:
                file_name = file_message.getElementsByTagName('FileName')[0]
                file_path = file_message.getElementsByTagName('FilePath')[0]
                messageDict = {'file_name': file_name.childNodes[0].data, 'file_path': file_path.childNodes[0].data}
                messageLists.append(messageDict)
            return messageLists

    def add_message(self, messageDict):
        # 第一次使用需要新建xml文件
        if not os.path.exists(xml_file):
            # 在内存中创建一个空的文档
            xmlDoc = xml.dom.minidom.Document()
            # 创建一个根节点Managers对象
            rootNode = xmlDoc.createElement('FileMessages')
            xmlDoc.appendChild(rootNode)
            with open(xml_file, 'w', encoding='utf-8') as f:
                xmlDoc.writexml(f, addindent='  ', encoding='utf-8')
        # 解析xml文件
        xmlDoc = xml.dom.minidom.parse(xml_file)
        # 获取根节点
        rootNode = xmlDoc.documentElement
        # for messageList in messageLists:
        fileMessage = xmlDoc.createElement('FileMessage')
        fileName = xmlDoc.createElement('FileName')
        filePath = xmlDoc.createElement('FilePath')
        fileName.appendChild(xmlDoc.createTextNode(messageDict['file_name']))
        filePath.appendChild(xmlDoc.createTextNode(messageDict['file_path']))
        fileMessage.appendChild(fileName)
        fileMessage.appendChild(filePath)
        rootNode.appendChild(fileMessage)
        with open(xml_file, 'w', encoding='utf-8') as f:
            xmlDoc.writexml(f)

    def del_message(self, del_file_name):
        rootNode,FileMessages = self.parse_xml()
        for file_message in FileMessages:
            file_name_node = file_message.getElementsByTagName('FileName')
            file_name = file_name_node[0].childNodes[0].data
            if file_name == del_file_name:
                # print(file_name_node)
                # print(file_message)
                # rootNode.delete(file_message)
                break

    def change_message(self, messageDict, change_file_path):
        xmlDoc, FileMessages = self.parse_xml()
        rootNode = xmlDoc.documentElement
        for file_message in FileMessages:
            file_name_node = file_message.getElementsByTagName('FileName')
            file_name = file_name_node[0].childNodes[0].data
            if file_name == change_file_path:
                file_message.childNodes[0].childNodes[0].data = messageDict['file_name']
                file_message.childNodes[1].childNodes[0].data = messageDict['file_path']
                # file_name.text = messageDict['file_name']
                # file_name_node.text = messageDict['file_path']
                # file_name_node[0].childNodes[0].data = change_file_path
                # print(file_name_node)
                break
        with open(xml_file, 'w', encoding='utf-8') as f:
            xmlDoc.writexml(f)



if __name__ == "__main__":
    xmlTool = XmlTool()
    messageLists = xmlTool.read_message()

