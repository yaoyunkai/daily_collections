/*
每个函数都会创建一个prototype属性，这个属性是一个对象，包含应该由特定引用类型的实例共享的属性和方法。
实际上，这个对象就是通过调用构造函数创建的对象的原型。
使用原型对象的好处是，在它上面定义的属性和方法可以被对象实例共享。

----------------------------------------------------------------
每个function都有 prototype的属性

这个prototype属性实例会有一个 constructor 属性指向方法自己。
这个prototype属性实例 [[Prototype]] --> 指向 Object构造函数的prototype属性

每次调用构造函数创建一个新实例，这个实例的内部[[Prototype]]指针就会被赋值为构造函数的原型对象
通过 __proto__ 访问这个指针

实例的 __proto__ 指向了原型对象，原型对象的constructor指向了构造方法

Object 原型对象的原型对象是null
Object.prototype.__proto__ === null

Object.getPrototypeOf 用来获取实例的 [[Prototype]]

同一个构造函数创建的实例共享原型对象

isPrototypeOf() 用来检查给定的原型对象是不是实例的原型对象

Object类型还有一个setPrototypeOf()方法，可以向实例的私有特性[[Prototype]]写入一个新值。这样就可以重写一个对象的原型继承关系

---------------------------------------------------------------------
搜索开始于对象实例本身。如果在这个实例上发现了给定的名称，则返回该名称对应的值。
如果没有找到这个属性，则搜索会沿着指针进入原型对象，然后在原型对象上找到属性后，再返回对应的值。

虽然可以通过实例读取原型对象上的值，但不可能通过实例重写这些值。
如果在实例上添加了一个与原型对象中同名的属性，那就会在实例上创建这个属性，这个属性会遮住原型对象上的属性。

hasOwnProperty()方法用于确定某个属性是在实例上还是在原型对象上。


*/

function Person() {
}

Person.prototype.name = "Nicholas";
Person.prototype.age = 29;
Person.prototype.job = "Software Engineer";
Person.prototype.sayName = function () {
    console.log(this.name);
};

let person1 = new Person();
person1.sayName(); // "Nicholas"

let person2 = new Person();
person2.sayName(); // "Nicholas"

// console.log(person1.sayName === person2.sayName); // true
// console.log(person1.age)
//
// person1.name = "Tom"
// console.log(person2.name)

console.log('----------------------------------\n')
console.log(typeof Person.prototype);  // Object
console.log(Person.prototype)  // 构造函数的原型对象
console.log(Person.prototype.constructor === Person); // 构造函数的prototype.constructor -> self

console.log(Person.prototype.__proto__ === Object.prototype);
console.log(Person.prototype.__proto__.constructor === Object);

console.log(Person.prototype.__proto__.__proto__ === null);
console.log(Person.prototype.__proto__);
// console.log(Object.prototype)


console.log(
    Object.getPrototypeOf(person1) === Object.getPrototypeOf(person2)
)

console.log(person1 instanceof Person)
