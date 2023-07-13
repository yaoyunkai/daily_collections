uvicorn module-name:app --reload


path params:

path是按code的顺序解析的

query params:

声明不属于路径参数的其他函数参数时，它们将被自动解释为"查询字符串"参数


request body: Body
    embed=True



查询参数和字符串校验: Query

路径参数和数值校验: Path


cookie: Cookie 参数
    也需要放到function的方法参数中

header: Header
默认情况下, Header 将把参数名称的字符从下划线 (_) 转换为连字符 (-) 来提取并记录 headers.


响应状态码:
    @app.post("/items/", status_code=201)
    @app.post("/items/", status_code=status.HTTP_201_CREATED)


APIRouter:

router = APIRouter(
    prefix="/items",
    tags=["items"],
    dependencies=[Depends(get_token_header)],
    responses={404: {"description": "Not found"}},
)

app.include_router(users.router)
app.include_router(items.router)
app.include_router(
    admin.router,
    prefix="/admin",
    tags=["admin"],
    dependencies=[Depends(get_token_header)],
    responses={418: {"description": "I'm a teapot"}},
)
