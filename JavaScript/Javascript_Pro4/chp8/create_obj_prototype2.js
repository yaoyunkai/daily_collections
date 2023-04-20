/*
重写整个原型会切断最初原型与构造函数的联系，但实例引用的仍然是最初的原型。

 */

function Person() {
}

// 完全重写了Person的prototype，现在constructor不会指向Person
Person.prototype = {
    name: "Nicholas",
    age: 29,
    job: "Software Engineer",
    sayName() {
        console.log('say name: ' + this.name);
    }
};


let person1 = new Person();
person1.name = "Tom";
person1.sayName();


let friend = new Person();
console.log(friend instanceof Object);        // true
console.log(friend instanceof Person);        // true
console.log(friend.constructor === Person);   // false
console.log(friend.constructor === Object);   // true


function Person2() {
}

// 但这里的 constructor 的特性 Enumerable 为 True
Person2.prototype = {
    constructor: Person2,
    name: "Nicholas",
    age: 29,
    job: "Software Engineer",
    sayName() {
        console.log(this.name);
    }
};

function Person3() {
}

Person3.prototype = {
    name: "Nicholas",
    age: 29,
    job: "Software Engineer",
    sayName() {
        console.log(this.name);
    }
};
// 恢复constructor属性
Object.defineProperty(Person3.prototype, "constructor", {
    enumerable: false,
    value: Person3
});