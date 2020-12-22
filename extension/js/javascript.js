// console.log("working");
// document
//   .getElementById("test")
//   .addEventListener("click", console.log("clicked!"));
console.log("here1");

document.querySelector("h1").addEventListener("click", function () {
  console.log("clicked");
});
document.getElementById("test_button").addEventListener("click", testFunction);

function testFunction() {
  console.log("DAYM");
}

// function () {
//   console.log("clicked test button");
// });
// document.querySelectorAll('button')[i].addEventListener('click', function (){
//     makeSound(this.innerHTML);
//     buttonAnimation(this.innerHTML);
// }
