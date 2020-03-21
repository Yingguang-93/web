from django.test import TestCase

# Create your tests here.


class A(object):
    def __init__(self, a, b):
        self.a = a
        self.b = b

    @property
    def name(self):
        return 'itcast'

    def show(self):
        print(self.a, self.b)


if __name__ == "__main__":
    obj = A(1, 2)
    # res = obj.name
    # print(res)

    # print(obj.a)
    # res = getattr(obj, 'a')
    # print(res)

    # obj.show()
    # func = getattr(obj, 'show')
    # func()
    # 注：类视图原理：使用getattr根据请求方式获取类视图中对应方法，然后调用
