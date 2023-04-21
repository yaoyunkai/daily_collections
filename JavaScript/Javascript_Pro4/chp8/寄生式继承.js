/*
parasitic inheritance

通过寄生式继承给对象添加函数会导致函数难以重用，与构造函数模式类似。

 */
function object(o) {
    function F() {
    }

    F.prototype = o;
    return new F();
}

function createAnother(original) {
    let clone = object(original);   // 通过调用函数创建一个新对象
    clone.sayHi = function () {      // 以某种方式增强这个对象
        console.log("hi");
    };
    return clone;              // 返回这个对象
}

let person = {
    name: "Nicholas", friends: ["Shelby", "Court", "Van"]
};
let anotherPerson = createAnother(person);
anotherPerson.sayHi();   // "hi"


/*
基本思路是不通过调用父类构造函数给子类原型赋值，而是取得父类原型的一个副本。
说到底就是使用寄生式继承来继承父类原型，然后将返回的新对象赋值给子类原型。

 */
function inheritPrototype(subType, superType) {
    let prototype = object(superType.prototype);   // 创建对象
    prototype.constructor = subType;                  // 增强对象
    subType.prototype = prototype;                    // 赋值对象
}


function SuperType(name) {
    this.name = name;
    this.colors = ["red", "blue", "green"];
}

SuperType.prototype.sayName = function () {
    console.log(this.name);
};

function SubType(name, age) {
    SuperType.call(this, name);
    this.age = age;
}

inheritPrototype(SubType, SuperType);

SubType.prototype.sayAge = function () {
    console.log(this.age);
};
