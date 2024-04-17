# Tests of the heating simulator

This README file provides an overview of the test suite included in the `test` directory for the heating simulator. The test suite consists of one test file, `test_heating_simulator.py`, which contains functional tests for the heating simulation. The test file covers the following test cases through 26 different tests:

1. Testing the `Boiler` class.
2. Testing the `Building` class.
3. Testing the `Regulator` class.
4. Testing the `Weather` class.
5. Testing the `Simulator` class.

By running these tests, that ensures that the heating simulation is working as expected.


## Prerequisites

Before running the tests, ensure that you have installed the required dependencies. You can install these dependencies by running:
```shell
poetry install
```

You also need to set the `PYTHONPATH` environment variable to the root directory of the simulation's files. This is required to ensure that the test files can import all the files from the root directory. You can set the `PYTHONPATH` environment variable by running the following command in your terminal:
```bash
export PYTHONPATH="${PYTHONPATH}:$(pwd)"
```


## Running the tests

To execute the tests, you can use the `pytest` command in your terminal. The `pytest` command will automatically discover and execute the test cases defined in `test_heating_simulator.py`. Follow the steps below to run the tests:

1. Open a terminal and navigate to the root directory of the simulator's files.

2. Run the following command to execute the tests:
```shell
pytest
```

3. The test results will be displayed in the terminal, indicating the number of passed and failed tests.
```shell
======================= test session starts ========================
platform darwin -- Python 3.11.4, pytest-7.4.0, pluggy-1.2.0
rootdir: /Users/philm/Documents/git-repo/tb-optibot/src/simulator
plugins: anyio-3.7.1
collected 26 items

test/test_heating_simulator.py ..........................    [100%]

======================== 26 passed in 4.65s ========================
```
