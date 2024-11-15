from typing import Annotated, Any, Dict

from litestar import Controller, Request, delete, get, post
from litestar.enums import RequestEncodingType
from litestar.params import Body
from litestar.response import Redirect, Template

from schemas.user import UserIn, UserPydantic
from security.auth import authenticate_user


class HTMLController(Controller):
    include_in_schema=False
    
    @get()
    async def index(self, request:"Request[UserPydantic,  Dict[str, str], Any]")->Template:
        print(request.user.id)
        return Template(template_name="index.html", context={"main":True})

    @get("tree")
    async def tree(self)->Template:
        return Template(template_name="tree.html", context={"tree":True})

    @get('table')
    async def employees(self)->Template:
        return Template(template_name='table.html', context={"table":True})

    @get('login')
    async def login(selft)->Template:    
        return Template(template_name="login.html", context={"login":True})

    @post('login')
    async def authenticate(self, data: Annotated[UserIn, Body(media_type=RequestEncodingType.URL_ENCODED)], 
                           request:"Request[Any, Any, Any]")->Redirect:
        user = await authenticate_user(data.username, data.password)
        if user is None:
            return Template(template_name="login.html", context={
                "login":True,
                "err":"Неверное имя пользователя или пароль!"
            })
        # return jwt_cookie_auth.login(identifier=str(user.id), response_body=UserPydantic.model_validate(user, from_attributes=True))
        request.set_session({"user_id":user.id})
        return Redirect(path="/")
    
    @delete("logout")
    async def logout(self, request:Request[Any, Any, Any])->None:
        if request.session:
            request.clear_session()           