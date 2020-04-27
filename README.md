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
You can write input, output, exitcode blocks in whatever order you want. Also if your programm outputs nothing you can write either None or " " (space)

# How to test

So to test code you need to exec testsystem via console like:

```bash
python3 ./bin/__main__.py test -pt PATH_TO_TESTS -pc PATH_TO_C_FILE
```

Or if you are using [compiled version](https://yadi.sk/d/kHy5cWYrlKmC8w) (it was tested under macos Catalina, so write issue if you had some problems)

```bash
chmod +x ./TestSystem - you have to do it only once
TestSystem test -pt PATH_TO_TESTS -pc PATH_TO_C_FILE
```


