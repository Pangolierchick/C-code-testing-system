# Base
This is a project that helps you to test C (and further C++) programms that inputes something and then print
and also it checks main returned value

# How to write tests

So what do you need to test your programms? Of course, tests. So you need to create *.txt file somewhere
and then give a path to testsystem. So the template of test file is 

```
#test1

#input

4
2 4 6 8

#output

None

#exitcode

0
```

Test block starts with ```#test``` and then you can see blocks ```input```, ```output``` and ```exitcode```. In that blocks you writing your tests.

# How to test

So to test code you need to exec testsystem via console like:

```bash
python3 ./TestSystem.py test -pt PATH_TO_TESTS -pe PATH_TO_C_FILE
```





