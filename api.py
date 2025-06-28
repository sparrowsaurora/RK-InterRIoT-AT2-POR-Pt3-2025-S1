"""
 Assessment Title: Portfolio Part X
 Cluster:          Intermediate RIoT
 Qualification:    ICT50220 Diploma of Information Technology (Advanced Programming)
 Name:             ryan kelley
 Student ID:       20136584
 Year/Semester:    20YY/SN

 YOUR SUMMARY OF PORTFOLIO ACTIVITY
 GOES HERE

"""

# Imports
from pathlib import Path

from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

import casbin
from fastapi_authz import CasbinMiddleware
from starlette.middleware.authentication import AuthenticationMiddleware
from starlette.authentication import requires, AuthenticationError

import basic_auth as basic_auth

# Global CONSTANTS


## Global Variables

api = FastAPI(title='RK-InterRIoT-AT2-POR-Pt3-2025-S1')

enforcer = casbin.Enforcer(
    'api/rbac_model.conf',
    'api/rbac_policy.csv',
)

backend = basic_auth.BasicAuth()

api.add_middleware(CasbinMiddleware, enforcer=enforcer)
api.add_middleware(AuthenticationMiddleware, backend=backend)


BASE_PATH = Path(__file__).parent
print(BASE_PATH)

api.mount("/static",
          StaticFiles(directory="static"),
          name="static")

api.mount("/css",
          StaticFiles(directory="static/css"),
          name="css")
api.mount("/js",
          StaticFiles(directory="static/js"),
          name="js")
api.mount("/images",
          StaticFiles(directory="static/img"),
          name="images")

TEMPLATES = Jinja2Templates(directory="templates")


# Functions/Methods
@api.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return TEMPLATES.TemplateResponse(
        request=request,
        name="pages/home.html"
    )

@api.exception_handler(AuthenticationError)
async def auth_exception_handler(request: Request, exc: AuthenticationError):
    '''Custom authentication error handler to return JSON response'''
    return JSONResponse(
        content={"success": False, "message": str(exc), "data": []},
        status_code=401
    )
@api.get("/api")
async def api_index():
    return JSONResponse(content={
    "success": True,
    "message": "Endpoint: /",
    "data": [
        {"greeting": "Hello, world."}
    ]
})


@api.get("/about", response_class=HTMLResponse)
async def about(request: Request):
    return TEMPLATES.TemplateResponse(
        request=request,
        name="pages/about.html"
    )

@api.get("/api/data")
async def api_data(request: Request):
    return { 'name':'Frank Spencer' }

@api.get("/api/ds1/res1 ")
async def api_ds1(request: Request):
    return JSONResponse(content={
    "success": True,
    "message": "Endpoint: ds1/res1",
    "data": [
        {"greeting": "Resource 1 accessed"}
    ]
})


@api.get("/api/ds2/res2 ")
async def api_ds2(request: Request):
    return JSONResponse(content={
    "success": True,
    "message": "Endpoint: ds2/res2",
    "data": [
        {"greeting": "Resource 2 accessed"}
    ]
})


# Main Code
