# kNN Digit Recognition Using Flask

- [kNN Digit Recognition Using Flask](#knn-digit-recognition-using-flask)
  - [For Who?](#for-who)
  - [How to use it?](#how-to-use-it)
    - [Complete Version](#complete-version)
    - [Skeleton Version](#skeleton-version)
  - [Inspiration](#inspiration)
  - [Go Further](#go-further)
  - [Resource List](#resource-list)
  - [License](#license)


## For Who?

This project is for students of ERG3010 Fall 2019, CUHK(SZ) as well as everyone who is interested in building web interface.

## How to use it?

I provide 2 versions of codes here: a complete version and a skeleton verison.

Note: for the following shell instructions, you may need to change `python` and `pip` to `python3` and `pip3` if you have multiple versions of `python`.

### Complete Version

For the complete version, it is already available to run:

1. `$pip install -r requirements.txt`
2. `$cd complete`
3. Edit `config.json` with proper database settings.
4. `$python setup.py`
5. `$python app.py`

Then, you can go to browser and enter url: `http://localhost:5000`.

To terminate it, use `Ctrl + C` on terminal. To restart it, run `$python app.py` again.

### Skeleton Version

For the skeleton version, I have removed some implementations of functions. You are required to complete these functions based on the comments first to make progress.

The first step to start is similar to the complete version:

1. `$pip install -r requirements.txt`
2. `$cd skeleton`
3. Edit `config.json` with proper database settings.

Then, you should implement functions in `db_func.py` first. 

After you implement them, run `$python test.py` and some tests will be PASSED!

After implementing `db_func.py`, you should implement `knn.py` now. You can also check your progress by running `$python test.py$.

If you have passed all the tests, you can now start to code your Flask app. For this part, the test is not provided. You can test it using `print` and `console.log()` and taking advantage of your browser's development tool.

Moreover, the frontend for the skeleton version is very simple. You may take advantage of Bootstrap or other packages to redesign it.

If you stuck in somewhere, you may go to the complete version and see the sample code.

**Enjoy it!**

## Inspiration

The inspiration of using Flask (Python) is intuitive, because Python is one of the most popular language for data science and artificial intelligent. Most codes of data analysis are written in Python. Then, why don't we just use a Python web framework as the interface for our data functions?

Learning Flask can help you easily integrate your data analysis with web interface, making it available on web as soon as possible.


## Go Further

This project still has much improvement potential:

1. Because Python cannot serve simple requests as fast as PHP, can you separate some queries into PHP, and use __backward proxy__ (with **Apache** or **Nginx**) to connect PHP program and your Flask program? For example, for those simple database manipulation, use PHP to implement them, and leave Flask to handle only the matrix and algorithm's job with the power of __numpy__ and other packages.
2. Can you make the frontend more beautiful?
3. Are there any potential bugs?
4. Can you add more features to it, such as do the statistics of the total number of predictions and the accuracy of the prediction? Can you use **PHP** to implement this part?

If you are interested in, you can add more stuff to this project, save your version into another folder, and make a pull request. Hope to see other interesting ideas!

## Resource List

1. Flask:
   1. (Official Document): https://flask.palletsprojects.com/en/1.1.x/
   2. (Chinese Version): https://dormousehole.readthedocs.io/en/latest/
   3. (GitHub): https://github.com/pallets/flask
2. Bootstrap (An Easy-To-Use UI Library):
   1. (Official Website): https://getbootstrap.com
   2. (Chinese Version): https://www.bootcss.com/
   3. (GitHub): https://github.com/twbs/bootstrap
3. HTML:
   1. Guide in English:
      1. https://developer.mozilla.org/en-US/docs/Web/HTML
      2. https://www.w3schools.com/html/
   2. Guide in Chinese:
      1. https://developer.mozilla.org/zh-CN/docs/Web/HTML
      2. https://www.runoob.com/html/html-tutorial.html
      3. https://www.w3school.com.cn/html/index.asp
4. CSS:
   1. Guide in English:
      1. https://developer.mozilla.org/en-US/docs/Web/CSS
      2. https://www.w3schools.com/css/
   2. Guide in Chinese:
      1. https://developer.mozilla.org/zh-CN/docs/Web/CSS
      2. https://www.runoob.com/css/css-tutorial.html
5. JavaScript:
   1. Guide in English:
      1. https://developer.mozilla.org/en-US/docs/Web/JavaScript
      2. https://www.w3schools.com/js/
   2. Guide in Chinese:
      1. https://developer.mozilla.org/zh-CN/docs/Web/JavaScript
      2. https://www.runoob.com/js/js-tutorial.html
6. React (A JavaScript Framework for Single Page Application):
    1. English: https://reactjs.org/
    2. Chinese: https://react.docschina.org/
7. Ant Design (A React-Based UI Framework by Ant Financial):
    1. http://ant.design/
8. Vue.js (An Easy JavaScript Framework):
    1. https://vuejs.org/index.html
9. Element UI:
    1.  https://element.eleme.io/#/en-US
10. Apache HTTP Server (The default software to run PHP):
    1.  https://httpd.apache.org/
    2.  (Chinese Version): https://www.yiibai.com/apache_http/
11. Nginx (A high performance HTTP Server):
    1.  https://nginx.org/en/
    2.  (Chinese Version): https://www.w3cschool.cn/nginx/

## License

MIT License

Copyright (c) 2019 Guochao Xie
