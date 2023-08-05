# simple-system-tests
Simple Python library for writing test cases for System and components tests including automatic reports via html. The intention is to have an easy framework for developers without the need to learn a separate coding language. Check out the repository via:
```
git clone https://github.com/chrisKoeh/simple-system-tests.git
```
Main advantages using this framework:
- separate command line option for each testcase allows faster debugging
- parameterized subtests require only one test function but allows multiple tests of one part with different values
- python only with just 3 decorator functions being necessary to learn

## (Optional) Build package locally
```
pip3 install setuptools wheel
python3 setup.py sdist bdist_wheel
(sudo) python3 setup.py install
```
## Installation
```
pip3 install simple-system-tests
```
## Quick-Start
After installation create a script with the following content:
```
import simple_system_tests as sst

@sst.testcase()
def my_testcase():
    sst.logger().info("this is a PASS")

sst.run_tests()
```
Upon execution an error message will be printed, that the `system_params.json` was not found
which can be ignored for now. After that open the created `index.html` for an overview
of the results in a web browser. For a more detailed example take a look at `examples` folder. 
## Testsuite
The Testsuite is defined under `simple_system_tests/TestSuite.py`:
- holds and executes testcases
- prepare and teardown of Testsuite, which can be implemented by using decorators(optional):
```
import simple_system_tests as sst
@sst.prepare_suite
def s_prepare():
    sst.logger().info("preparing the suite")
@sst.teardown_suite
def s_teardown():
    sst.logger().info("tearing the suite down")
```
- reporting of test results stored in `index.html` (can be configured via command line)
- providing command line options for configurations and all testcases allowing them to be called
separately

## Command line options
When using a Testsuite command line options for all testcases added to the suite will be
automatically created. Command line option shortcut will be
derived from the beginning characters of the decorated function name.
Make sure to have varying descriptions for your testcases. Having a look at the help of
`examples/main.py` will give the following output:
```
shell: python3 main.py -h
usage: main.py [-h] [-no] [-p JSON_SYSTEM_PARAMS] [-o REPORT_OUTPUT] [-e] [-s]
               [-m] [-j] [-r] [-t] [-pr] [-te]

optional arguments:
  -h, --help            show this help message and exit
  -no, --no-suite-setup
                        No Suite Prepare and Teardown
  -p JSON_SYSTEM_PARAMS, --json-system-params JSON_SYSTEM_PARAMS
                        Path to JSON params file.
  -o REPORT_OUTPUT, --report-output REPORT_OUTPUT
                        Path to report html file.
  -e, --env_case        Test Env case
  -s, --simple_print    Test Simple print
  -m, --multi_prints    Test Multi prints
  -j, --json_multi_prints
                        Test Json multi prints
  -r, --retry_case      Test Retry case
  -t, --timeout_case    Test Timeout case
  -pr, --prepare_fail_case
                        Test Prepare fail case
  -te, --teardown_fail_case
                        Test Teardown fail case
```
Testcases can be called separately without having to execute all testcases in one run.
It is also possible to pass multiple testcases in one execution. In case the Suite setup and
teardown is not wanted this can be achieved by putting the `-no, --no-suite-setup` option.
## Testcases
### Create new testcases

Testcases are created using decorators:
```
import simple_system_tests as sst

@sst.testcase()
def custom_testcase():
    raise Exception("Fails always, anyways")
```
A testcase is considered `PASS` as long as no exception is raised.
### Testcase arguments
```
@sst.testcase(retry=0, timeout=-1, prepare_func=None, teardown_func=None)
```
- retry: how often a testcase is retried before considered as `FAIL`
- timeout: in seconds how long the testcase may last, considered as `FAIL` if extended
- prepare_func / teardown_func: functions to be called before / after testcase execution

### Sub testcases
```
@sst.testcases(sub_params, retry=0...)
def multi_tests(sub_param):
    ...
```
It is possible to run multiple tests at once. The number of tests is defined by the list length
of the `sub_params` argument. The rest of the arguments are the same as for `@sst.testcase`
decorator.
### System parameters
Environment parameters for the testsuite can be used from a json file named `system_params.json`
(the file path can be customized by passing the `-p` option). Those will be made available in the
Testcase by the function `sst.get_env()`:
```
import simple_system_tests as sst

@sst.testcase()
def env_case():
    sst.logger().info(sst.get_env())
```
Setting these json params from within the testsuite, eg. in case
a global python object should be made available in Testsuite preparation for all testcases,
is possible with `sst.set_env(key, value)` function.
### Logging
The file path of the output file can be customized by passing the `-o` option, which defaults to
`index.html`. A `logger` object attribute is available within testcases and testsuites.
However stdout is mapped to `logger.info`, hence `print` can also be used directly which will
result in output of both console and html report file as `INFO` message.
