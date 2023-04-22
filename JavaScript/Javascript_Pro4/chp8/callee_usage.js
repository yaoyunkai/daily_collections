/*
递归调用问题

 */


function factorial(num) {
    if (num <= 1) {
        return 1;
    } else {
        return num * arguments.callee(num - 1);
    }
}

(function () {
    // 块级作用域
    console.log('call soon')
})();