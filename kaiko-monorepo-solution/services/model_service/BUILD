python_sources(name="src", dependencies=[
    "libs/common_utils:lib",
])

python_tests(name="tests", dependencies=[
    "libs/common_utils:lib",
])

pex_binary(
    name="bin",
    entry_point="services.model_service.app.main:run",
    dependencies=[":src", "3rdparty/python:reqs"],
)
