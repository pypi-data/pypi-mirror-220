from wordx.word_file import WordFile
from jinja2 import Template


class Sheet(WordFile):
    """简易文档生成(配套使用标准模板文件)"""
    def __init__(self, tpl_path):
        super().__init__(tpl_path)

    @staticmethod
    def render_template(tpl, data):
        lib = {
            'enumerate': enumerate,
            'len': len,
            'isinstance': isinstance,
            'tuple': tuple,
            'list': list
        }
        return Template(tpl).render(**data, **lib)

    def render_header(self, data):
        """页眉渲染"""
        header_xml = self.retrieve(f'word/header.xml')
        self['word/header.xml'] = self.render_template(header_xml, data)

    def render_footer(self, data):
        """页脚渲染""" 
        footer_xml = self.retrieve(f'word/footer.xml')
        self['word/footer.xml'] = self.render_template(footer_xml, data)

    def render_document(self, data):
        """文档渲染"""
        document_xml = self.retrieve(f'word/document.xml')
        self['word/document.xml'] = self.render_template(document_xml, data)

    def render_and_add_header(self, data):
        """添加页眉"""
        header_xml_data = self.render_template(self.retrieve(f'word/header.xml'), data)
        return self.add_header(header_xml_data)

    def render_and_add_footer(self, data):
        """添加页脚"""
        footer_xml_data = self.render_template(self.retrieve(f'word/footer.xml'), data)
        return self.add_footer(footer_xml_data)

    def render(self, data):
        self.render_header(data)
        self.render_footer(data)
        self.render_document(data)
        return self