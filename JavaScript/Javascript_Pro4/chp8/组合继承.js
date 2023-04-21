/*
基本的思路是使用原型链继承原型上的属性和方法，而通过盗用构造函数继承实例属性。

 */

function SuperType(name) {
    this.name = name;
    this.colors = ["red", "blue", "green"];
}

SuperType.prototype.sayName = function () {
    console.log(this.name);
};


function SubType(name, age) {
    // 继承属性
    SuperType.call(this, name);
    this.age = age;
}

// 继承方法
SubType.prototype = new SuperType();
SubType.prototype.sayAge = function () {
    console.log(this.age);
};

let instance1 = new SubType("Nicholas", 29);
instance1.colors.push("black");
console.log(instance1.colors);   // "red, blue, green, black"
instance1.sayName();               // "Nicholas";
instance1.sayAge();                // 29

let instance2 = new SubType("Greg", 27);
console.log(instance2.colors);   // "red, blue, green"
instance2.sayName();               // "Greg";
instance2.sayAge();                // 27
