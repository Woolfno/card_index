from litestar import Controller
from litestar.response import Template
from litestar import get, route, Request, HttpMethod
from security.jwt import authenticate_user, jwt_auth


class HTMLController(Controller):
    path = "/"
    
    @get(exclude_from_auth=True)
    async def index(self)->Template:
        return Template(template_name="index.html", context={"main":True})

    @get("tree")
    async def tree(self)->Template:
        return Template(template_name="tree.html", context={"tree":True})

    @get('table')
    async def employees(self)->Template:
        return Template(template_name='table.html', context={"table":True})

    @route(path='login', http_method=[HttpMethod.GET, HttpMethod.POST])  
    async def login(self, request:Request)->Template:    
        if request.method==HttpMethod.GET:
            return Template(template_name="login.html", context={"login":True})

        form_data = await request.form()
        username = form_data.get("username")
        password = form_data.get("password")
        user = await authenticate_user(username, password)
        if user is None:
            return Template(template_name="login.html", context={
                "login":True,
                "err":"Неверное имя пользователя или пароль!"
            })
        return jwt_auth.login(identifier=user.id)
