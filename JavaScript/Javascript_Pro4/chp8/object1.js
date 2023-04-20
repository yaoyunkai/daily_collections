/*
属性的特征

属性分为 数据属性和访问器属性

Configurable: True
Enumerable: True
Writable: True
Value: True

在调用Object.defineProperty()时，configurable、enumerable和writable的值如果不指定，则都默认为false

访问器属性:
Configurable
Enumerable
Get
Set

Object.getOwnPropertyDescriptor()
Object.assign(dest, src, result); 合并对象


*/


let person = new Object()
person.name = 'Tom'
person.age = 29
person.job = 'TE'
person.sayName = function () {
    console.log("Hi " + this.name)
};

let person2 = {
    name: "Nicholas", age: 29, job: "Software Engineer", sayName() {
        console.log(this.name);
    }
};


// person.sayName();
// person2.sayName();

Object.defineProperty(person, "aaa", {
    configurable: true, writable: true, enumerable: true, value: "RTY"
})

// console.log(person.aaa);

let book = {
    _year: 2017, edition: 1
};

Object.defineProperty(book, "year", {
    get() {
        return this._year;
    }, set(val) {
        if (val > 2017) {
            this._year = val;
            this.edition += val;
        }
    }

})


book.year = 2018;
console.log(book.edition);


const nameKey = 'name';
const ageKey = 'age';
const jobKey = 'job';
let person3 = {};
person3[nameKey] = 'Matt';
person3[ageKey] = 27;
person3[jobKey] = 'Software engineer';
console.log(person3); // { name: 'Matt', age: 27, job: 'Software engineer' }


/*
对象解构

 */

// 使用对象解构
let person4 = {
    name: 'Matt',
    age: 27
};
let {name: personName, age: personAge} = person4;
console.log(personName);   // Matt
console.log(personAge);    // 27