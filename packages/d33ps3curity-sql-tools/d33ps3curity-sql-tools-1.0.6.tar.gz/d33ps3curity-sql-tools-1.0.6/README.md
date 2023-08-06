# d33ps3curity-sql-tools

A simple middleware tool for analyzing Django ORM SQL execution. You can learn how to build this middleware package by following the steps below.

# Usage

Add the follow line of code to your middleware in your project settings.py file.

```
d33ps3curity-sql-tools.middleware.new_middleware
```

# How it works

The tool uses Django built in features to inspect the SQL generated from queries executed by the application. 3rd party tools are used to format and highlight the SQL presented in the terminal window.
