from litestar import Router

from .auth import AuthController
from .employee import EmployeeController
from .position import PositionController

auth_router =     Router(path="/", tags=["Authentication"], route_handlers=[AuthController])
employee_router = Router(path="/", tags=["Employees"], route_handlers=[EmployeeController])
position_router = Router(path="/", tags=["Position"], route_handlers=[PositionController])
