console.log("*******************")
console.log("*******************")
console.log("*******************")
console.log("*******************")
console.log("*******************")

var myId = 'my-container'
var body = document.getElementsByTagName('body')[0]
var newNode = document.createElement('div');
newNode.setAttribute('id', myId);
body.appendChild(newNode);

console.log(body)
console.log(document.getElementById("chem_dropdown"))


document.getElementById("chem_dropdown").addEventListener("change", function () {
    alert("ciao")
    var myElement = document.getElementById(myId);
    myElement.innerHtml = ([
        '<div>',
        '<hr/>',
        '<div style="font-size: 14px;">CIAO!</div>',
        '</div>'
    ].join(''))
});
