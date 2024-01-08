# SearchTitle_catalyzex

## 方法一：源码

安装需要的包，使用jupyter分阶段运行，



第一段：登录，手动



第二段：查询信息填写，自己添加申请人、发明人，并在页尾设置为每页显示50条信息。



第三段：本页面所有的专利信息爬取




常用网站：

https://pss-system.cponline.cnipa.gov.cn/seniorSearch

查询单个专利详细内容，可以导出excel，但不包含法律状态



https://cpquery.cponline.cnipa.gov.cn/chinesepatent/index

专利状态查询，但不能直接批量导出



我觉得可以在使用python代码在cpquery查询后，导出专利基本信息，但是缺少发明人信息，此时可以用上面那个专利检索分析网站查询导出，或者使用知网导出excel也行，然后根据申请号，将两个excel合并。



当然也可以自己添加代码，点击专利详情，爬取作者信息。
