from bs4 import BeautifulSoup


class DOM:
    """类html对象 对DOM操作进行封装
    d = DOM('<div><span>123</span></div>')
    """
    def __init__(self,data):
        if(isinstance(data, str)):
            self._DOM = BeautifulSoup(data, 'lxml')
        else: 
            self._DOM = data
            
    def find(self,*args,**kwargs):
        """标签、css选择器
        d = DOM('<div><span class="haha">123</span></div>')
        print(d.find('.haha').format())"""
        return DOM(self._DOM.select_one(*args,**kwargs))

    def find_all(self,*args,**kwargs):
        """find()的多元素模式
        items = DOM(html).find_all('div.list-data-item')
        """
        return [DOM(data) for data in self._DOM.select(*args,**kwargs)]

    def get(self,*args,**kwargs):
        """获取元素属性值
        d = DOM('<div><a href="http://heinz97.top"><span class="haha">123</span></a></div>')
        print(d.find('div>a').get('href'))
        """
        return self._DOM.get(*args,**kwargs)

    @property
    def text(self,*args,**kwargs):
        """获取元素文本
        DOM('<div><a class="gx2"><span>gx</span><a></div>').find('a.gx2 span').get_text()
        """
        return self._DOM.get_text(*args,**kwargs)

    def format(self):
        """格式化输出html字符串
        a.find('a.gx').format()
        """
        return self._DOM.prettify()
