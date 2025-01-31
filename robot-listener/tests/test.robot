*** Settings ***
Documentation       Test suite that showcase the listener capabilities

*** Variables ***
${STRING}=                  cat
${NUMBER}=                  ${1}
@{LIST}=                    one    two    three
&{DICTIONARY}=              string=${STRING}    number=${NUMBER}    list=@{LIST}
${ENVIRONMENT_VARIABLE}=    %{PATH=Default value}


*** Tasks ***
Call keywords with a varying number of arguments
    [Documentation]    This is a test documentation
    A keyword without arguments
    A keyword with a required argument    ${10}
    A keyword with a required argument    Argument
    A keyword with an optional argument
    A keyword with an optional argument    ${NUMBER}
    A keyword with an optional argument    argument=Argument
    A keyword with any number of arguments
    A keyword with any number of arguments    arg1    arg2    arg3    arg4    arg5
    A keyword with one or more arguments    arg1
    A keyword with one or more arguments    arg1    arg2    @{LIST}
    Log Many    @{LIST}    &{DICTIONARY}    ${STRING}
    Comment    Test comment
    ${result}=    Convert To Binary    10
    Log    Result is ${result}
    Log To Console    Result is ${result}

*** Keywords ***
A keyword without arguments
    A keyword with a required argument    Argument=test

A keyword that fails
    Fail    This keyword will fail
    

A keyword with a required argument
    [Arguments]    ${argument}
    Log To Console    A log in the console of numer ${NUMBER}
    Log    Required argument: ${argument}

A keyword with an optional argument
    [Arguments]    ${argument}=Default value
    Log    Optional argument: ${argument}

A keyword with any number of arguments
    [Arguments]    @{varargs}
    Log    Any number of arguments: @{varargs}

A keyword with one or more arguments
    [Arguments]    ${argument}    @{varargs}
    Log    One or more arguments: ${argument} @{varargs}