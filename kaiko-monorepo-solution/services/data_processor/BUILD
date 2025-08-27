python_sources(name="src", dependencies=[
    "libs/common_utils:lib",
])

python_tests(name="tests", dependencies=[
    "libs/common_utils:lib",
])

# Optional PEX binary (for packaging or Docker usage via Pants)
pex_binary(
    name="bin",
    entry_point="services.data_processor.app.main:run",
    dependencies=[":src", "3rdparty/python:reqs"],
)
