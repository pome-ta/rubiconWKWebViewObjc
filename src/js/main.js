console.log(1);

function addElement() {
  // 新しい div 要素を作成します
  const newDiv = document.createElement('div');

  // いくつかの内容を与えます
  const newContent = document.createTextNode('みなさん、こんにちは!');

  // テキストノードを新規作成した div に追加します
  newDiv.appendChild(newContent);

  // DOM に新しく作られた要素とその内容を追加します
  const currentDiv = document.getElementById('div1');
  document.body.insertBefore(newDiv, currentDiv);
}

document.addEventListener('DOMContentLoaded', (event) => {
  console.log(2);
  addElement()
});


window.addEventListener('load', (event) => {
  console.log(3);
});

console.log(4);
