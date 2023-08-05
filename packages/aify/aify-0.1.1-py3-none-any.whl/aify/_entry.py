import os
import json
import contextlib
from starlette.applications import Starlette
from starlette.routing import Mount, Route
from starlette.staticfiles import StaticFiles
from starlette.responses import JSONResponse, StreamingResponse
from starlette.exceptions import HTTPException
from fastapi import FastAPI, Request
from . import _env
from . import _program
from . import memory
from ._logging import logger
from ._web_template import render

# FastAPI
api = FastAPI()

def get_program(name: str) -> _program.Program:
    program = None
    try:
        program = _program.get(name)
    except Exception as e:
        logger.error(e, exc_info=e)
        raise HTTPException(
            status_code=404, detail=f"Not a valid app: {e}")
    return program

@api.put('/apps/{name}/{session_id}')
async def execute_program(request: Request, name: str, session_id: str):
    program = get_program(name)
    
    kwargs = {}
    try:
        kwargs = await request.json()
    except Exception as e:
        raise HTTPException(status_code=400, detail="Bad request body.")
    
    kwargs['program_name'] = name
    kwargs['session_id'] = session_id

    filter_variable = request.query_params.get('variable')
    if filter_variable and not (filter_variable in program.input_variable_names or filter_variable in program.output_variable_names):
        raise HTTPException(status_code=400, detail="invalid variable.")

    # Server Sent Events
    sse = 'sse' in request.query_params

    # https://github.com/microsoft/guidance/discussions/129
    async def _aiter():
        pos = dict([(vname, 0) for vname in program.output_variable_names])
        #pos = 0
        catched = False

        kwargs['stream'] = True
        kwargs['async_mode'] = True
        kwargs['silent'] = True

        async for t in program.run(**kwargs):
            if t._exception:
                if catched:
                    return
                catched = True

                e = {
                    "error": str(t._exception)
                }
                if sse:
                    yield "event: error\ndata: %s\n\n" % json.dumps(e)
                else:
                    yield json.dumps(e)
            else:
                #generated = t.text if not variable else t.get(variable)
                for vname in program.output_variable_names:

                    if filter_variable and vname != filter_variable:
                        continue

                    generated = t.get(vname)
                    if generated:
                        diff = generated[pos[vname]:]
                        pos[vname] = len(generated)
                        if len(diff) > 0:
                            if sse:
                                e = {
                                    "variable": vname,
                                    "diff": diff
                                }

                                yield "event: message\ndata: %s\n\n" % json.dumps(e)
                            else:
                                yield diff

    content_type = 'text/event-stream' if sse else 'text/plain'

    try:
        it = _aiter()
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Something wrong: {e}")

    return StreamingResponse(it, headers={'Content-Type': content_type})

@api.get('/apps/{name}/{session_id}/memories')
async def get_memories(request: Request, name: str, session_id: str):
    memories = []
    program = get_program(name)
    memory = program.modules.get('memory')
    if memory:
        m = memory.read(name, session_id, max_len=2040*1024, n=1000)
        if m:
            memories = m
    return JSONResponse(memories)

@api.get('/apps')
async def list_apps(request: Request):
    progs = []
    if len(_program.programs) == 0:
        _program.reload()

    for name, prog in _program.programs.items():
        progs.append({
            'name': name,
            'title': prog.template.get('title'),
            'description': prog.template.get('description'),
            'icon_emoji': prog.template.get('icon_emoji'),
        })
    
    return JSONResponse(progs)

@api.get('/sessions')
async def list_sessions(request: Request):
    return JSONResponse(memory.sessions())

# Routes
routes = [
    Mount(
        '/api',
        name='api',
        app=api
    ),
    Mount(
        '/static',
        name='static',
        app=StaticFiles(directory=os.path.join(_env.webui_dir(), 'static'), check_dir=False),
    ),
    Route(
        '/',
        name='home',
        endpoint=render('index.html')
    )
]

apps_static_dir = os.path.join(_env.get_apps_dir(), 'static')
if os.path.exists(apps_static_dir):
    routes.append(Mount(
        '/apps/static',
        name='apps_static',
        app=StaticFiles(directory=apps_static_dir, check_dir=False),
    ))

@contextlib.asynccontextmanager
async def lifespan(app):
    yield

entry = Starlette(debug=True, routes=routes, lifespan=lifespan)
