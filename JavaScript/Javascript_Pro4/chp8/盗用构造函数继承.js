/*
JS
func.call(this, arg1, arg2);
func.apply(this, [arg1, arg2])

-------------------------------------------------
盗用构造函数

盗用构造函数的主要缺点，也是使用构造函数模式自定义类型的问题：
必须在构造函数中定义方法，因此函数不能重用。


*/

function SuperType(name) {
    this.colors = ["red", "blue", "green"];
    this.name = name;
}

function SubType() {
    //继承SuperType
    SuperType.call(this, "SubType");
}

let instance1 = new SubType();
instance1.colors.push("black");
console.log(instance1.colors); // "red, blue, green, black"

let instance2 = new SubType();
console.log(instance2.colors); // "red, blue, green"

let instance = new SubType();
console.log(instance.name); // "Nicholas";
