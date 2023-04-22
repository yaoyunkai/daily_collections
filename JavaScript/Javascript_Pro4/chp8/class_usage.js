/*
JavaScript中的class

Person.prototype: 实例的原型 ???

Person.prototype.constructor === Person

先调用 static init block
然后调用 constructor

new.target === class对象

在箭头函数中，this引用的是定义箭头函数的上下文。

 */

function MyClass() {
    this.myField = "foo";
    // Constructor body
}

MyClass.myStaticField = "bar";
MyClass.myStaticMethod = function () {
    // myStaticMethod body
};
MyClass.prototype.myMethod = function () {
    // myMethod body
};

(function () {
    // Static initialization code
})();


class Person {
    // 这些属性相当于类变量
    name = 'Null';
    age = 0;

    static TYPE = 'AA';

    static sayClass() {
        console.log('My class is Person, type is ' + this.TYPE);
    }

    constructor(name, age) {
        // 这些属性相当于实例变量
        this.name = name;
        this.age = age
    }

    // 实例共享一个方法对象
    sayHello() {
        console.log("Name: " + this.name + " Hello")
    }

    static {
        console.log('static init block')
    }

    static {
        console.log('static init block2')
    }
}

class Student extends Person {
    constructor(name, age, clazz) {
        super(name, age);
        this.clazz = clazz
    }

    sayHello() {
        super.sayHello();
        console.log('My class is ' + this.clazz);
    }
}

let p = new Person('Tom', 18)
p.sayHello()

console.log(p.age);

console.log(Person.TYPE);
Person.sayClass();


let s = new Student('dd', 19, 'C1');
s.sayHello();
