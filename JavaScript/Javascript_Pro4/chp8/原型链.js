/*
通过重写子类构造器函数的prototype为父类构造器函数的实例
来实现继承父类的原型

SubType的实例不仅能从SuperType的实例中继承属性和方法，而且还与SuperType的原型挂上了钩。
于是instance（通过内部的[[Prototype]]）指向SubType.prototype

---------------------------------------------------------
原型链的第二个问题是，子类型在实例化时不能给父类型的构造函数传参。
事实上，我们无法在不影响所有对象实例的情况下把参数传进父类的构造函数。



 */

function SuperType() {
    this.property = true;
}

SuperType.prototype.getSuperValue = function () {
    return this.property;
};

function SubType() {
    this.subproperty = false;
}

// 继承SuperType
SubType.prototype = new SuperType();
//新方法
SubType.prototype.getSubValue = function () {
    return this.subproperty;
};
//覆盖已有的方法
SubType.prototype.getSuperValue = function () {
    return false;
};

let instance = new SubType();
console.log(instance.getSuperValue()); // false
