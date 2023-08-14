BaseModel的属性:
    dict()
    json()
    copy()
    parse_obj()   是一种实用工具，用于将任何对象加载到模型中，如果对象不是字典，还可以进行错误处理；
    parse_row()
    parse_file()

    from_orm()

    schema()

    schema_json()

    construct() 无需运行验证即可创建模型的类方法

    __fields_set__  模型实例初始化时设置的字段名称集

    __fields__      模型字段字典

    __config__


orm_mode = True

ValidationError:
    e.errors()
    e.json()




------------------------------------------------------------------------------------------

字段:
python的基本字段和 pydantic提供的一些字段


------------------------------------------------------------------------------------------
验证器


param1:
    value:  第二个参数总是要验证的字段值；可以随意命名


param2:
    values: 所有的字段的值的字典
    field: 当前验证的Field实例
    config: 模型的Config的类


构造函数的参数
    *: 匹配所有字段
    pre=True: 高优先级
    each_item=True: 应用容器的每个元素









