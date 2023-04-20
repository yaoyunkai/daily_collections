function Person(name, age, job) {
    this.name = name;
    this.age = age;
    this.job = job;
    this.sayName = function () {
        console.log(this.name);
    };
}


// 作为构造函数
let person = new Person("Nicholas", 29, "Software Engineer");
person.sayName();     // "Nicholas"

// 作为函数调用
Person("Greg", 27, "Doctor");    // 添加到window对象
window.sayName();     // "Greg"

// 在另一个对象的作用域中调用
let o = new Object();
Person.call(o, "Kristen", 25, "Nurse");
o.sayName();    // "Kristen"
