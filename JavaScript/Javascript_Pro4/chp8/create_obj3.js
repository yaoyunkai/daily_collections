/*
构造函数的主要问题在于，其定义的方法会在每个实例上都创建一遍。

 */

function Person(name, age, job) {
    this.name = name;
    this.age = age;
    this.job = job;
    this.sayName = sayName;
}

function sayName() {
    console.log(this.name);
}

let person1 = new Person("Nicholas", 29, "Software Engineer");
let person2 = new Person("Greg", 27, "Doctor");
person1.sayName();   // Nicholas
person2.sayName();   // Greg

console.log(person1.sayName === person2.sayName)