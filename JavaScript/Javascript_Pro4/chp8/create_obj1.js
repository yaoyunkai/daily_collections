/*
工厂模式


 */
function createPerson(name, age, job) {
    let o = {};
    o.name = name;
    o.age = age;
    o.job = job;
    o.sayName = function () {
        console.log(this.name);
    };
    return o;
}

let person1 = createPerson("Nicholas", 29, "Software Engineer");
let person2 = createPerson("Greg", 27, "Doctor");


/*
构造函数模式
要创建Person的实例，应使用new操作符。

这个新对象内部的[[Prototype]]特性被赋值为构造函数的prototype属性
构造函数内部的this被赋值为这个新对象（即this指向新对象）

构造函数的主要问题在于，其定义的方法会在每个实例上都创建一遍。

*/
function Person(name, age, job) {
    this.name = name;
    this.age = age;
    this.job = job;
    this.sayName = function () {
        console.log(this.name);
    };
}

let person3 = new Person("Nicholas", 29, "Software Engineer");
let person4 = new Person("Greg", 27, "Doctor");
person3.sayName();   // Nicholas
person4.sayName();   // Greg

console.log(person3 instanceof Object);   // true
console.log(person3 instanceof Person);   // true
console.log(person4 instanceof Object);   // true
console.log(person4 instanceof Person);   // true

let Person2 = function (name, age, job) {
    this.name = name;
    this.age = age;
    this.job = job;
    this.sayName = function () {
        console.log(this.name);
    };
}
let person5 = new Person2("Nicholas", 29, "Software Engineer");
let person6 = new Person2("Greg", 27, "Doctor");
person5.sayName();   // Nicholas
person6.sayName();   // Greg
console.log(person5 instanceof Object);   // true
console.log(person5 instanceof Person2);   // true
console.log(person6 instanceof Object);   // true
console.log(person6 instanceof Person2);   // true

console.log('test function equal')
console.log(person5.sayName === person6.sayName)